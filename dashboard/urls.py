from django.urls import path

from dashboard.views import (
    DashboardDeadlinesView,
    DashboardDocumentsView,
    DashboardFinancialView,
    DashboardSummaryView,
    DashboardTasksView,
)


urlpatterns = [
    path('summary/', DashboardSummaryView.as_view()),
    path('deadlines/', DashboardDeadlinesView.as_view()),
    path('tasks/', DashboardTasksView.as_view()),
    path('documents/', DashboardDocumentsView.as_view()),
    path('financial/', DashboardFinancialView.as_view()),
]

