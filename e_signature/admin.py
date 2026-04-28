from django.contrib import admin

from e_signature.models import SignatureAuditTrail, SignatureParty, SignatureRequest, SignedDocument


admin.site.register(SignatureRequest)
admin.site.register(SignatureParty)
admin.site.register(SignedDocument)
admin.site.register(SignatureAuditTrail)

