import os
import datetime
from tempfile import NamedTemporaryFile

from InvoiceGenerator.api import Invoice, Item, Client, Provider, Creator, Address
from InvoiceGenerator.pdf import SimpleInvoice
import sendEmail

# choose english as language
os.environ["INVOICE_LANG"] = "en"



def info(einvoice,ename,ephone,eemail):
    global client, provider,creator, invoiceId, nameCustomer, phoneCustomer, emailCustomer, invoice
    invoiceId, nameCustomer, phoneCustomer, emailCustomer=einvoice, ename, ephone,eemail 
    client = Client(ename)#phone=ephone,email=eemail)
    provider = Provider('Smart Kart Pvt. Ltd.',address='India', city='Hyd', zip_code='590073', phone='040-88999889', email='smartkartindia.pvtltd@gmail.co', bank_account='2600420569', bank_code='762010')
    creator = Creator('"Team Smart Kart"')
    invoice = Invoice(client, provider, creator)
    invoice.currency= "\u20B9"
    invoice.number=einvoice #invoice number 
    invoice.paytype='Card payment'
    invoice.title='Smart Kart'

def prodinfo(name,rate,qty,total):
    
    invoice.add_item(Item(qty, rate, description=name))

def savepdf():
    pdf = SimpleInvoice(invoice)
    pdf.gen("invoice.pdf", generate_qr_code=True)
    print(emailCustomer)
    sendEmail.sendInvoice(emailCustomer)

'''
Client(summary, address='', city='', zip_code='', phone='', 
email='', bank_name='', bank_account='', bank_code='', note='', vat_id='', ir='', 
logo_filename='', vat_note='')

Provider(summary, address='', city='', zip_code='', phone='', email='',
bank_name='', bank_account='', bank_code='', note='', vat_id='', ir='', 
logo_filenam  e='', vat_note='')

Creator(name, stamp_filename='')

Address(summary, address='', city='', zip_code='', phone='', email='',
bank_name='', bank_account='', bank_code='', note='', vat_id='', ir='', logo_filename='', vat_note='')
-------------------------------------------------------------------------------------------------------------
add_item(item)
Add item to the invoice.

Parameters:	item (Item class) – the new item
currency= u'K\u010d'
currency identifier (e.g. “$” or “Kč”)

currency_locale= 'cs_CZ.UTF-8'
currency_locale: locale according to which will be the written currency representations

date= None
date of exposure

difference_in_rounding
Difference between rounded price and real price.

generate_breakdown_vat()
generate_breakdown_vat_table()
iban= None
iban

items
Items on the invoice.

number= None
number or string used as the invoice identifier

payback= None
due date

paytype= None
textual description of type of payment

price
Total sum price without taxes.

price_tax
Total sum price including taxes.

rounding_result= False
round result to integers?

rounding_strategy= 'ROUND_HALF_EVEN'
Result rounding strategy (identifiers from decimal module). Default strategy for rounding in Python is bankers’ rounding, which means that half of the X.5 numbers are rounded down and half up. Use this parameter to set different rounding strategy.

specific_symbol= None
specific_symbol

swift= None
swift

taxable_date= None
taxable date
title= ''
title on the invoice

use_tax= False
variable_symbol= None
variable symbol associated with the payment
'''
