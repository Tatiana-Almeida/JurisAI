import re
import unicodedata
import uuid
from pathlib import Path


MAX_UPLOAD_FILENAME_BASENAME_LENGTH = 80


def generate_uuid():
    return uuid.uuid4()


def sanitize_upload_filename(filename):
    raw_name = str(filename or '')
    basename = raw_name.replace('\\', '/').split('/')[-1]
    suffix = Path(basename).suffix.lower()
    stem = Path(basename).stem

    normalized_stem = unicodedata.normalize('NFKD', stem).encode('ascii', 'ignore').decode('ascii')
    normalized_stem = re.sub(r'\s+', '_', normalized_stem)
    normalized_stem = re.sub(r'[^A-Za-z0-9_-]+', '_', normalized_stem)
    normalized_stem = re.sub(r'_+', '_', normalized_stem).strip('_-')

    if not normalized_stem:
        normalized_stem = 'document'

    normalized_stem = normalized_stem[:MAX_UPLOAD_FILENAME_BASENAME_LENGTH].rstrip('_-')
    if not normalized_stem:
        normalized_stem = 'document'

    return f'{normalized_stem}{suffix}'


def document_upload_path(instance, filename):
    organization_id = getattr(instance, 'organization_id', 'unknown')
    case_id = getattr(instance, 'law_case_id', 'general')
    safe_filename = sanitize_upload_filename(filename)
    return Path('documents') / str(organization_id) / str(case_id) / f'{uuid.uuid4()}_{safe_filename}'
