from ingestion.extensions import ma
from ingestion.models import Account, Transaction


class AccountSchema(ma.SQLAlchemySchema):
    class Meta:
        model = Account
        load_instance = True

    account_id = ma.auto_field()
    name = ma.auto_field()
    type = ma.auto_field()
    created_at = ma.auto_field()
    updated_at = ma.auto_field()


class TransactionSchema(ma.SQLAlchemySchema):
    class Meta:
        model = Transaction
        load_instance = True

    transaction_id = ma.auto_field()
    account_id = ma.auto_field()
    amount = ma.auto_field()
    currency = ma.auto_field()
    date = ma.auto_field()
    merchant_name = ma.auto_field()
    description = ma.auto_field()
    category = ma.auto_field()
    batch_id = ma.auto_field()
    ingestion_status = ma.auto_field()
    created_at = ma.auto_field()
    updated_at = ma.auto_field()
