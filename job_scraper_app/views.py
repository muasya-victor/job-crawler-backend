from django.contrib.auth import authenticate
from reportlab.lib.units import inch
from rest_framework import status, generics, permissions
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Job, User, AttemptedJobs, Portfolio
from .scraper import linkedin_scraper
from .serializers import JobSerializer, UserSerializer, AttemptedJobsSerializer, PortfolioSerializer,CustomTokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from django.http import HttpResponse
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter, landscape
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle
from .models import Job


def generate_pdf_report(request):
    # Query available jobs
    available_jobs = Job.objects.all()

    # Create a PDF document
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="job_report.pdf"'

    doc = SimpleDocTemplate(response, pagesize=landscape(letter), leftMargin=50, rightMargin=50, topMargin=50, bottomMargin=50)
    elements = []

    # Define table data
    data = [['Job Title', 'Company Name', 'Job ID', 'Level', 'Description']]
    for job in available_jobs:
        data.append([job.job_title, job.job_company_name, job.job_id, job.job_level,
                     job.job_description ])

    # Create a table and add data to it
    col_widths = [2 * inch, 1 * inch, 1 * inch, 1 * inch, 1 * inch, 2 * inch, 2 * inch]  # Specify custom widths

    # Create a table and add data to it
    table = Table(data, colWidths=col_widths )
    table = Table(data)



    table.setStyle(TableStyle([('BACKGROUND', (0, 0), (-1, 0), colors.grey),
                               ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                               ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                               ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                               ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                               ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                               ('GRID', (0, 0), (-1, -1), 1, colors.black),
                               ('WORDWRAP', (0, 0), (-1, -1)),
                               ('OVERFLOW', (0, 0), (-1, -1), 'ELLIPSE')]))
    table._argH[0] = 0.5 * inch # Increase height of the header row
    table.setStyle(TableStyle([('TEXTCOLOR', (0, 0), (-1, -1), colors.black),
                               ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
                               ('FONTSIZE', (0, 0), (-1, -1), 10)]))



    # Add the table to the PDF document
    elements.append(table)
    doc.build(elements)

    return response


class AttemptedJobsPdfReportView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        attempted_jobs = AttemptedJobs.objects.all()

        # Create a PDF document
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="attempted_jobs_report.pdf"'

        doc = SimpleDocTemplate(response, pagesize=landscape(letter), leftMargin=50, rightMargin=50, topMargin=50, bottomMargin=50)
        elements = []

        # Define table data
        data = [['ID', 'Job Title','Date Attempted', 'Status']]
        for job in attempted_jobs:
            data.append([job.id, job.attempted_job,job.date_attempted, job.attempted_job_status])

        num_cols = len(data[0])
        col_widths = [0.5 * inch, 1 * inch, 1 * inch, 1 * inch, 1 * inch, 2 * inch, 2 * inch]  # Specify custom widths

        # Create a table and add data to it
        table = Table(data, colWidths=col_widths)
        # Create a table and add data to it
        table = Table(data)
        table._argH[0] = 0.5 * inch  # Increase height of the header row
        table.setStyle(TableStyle([('BACKGROUND', (0, 0), (-1, 0), colors.grey),
                                   ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                                   ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                                   ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                                   ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                                   ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                                   ('GRID', (0, 0), (-1, -1), 1, colors.black),
                                   ('WORDWRAP', (0, 0), (-1, -1)),
                                   ('OVERFLOW', (0, 0), (-1, -1), 'ELLIPSE')]))
        table._argH[0] = 0.5 * inch  # Increase height of the header row
        table.setStyle(TableStyle([('TEXTCOLOR', (0, 0), (-1, -1), colors.black),
                                   ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
                                   ('FONTSIZE', (0, 0), (-1, -1), 10)]))

        # Add the table to the PDF document
        elements.append(table)
        doc.build(elements)

        return response

class CustomTokenObtainPairView(TokenObtainPairView):
    permissions = AllowAny
    serializer_class = CustomTokenObtainPairSerializer


class UserCreateView(generics.CreateAPIView):
    serializer_class = UserSerializer

    def post(self, request, *args, **kwargs):
        serializer = UserSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class JobListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, format=None):
        jobs = Job.objects.all()
        serializer = JobSerializer(jobs, many=True)
        return Response(serializer.data)


class UserListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, format=None):
        user = User.objects.all()
        serializer = UserSerializer(user, many=True)
        return Response(serializer.data)


class AttemptedJobsListView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    queryset = AttemptedJobs.objects.all()
    serializer_class = AttemptedJobsSerializer


class AttemptedJobsCreateView(generics.CreateAPIView):
    permission_classes = [IsAuthenticated]
    queryset = AttemptedJobs.objects.all()
    serializer_class = AttemptedJobsSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)  # Assuming you are using authentication
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PortfolioListView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Portfolio.objects.all()
    serializer_class = PortfolioSerializer


class ScrapedJobListView(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request, format=None):
        keywords = request.data.get('keywords')
        location = request.data.get('location')
        webpage = request.data.get('webpage_url')
        trk = request.data.get('trk')
        position = request.data.get('position')
        page_number = request.data.get('page_number')
        limit = request.data.get('limit')
        start = request.data.get('start')
        save_to_db = request.data.get('save_to_db', True)

        webpage_url = f"{webpage}?keywords={keywords}&location={location}&start={start}&trk={trk}&position={position}&pageNum={page_number}&limit={limit}"

        # Ensure all required parameters are provided
        # linkedin_scraper(webpage_url, position, start, limit, keywords, location, trk, save_to_db, page_number)
        linkedin_scraper(webpage_url, position, start, limit, keywords, location, trk, page_number)

        return Response("Scraping completed", status=status.HTTP_200_OK)

