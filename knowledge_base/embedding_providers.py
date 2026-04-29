import hashlib
import math
import re
import unicodedata


LOCAL_EMBEDDING_PROVIDER = 'local'
LOCAL_EMBEDDING_MODEL = 'local-hash-v1'
LOCAL_EMBEDDING_DIMENSION = 64


def _normalize_text(text):
    text = (text or '').strip().lower()
    normalized = unicodedata.normalize('NFKD', text)
    return ''.join(char for char in normalized if not unicodedata.combining(char))


def _tokenize(text):
    return re.findall(r'[a-z0-9]+', _normalize_text(text))


def _normalize_vector(values):
    magnitude = math.sqrt(sum(value * value for value in values))
    if magnitude == 0:
        return [0.0 for _ in values]
    return [round(value / magnitude, 12) for value in values]


class BaseEmbeddingProvider:
    provider = ''
    model = ''
    dimension = LOCAL_EMBEDDING_DIMENSION
    is_external = False

    def generate_embedding(self, text):
        raise NotImplementedError


class LocalHashEmbeddingProvider(BaseEmbeddingProvider):
    provider = LOCAL_EMBEDDING_PROVIDER
    model = LOCAL_EMBEDDING_MODEL
    dimension = LOCAL_EMBEDDING_DIMENSION

    def __init__(self, model=None):
        self.model = model or self.model

    def generate_embedding(self, text):
        tokens = _tokenize(text)
        vector = [0.0] * self.dimension

        if not tokens:
            return vector

        for token in tokens:
            digest = hashlib.sha256(token.encode('utf-8')).digest()
            for offset in range(0, min(len(digest), 16), 4):
                bucket = digest[offset] % self.dimension
                sign = 1 if digest[offset + 1] % 2 == 0 else -1
                magnitude = 1.0 + (digest[offset + 2] / 255.0)
                vector[bucket] += sign * magnitude

        return _normalize_vector(vector)


class ExternalEmbeddingProviderPlaceholder(BaseEmbeddingProvider):
    is_external = True

    def __init__(self, provider, model=''):
        self.provider = provider or 'other'
        self.model = model or ''

    def generate_embedding(self, text):
        raise NotImplementedError('External embedding providers are not enabled in this phase.')


def get_embedding_provider(settings):
    provider_name = getattr(settings, 'embedding_provider', '') or ''
    model_name = getattr(settings, 'embedding_model', '') or ''

    if provider_name == LOCAL_EMBEDDING_PROVIDER:
        return LocalHashEmbeddingProvider(model=model_name or LOCAL_EMBEDDING_MODEL)

    return ExternalEmbeddingProviderPlaceholder(provider=provider_name or 'other', model=model_name)
