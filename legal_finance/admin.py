from django.contrib import admin

from legal_finance.models import ClientInvoice, Expense, LegalFee, PaymentRecord


admin.site.register(ClientInvoice)
admin.site.register(LegalFee)
admin.site.register(Expense)
admin.site.register(PaymentRecord)

