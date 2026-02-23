
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

class Invoice(BaseModel):
    number = CharField()
    date_issue = DateField()
    description = TextField() # Opis zdarzenia dla AI
    amount = DecimalField(max_digits=10, decimal_places=2)
    contractor = ForeignKeyField(Contractor, backref='invoices')
    created_at = DateField(default=datetime.date.today)

class InvoiceLine(BaseModel):
    invoice = ForeignKeyField(Invoice, backref='lines')
    account_wn = ForeignKeyField(Account, backref='lines_wn')
    account_ma = ForeignKeyField(Account, backref='lines_ma')
    amount = DecimalField(max_digits=10, decimal_places=2)
