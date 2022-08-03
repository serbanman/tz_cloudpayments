from marshmallow import Schema, fields


class ParamsSchema(Schema):
    Amount = fields.Float(required=True, data_key='amount')
    IpAddress = fields.Str(required=True, data_key='ip_address')
    CardCryptogramPacket = fields.Str(required=True, data_key='card_cryptogram_packet')

    Currency = fields.Str(data_key='currency')
    Name = fields.Str(data_key='name')
    PaymentUrl = fields.Str(data_key='payment_url')
    InvoiceId = fields.Str(data_key='invoice_id')
    Description = fields.Str(data_key='description')
    CultureName = fields.Str(data_key='culture_name')
    AccountId = fields.Str(data_key='account_id')
    Email = fields.Str(data_key='email')
    Payer = fields.Str(data_key='payer')
    JsonData = fields.Str(data_key='json_data')
