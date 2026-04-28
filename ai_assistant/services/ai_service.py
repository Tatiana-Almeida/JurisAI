import os
import json
from django.conf import settings
from django.utils import timezone
from rest_framework.exceptions import Throttled
from ai_assistant.models import AIRequest

try:
    import openai
    OPENAI_AVAILABLE = True
except ImportError:
    openai = None
    OPENAI_AVAILABLE = False

API_KEY = os.getenv('OPENAI_API_KEY', settings.OPENAI_API_KEY)
if OPENAI_AVAILABLE:
    openai.api_key = API_KEY

SYSTEM_PROMPT = 'Você é um assistente jurídico que gera textos claros, objetivos e compatíveis com a legislação brasileira.'
PLAN_IA_LIMITS = {
    'free': 20,
    'solo': 100,
    'growth': 100,
    'enterprise': 2000,
}


def _mock_response(default_text: str):
    return {
        'choices': [
            {
                'message': {
                    'content': default_text,
                }
            }
        ]
    }


def _record_ai_request(user, organization, prompt, response, tokens_used=0, cost=0):
    if organization is None:
        return

    try:
        AIRequest.objects.create(
            user=user if getattr(user, 'is_authenticated', False) else None,
            organization=organization,
            prompt=prompt,
            response=response,
            tokens_used=tokens_used,
            cost=cost,
        )
    except Exception:
        pass


def _ensure_ai_quota(organization):
    if organization is None:
        return

    limit = organization.ai_request_limit() if hasattr(organization, 'ai_request_limit') else PLAN_IA_LIMITS.get(organization.plan, 20)
    now = timezone.now()
    used = AIRequest.objects.filter(
        organization=organization,
        created_at__year=now.year,
        created_at__month=now.month,
    ).count()

    if used >= limit:
        raise Throttled(detail='Limite de requisições IA do plano atingido. Faça upgrade para continuar usando.')


class AIService:
    @staticmethod
    def _call_openai(messages, max_tokens=800):
        if not API_KEY or not OPENAI_AVAILABLE:
            return _mock_response('Resposta de mock: chave OpenAI não configurada.')

        return openai.ChatCompletion.create(
            model='gpt-4o-mini',
            messages=messages,
            max_tokens=max_tokens,
            temperature=0.2,
        )

    def gerar_peticao(self, contexto: str, tipo: str, user=None, organization=None) -> str:
        _ensure_ai_quota(organization)
        prompt = [
            {'role': 'system', 'content': SYSTEM_PROMPT},
            {'role': 'user', 'content': f'Gere uma petição do tipo {tipo} com o seguinte contexto: {contexto}'},
        ]
        result = self._call_openai(prompt)
        text = result['choices'][0]['message']['content'].strip() if isinstance(result, dict) else result.choices[0].message.content.strip()
        _record_ai_request(user, organization, json.dumps(prompt), text)
        return text

    def resumir_documento(self, texto: str, user=None, organization=None) -> str:
        _ensure_ai_quota(organization)
        prompt = [
            {'role': 'system', 'content': SYSTEM_PROMPT},
            {'role': 'user', 'content': f'Resuma o texto a seguir com foco jurídico: {texto}'},
        ]
        result = self._call_openai(prompt)
        text = result['choices'][0]['message']['content'].strip() if isinstance(result, dict) else result.choices[0].message.content.strip()
        _record_ai_request(user, organization, json.dumps(prompt), text)
        return text

    def analisar_risco_processo(self, dados: dict, user=None, organization=None) -> dict:
        _ensure_ai_quota(organization)
        prompt = [
            {'role': 'system', 'content': SYSTEM_PROMPT},
            {'role': 'user', 'content': f'Analise o risco do seguinte processo: {dados}'},
        ]
        result = self._call_openai(prompt)
        text = result['choices'][0]['message']['content'].strip() if isinstance(result, dict) else result.choices[0].message.content.strip()
        _record_ai_request(user, organization, json.dumps(prompt), json.dumps({'risk_analysis': text}))
        return {'risk_analysis': text}

    def pesquisar_jurisprudencia(self, query: str, user=None, organization=None) -> dict:
        _ensure_ai_quota(organization)
        prompt = [
            {'role': 'system', 'content': SYSTEM_PROMPT},
            {'role': 'user', 'content': f'Pesquise jurisprudência relevante para: {query}. Retorne em formato estruturado.'},
        ]
        result = self._call_openai(prompt)
        text = result['choices'][0]['message']['content'].strip() if isinstance(result, dict) else result.choices[0].message.content.strip()
        _record_ai_request(user, organization, json.dumps(prompt), json.dumps({'search_results': text}))
        return {'search_results': text}

    def redigir_contrato(self, requisitos: str, user=None, organization=None) -> str:
        _ensure_ai_quota(organization)
        prompt = [
            {'role': 'system', 'content': SYSTEM_PROMPT},
            {'role': 'user', 'content': f'Redija um contrato jurídico com os seguintes requisitos: {requisitos}. Utiliza terminologia clara e inclua cláusulas de proteção para a organização.'},
        ]
        result = self._call_openai(prompt)
        text = result['choices'][0]['message']['content'].strip() if isinstance(result, dict) else result.choices[0].message.content.strip()
        _record_ai_request(user, organization, json.dumps(prompt), text)
        return text

    def revisar_documento(self, texto: str, user=None, organization=None) -> dict:
        _ensure_ai_quota(organization)
        prompt = [
            {'role': 'system', 'content': SYSTEM_PROMPT},
            {'role': 'user', 'content': f'Revise o seguinte documento e aponte melhorias, riscos e inconsistências legais: {texto}'},
        ]
        result = self._call_openai(prompt)
        text = result['choices'][0]['message']['content'].strip() if isinstance(result, dict) else result.choices[0].message.content.strip()
        _record_ai_request(user, organization, json.dumps(prompt), json.dumps({'review': text}))
        return {'review': text}
