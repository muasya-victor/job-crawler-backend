from django.urls import path
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions

from .views import JobListView, ScrapedJobListView, UserCreateView, PortfolioListView, AttemptedJobsListView, \
    CustomTokenObtainPairView, AttemptedJobsCreateView, UserListView, generate_pdf_report, AttemptedJobsPdfReportView

schema_view = get_schema_view(
    openapi.Info(
       title="Job Crawler",
       default_version='v1',
       description="Your API description",
       terms_of_service="https://www.example.com/policies/terms/",
       contact=openapi.Contact(email="vicmwe184@gmail.com"),
       license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path('available-jobs/', JobListView.as_view(), name='job-list'),
    path('user-user_portfolio/', JobListView.as_view(), name='job-list'),
    path('user-reviews/', JobListView.as_view(), name='job-list'),
    path('attempted-jobs/', AttemptedJobsListView.as_view(), name='job-list'),
    path('attempted-create/', AttemptedJobsCreateView.as_view(), name='attempted-jobs-create'),
    path('scrape-jobs/', ScrapedJobListView.as_view(), name='scrape-jobs'),
    path('register-users/', UserCreateView.as_view(), name='register'),
    path('users/', UserListView.as_view(), name='users'),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    path('attempted/', AttemptedJobsListView.as_view(), name='attempted-jobs-list'),
    path('user_portfolio/', PortfolioListView.as_view(), name='user_portfolio-list'),
    path('token/request/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('generate-pdf-report/', generate_pdf_report, name='generate_pdf_report'),
    path('attempted-jobs-pdf-report/', AttemptedJobsPdfReportView.as_view(), name='attempted_job_pdf_report'),

]
