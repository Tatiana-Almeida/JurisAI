from django.contrib import admin

from knowledge_base.models import DocumentChunk, KnowledgeBase, KnowledgeDocument, RetrievalQuery


admin.site.register(KnowledgeBase)
admin.site.register(KnowledgeDocument)
admin.site.register(DocumentChunk)
admin.site.register(RetrievalQuery)

