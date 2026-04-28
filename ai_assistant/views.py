from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import viewsets
from ai_assistant.services.ai_service import AIService
from ai_assistant.models import AIRequest
from ai_assistant.serializers import AIRequestSerializer
from jurisai.permissions import IsOrganizationMember

class GeneratePetitionView(APIView):
    permission_classes = [IsAuthenticated, IsOrganizationMember]

    def post(self, request):
        contexto = request.data.get('contexto', '')
        tipo = request.data.get('tipo', 'petição')
        output = AIService().gerar_peticao(
            contexto,
            tipo,
            user=request.user,
            organization=getattr(request.user, 'organization', None),
        )
        return Response({'text': output})

class SummarizeDocumentView(APIView):
    permission_classes = [IsAuthenticated, IsOrganizationMember]

    def post(self, request):
        texto = request.data.get('texto', '')
        output = AIService().resumir_documento(
            texto,
            user=request.user,
            organization=getattr(request.user, 'organization', None),
        )
        return Response({'summary': output})

class AnalyzeRiskView(APIView):
    permission_classes = [IsAuthenticated, IsOrganizationMember]

    def post(self, request):
        dados = request.data.get('dados', {})
        output = AIService().analisar_risco_processo(
            dados,
            user=request.user,
            organization=getattr(request.user, 'organization', None),
        )
        return Response(output)

class SearchJurisprudenceView(APIView):
    permission_classes = [IsAuthenticated, IsOrganizationMember]

    def post(self, request):
        query = request.data.get('query', '')
        output = AIService().pesquisar_jurisprudencia(
            query,
            user=request.user,
            organization=getattr(request.user, 'organization', None),
        )
        return Response(output)

class DraftContractView(APIView):
    permission_classes = [IsAuthenticated, IsOrganizationMember]

    def post(self, request):
        requisitos = request.data.get('requisitos', '')
        output = AIService().redigir_contrato(
            requisitos,
            user=request.user,
            organization=getattr(request.user, 'organization', None),
        )
        return Response({'contract': output})

class ReviewDocumentView(APIView):
    permission_classes = [IsAuthenticated, IsOrganizationMember]

    def post(self, request):
        texto = request.data.get('texto', '')
        output = AIService().revisar_documento(
            texto,
            user=request.user,
            organization=getattr(request.user, 'organization', None),
        )
        return Response(output)

class AIRequestViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = AIRequest.objects.select_related('user', 'organization').all()
    serializer_class = AIRequestSerializer
    permission_classes = [IsAuthenticated, IsOrganizationMember]

    def get_queryset(self):
        queryset = super().get_queryset()
        if self.request.user.organization:
            return queryset.filter(organization=self.request.user.organization)
        return queryset.none()
