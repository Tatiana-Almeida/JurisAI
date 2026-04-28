from django.contrib import admin

from ocr.models import OCRJob, OCRResult


admin.site.register(OCRJob)
admin.site.register(OCRResult)

