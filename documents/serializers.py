from pathlib import Path
import zipfile

from rest_framework import serializers
from documents.models import Document
from law_cases.models import LawCase
from jurisai.serializers import OrganizationScopedValidationMixin, TenantRelationValidationMixin


MAX_DOCUMENT_UPLOAD_BYTES = 10 * 1024 * 1024
ALLOWED_DOCUMENT_UPLOAD_TYPES = {
    '.pdf': {'application/pdf'},
    '.doc': {'application/msword'},
    '.docx': {'application/vnd.openxmlformats-officedocument.wordprocessingml.document'},
    '.txt': {'text/plain'},
    '.jpg': {'image/jpeg'},
    '.jpeg': {'image/jpeg'},
    '.png': {'image/png'},
}
MAGIC_SIGNATURES = {
    '.pdf': b'%PDF',
    '.png': b'\x89PNG\r\n\x1a\n',
    '.jpg': b'\xff\xd8\xff',
    '.jpeg': b'\xff\xd8\xff',
}
DOCX_ZIP_SIGNATURES = (
    b'PK\x03\x04',
    b'PK\x05\x06',
    b'PK\x07\x08',
)
DOCX_REQUIRED_ENTRIES = {
    '[Content_Types].xml',
    '_rels/.rels',
    'word/document.xml',
}


class DocumentSerializer(TenantRelationValidationMixin, OrganizationScopedValidationMixin, serializers.ModelSerializer):
    law_case_id = serializers.UUIDField(write_only=True)
    organization_id = serializers.UUIDField(write_only=True, required=False)
    tenant_relation_fields = {
        'law_case_id': LawCase,
    }

    class Meta:
        model = Document
        fields = ['id', 'law_case', 'law_case_id', 'type', 'content', 'file', 'version', 'organization_id', 'created_at', 'updated_at']
        read_only_fields = ['law_case', 'version', 'created_at', 'updated_at']

    def _matches_magic_signature(self, uploaded_file, extension):
        expected_signature = MAGIC_SIGNATURES.get(extension)
        if not expected_signature:
            return True

        uploaded_file.seek(0)
        header = uploaded_file.read(len(expected_signature))
        uploaded_file.seek(0)
        return header.startswith(expected_signature)

    def _is_valid_docx_structure(self, uploaded_file):
        uploaded_file.seek(0)
        header = uploaded_file.read(4)

        if not header.startswith(DOCX_ZIP_SIGNATURES):
            uploaded_file.seek(0)
            return False

        uploaded_file.seek(0)

        try:
            with zipfile.ZipFile(uploaded_file) as archive:
                names = set(archive.namelist())
                return DOCX_REQUIRED_ENTRIES.issubset(names)
        except zipfile.BadZipFile:
            return False
        finally:
            uploaded_file.seek(0)

    def validate_file(self, uploaded_file):
        if not uploaded_file:
            return uploaded_file

        extension = Path(uploaded_file.name).suffix.lower()
        allowed_content_types = ALLOWED_DOCUMENT_UPLOAD_TYPES.get(extension)
        if not allowed_content_types:
            raise serializers.ValidationError('Tipo de ficheiro nao permitido')

        if uploaded_file.size > MAX_DOCUMENT_UPLOAD_BYTES:
            raise serializers.ValidationError('Ficheiro excede o tamanho maximo permitido')

        content_type = getattr(uploaded_file, 'content_type', None)
        if content_type and content_type not in allowed_content_types:
            raise serializers.ValidationError('Content type do ficheiro nao corresponde a extensao')

        if not self._matches_magic_signature(uploaded_file, extension):
            raise serializers.ValidationError('Assinatura binaria do ficheiro nao corresponde ao formato declarado')

        if extension == '.docx' and not self._is_valid_docx_structure(uploaded_file):
            raise serializers.ValidationError('Estrutura DOCX invalida ou incompleta')

        return uploaded_file

    def create(self, validated_data, **kwargs):
        latest = Document.objects.filter(law_case_id=validated_data['law_case_id']).order_by('-version').first()
        version = latest.version + 1 if latest else 1
        return Document.objects.create(
            law_case_id=validated_data['law_case_id'],
            type=validated_data['type'],
            content=validated_data.get('content', ''),
            file=validated_data.get('file'),
            version=version,
            organization_id=validated_data['organization_id'],
        )
