from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from dashboard.services import (
    get_dashboard_documents,
    get_dashboard_financial,
    get_dashboard_summary,
    get_dashboard_tasks,
    get_upcoming_deadlines,
)
from documents.serializers import DocumentSerializer
from deadlines.serializers import DeadlineSerializer
from jurisai.permissions import IsOrganizationMember
from tasks.serializers import TaskSerializer


class DashboardSummaryView(APIView):
    permission_classes = [IsAuthenticated, IsOrganizationMember]

    def get(self, request):
        return Response(get_dashboard_summary(request.user.organization))


class DashboardDeadlinesView(APIView):
    permission_classes = [IsAuthenticated, IsOrganizationMember]

    def get(self, request):
        return Response(DeadlineSerializer(get_upcoming_deadlines(request.user.organization), many=True).data)


class DashboardTasksView(APIView):
    permission_classes = [IsAuthenticated, IsOrganizationMember]

    def get(self, request):
        return Response(TaskSerializer(get_dashboard_tasks(request.user.organization), many=True).data)


class DashboardDocumentsView(APIView):
    permission_classes = [IsAuthenticated, IsOrganizationMember]

    def get(self, request):
        return Response(DocumentSerializer(get_dashboard_documents(request.user.organization), many=True).data)


class DashboardFinancialView(APIView):
    permission_classes = [IsAuthenticated, IsOrganizationMember]

    def get(self, request):
        return Response(get_dashboard_financial(request.user.organization))
