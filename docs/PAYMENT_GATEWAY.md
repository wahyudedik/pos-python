# Payment Gateway Integration - Midtrans

## Overview

Sistem POS mengintegrasikan **Midtrans** sebagai payment gateway utama untuk mendukung multiple payment methods dan online settlements.

## Fitur Midtrans

### Payment Methods (25+ methods)
1. **Bank Transfer** - Virtual Account (BCA, BNI, Mandiri, CIMB, Permata, Bank Syariah)
2. **E-Wallet** - GoPay, OVO, DANA, ShopeePay, LinkAja
3. **QRIS** - Fast & standardized QR code payment
4. **Credit Card** - Visa, Mastercard, JCB, AmEx
5. **Debit Card** - Direct bank account debit
6. **Over-The-Counter** - Indomaret, Alfamart, Alfamidi
7. **Buy Now Pay Later** - Akulaku, Kredivo, IndoDana

### Settlement & Reconciliation
- Real-time settlement
- Automated daily reports
- Multi-merchant support
- Flexible settlement schedule

## Setup

### 1. Create Merchant Account

Daftar di https://dashboard.midtrans.com

### 2. Get Credentials

Setelah login, ambil:
- **Server Key** - Untuk backend calls
- **Client Key** - Untuk frontend integration

### 3. Configure Environment

Edit `.env` dengan credentials:
```env
MIDTRANS_ENABLED=True
MIDTRANS_ENVIRONMENT=sandbox  # atau production
MIDTRANS_SERVER_KEY=your_server_key
MIDTRANS_CLIENT_KEY=your_client_key
MIDTRANS_MERCHANT_ID=your_merchant_id
```

### 4. Test Connection

```python
from src.config.payment_config import PaymentConfig

# Validate configuration
try:
    config = PaymentConfig.get_midtrans_config()
    print("Midtrans configured successfully!")
except Exception as e:
    print(f"Configuration error: {e}")
```

## Integration Code

### Create Transaction

```python
from src.services.midtrans_gateway import MidtransGateway
from src.config.payment_config import PaymentConfig

# Initialize gateway
config = PaymentConfig.get_midtrans_config()
gateway = MidtransGateway(
    server_key=config['server_key'],
    environment=config['environment']
)

# Create transaction
result = gateway.create_transaction(
    order_id="ORD-20251204-001",
    gross_amount=500000,
    customer_email="customer@example.com",
    customer_phone="08123456789",
    customer_name="John Doe",
    item_details=[
        {
            'id': '1',
            'price': 250000,
            'quantity': 2,
            'name': 'Product A'
        }
    ]
)

# Get payment link
payment_link = result.get('redirect_url')
print(f"Payment link: {payment_link}")
```

### Check Transaction Status

```python
status = gateway.get_transaction_status(order_id="ORD-20251204-001")

print(f"Status: {status['transaction_status']}")
# status dapat: pending, settlement, expired, failed, denied, etc
```

## Payment Methods Configuration

Setiap payment method dapat dikonfigurasi di `src/config/payment_config.py`:

```python
PAYMENT_METHODS = {
    "gopay": {
        "name": "GoPay",
        "code": "gopay",
        "enabled": True,
        "requires_gateway": True,
        "gateway": "midtrans",
        "display_order": 4,
    },
    # ... more methods
}
```

### Enable/Disable Methods

Untuk disable payment method, set `enabled: False`:

```python
PAYMENT_METHODS["gopay"]["enabled"] = False
```

## POS Integration

### Sales Screen Payment Processing

```python
# Di sales_screen.py
def process_payment(self):
    """Process payment via Midtrans"""
    payment_method = self.combo_payment.currentText()
    total = float(self.lbl_total.text().replace("Rp ", ""))
    
    if payment_method == "Tunai":
        # Cash payment - langsung sukses
        self.process_cash_payment(total)
    else:
        # Online payment via Midtrans
        result = self.process_midtrans_payment(total, payment_method)
        if result:
            self.complete_sale()
```

### Receipt Integration

Receipt otomatis include:
- Order ID (untuk tracking)
- Payment method
- QR code (jika supported)
- Transaction timestamp
- Amount & change

## Testing

### Sandbox Testing

Gunakan sandbox environment untuk testing tanpa charge uang.

**Test Credentials (Sandbox):**
- Status: Always succeeds unless specified otherwise
- No real transactions occur

### Test Cases

1. **Successful Payment**
   - Use any card number ending in 11
   - Status: `settlement`

2. **Pending Payment**
   - Use card ending in 07
   - Status: `pending`

3. **Failed Payment**
   - Use card ending in 12
   - Status: `failed`

Detailed test data: https://docs.midtrans.com/reference/sandbox-test-data

## Webhook Handling

Midtrans mengirim notification ke webhook endpoint Anda.

### Setup Webhook

Di Midtrans Dashboard:
1. Settings → Webhook Configuration
2. Masukkan URL: `https://your-domain.com/api/webhook/midtrans`

### Webhook Handler

```python
# Di src/services/payment_service.py
@app.post("/api/webhook/midtrans")
def webhook_handler(request):
    """Handle Midtrans webhook notification"""
    
    # Parse payload
    transaction_status = request.json.get('transaction_status')
    order_id = request.json.get('order_id')
    
    # Update database
    if transaction_status == 'settlement':
        # Payment successful
        update_transaction_status(order_id, 'completed')
    elif transaction_status == 'failed':
        # Payment failed
        update_transaction_status(order_id, 'failed')
    
    return {'status': 'ok'}
```

## Fees & Pricing

### Transaction Fees (as of 2024)

| Method | Fee |
|--------|-----|
| Bank Transfer | Rp 4.000 |
| QRIS | 0.7% |
| GoPay | 2% |
| OVO | 2% |
| DANA | 1.5% |
| Credit Card | 2.9% + Rp 2.000 |
| OTC (Indomaret) | Rp 5.000 |
| BNPL | 1.7-2% |

**Note:** Fee exclude PPN kecuali untuk QRIS, GoPay, ShopeePay

### Estimation

Untuk toko dengan ~500 transaksi/bulan (Rp 2.5M GMV):
- **Monthly Cost:** ~Rp 26-30M
- **Fee %:** ~1% dari GMV

## Troubleshooting

### Connection Error

```
Error: Failed to connect to Midtrans API
```

**Solution:**
1. Check internet connection
2. Verify server key in `.env`
3. Check if using sandbox/production correctly

### Invalid Credentials

```
Error: Invalid server key or client key
```

**Solution:**
1. Copy credentials dari dashboard (jangan hardcode)
2. Ensure environment matches (sandbox vs production)
3. Check for extra spaces in credentials

### Webhook Not Received

**Solution:**
1. Whitelist Midtrans IPs
2. Verify webhook URL is publicly accessible
3. Check logs untuk incoming requests
4. Test manual trigger dari Midtrans dashboard

## Best Practices

1. **Always use HTTPS** - Especially in production
2. **Validate signatures** - Verify webhook signatures
3. **Handle timeouts** - Implement retry logic
4. **Log transactions** - Keep audit trail
5. **Test thoroughly** - Use sandbox before going live
6. **Monitor settlements** - Reconcile daily
7. **Keep credentials secret** - Never expose keys

## Support & Documentation

- **Midtrans Docs:** https://docs.midtrans.com
- **API Reference:** https://api-docs.midtrans.com
- **Dashboard:** https://dashboard.midtrans.com
- **Support:** https://support.midtrans.com

## Migration to Production

### Pre-Production Checklist

- [ ] Test all payment methods
- [ ] Verify webhook handling
- [ ] Setup HTTPS
- [ ] Configure production credentials
- [ ] Setup monitoring & alerts
- [ ] Create backup strategy
- [ ] Document procedures
- [ ] Train staff

### Production Configuration

```env
MIDTRANS_ENABLED=True
MIDTRANS_ENVIRONMENT=production
MIDTRANS_SERVER_KEY=prod_server_key_xxx
MIDTRANS_CLIENT_KEY=prod_client_key_xxx
MIDTRANS_MERCHANT_ID=merchant_id
```

---

**Last Updated:** Desember 2025
