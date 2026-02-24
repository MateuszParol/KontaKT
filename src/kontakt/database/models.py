
import datetime
from peewee import Model, CharField, DateField, DecimalField, ForeignKeyField, TextField, IntegerField
from kontakt.database.db import database

class BaseModel(Model):
    class Meta:
        database = database

class Account(BaseModel):
    symbol = CharField(unique=True)
    name = CharField()
    description = TextField(null=True)

class Contractor(BaseModel):
    nip = CharField(unique=True, null=True)
    name = CharField()
    address = TextField(null=True)

class Document(BaseModel):
    document_type = CharField(default="Faktura")
    number = CharField()
    date_issue = DateField()
    description = TextField() # Opis zdarzenia dla AI
    amount = DecimalField(max_digits=10, decimal_places=2)
    contractor = ForeignKeyField(Contractor, backref='documents')
    created_at = DateField(default=datetime.date.today)

class DocumentLine(BaseModel):
    document = ForeignKeyField(Document, backref='lines')
    account_wn = ForeignKeyField(Account, backref='lines_wn')
    account_ma = ForeignKeyField(Account, backref='lines_ma')
    amount = DecimalField(max_digits=10, decimal_places=2)

class ProductCatalog(BaseModel):
    name = CharField(unique=True)
    price_net = DecimalField(max_digits=10, decimal_places=2)
    vat_rate = CharField(default="23") # e.g. "23", "8", "zw"
    unit = CharField(default="szt.")

class SalesInvoice(BaseModel):
    number = CharField(unique=True)
    date_issue = DateField(default=datetime.date.today)
    date_sale = DateField(default=datetime.date.today)
    due_date = DateField(default=datetime.date.today)
    contractor = ForeignKeyField(Contractor, backref='sales_invoices')
    payment_method = CharField(default="przelew")
    created_at = DateField(default=datetime.date.today)

class SalesInvoiceItem(BaseModel):
    invoice = ForeignKeyField(SalesInvoice, backref='items')
    product_name = CharField()
    quantity = DecimalField(max_digits=10, decimal_places=2, default=1)
    price_net = DecimalField(max_digits=10, decimal_places=2)
    vat_rate = CharField()
    total_net = DecimalField(max_digits=10, decimal_places=2)
    total_gross = DecimalField(max_digits=10, decimal_places=2)

class Settings(BaseModel):
    key = CharField(unique=True)
    value = TextField(null=True)
