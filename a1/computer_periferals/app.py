# models.py
from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils import timezone

class Department(models.Model):
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=10, unique=True)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.code} - {self.name}"

class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    student_id = models.CharField(max_length=20, unique=True)
    phone = models.CharField(max_length=15)
    date_of_birth = models.DateField()
    address = models.TextField()
    department = models.ForeignKey(Department, on_delete=models.SET_NULL, null=True, blank=True)
    enrollment_date = models.DateField(default=timezone.now)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.student_id} - {self.user.get_full_name()}"

class Course(models.Model):
    SEMESTER_CHOICES = [
        ('FALL', 'Fall'),
        ('SPRING', 'Spring'),
        ('SUMMER', 'Summer'),
    ]
    
    name = models.CharField(max_length=200)
    code = models.CharField(max_length=10, unique=True)
    description = models.TextField()
    credits = models.PositiveIntegerField(validators=[MinValueValidator(1), MaxValueValidator(6)])
    department = models.ForeignKey(Department, on_delete=models.CASCADE)
    semester = models.CharField(max_length=10, choices=SEMESTER_CHOICES)
    year = models.PositiveIntegerField(default=timezone.now().year)
    max_enrollment = models.PositiveIntegerField(default=30)
    instructor = models.CharField(max_length=100)
    schedule = models.CharField(max_length=100, help_text="e.g., MWF 10:00-11:00")
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.code} - {self.name}"
    
    @property
    def current_enrollment(self):
        return self.enrollments.filter(status='ENROLLED').count()
    
    @property
    def is_full(self):
        return self.current_enrollment >= self.max_enrollment

class Enrollment(models.Model):
    STATUS_CHOICES = [
        ('PENDING', 'Pending'),
        ('ENROLLED', 'Enrolled'),
        ('DROPPED', 'Dropped'),
        ('COMPLETED', 'Completed'),
    ]
    
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='enrollments')
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='enrollments')
    enrollment_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='PENDING')
    grade = models.CharField(max_length=2, blank=True, null=True, help_text="A, B, C, D, F")
    
    class Meta:
        unique_together = ('student', 'course')
    
    def __str__(self):
        return f"{self.student.student_id} - {self.course.code} ({self.status})"

# serializers.py
from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Department, Student, Course, Enrollment

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name']

class DepartmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Department
        fields = '__all__'

class StudentSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    department_name = serializers.CharField(source='department.name', read_only=True)
    
    class Meta:
        model = Student
        fields = '__all__'

class StudentCreateSerializer(serializers.ModelSerializer):
    # User fields
    username = serializers.CharField(write_only=True)
    email = serializers.EmailField(write_only=True)
    first_name = serializers.CharField(write_only=True)
    last_name = serializers.CharField(write_only=True)
    password = serializers.CharField(write_only=True, min_length=8)
    
    class Meta:
        model = Student
        fields = ['student_id', 'phone', 'date_of_birth', 'address', 'department',
                 'username', 'email', 'first_name', 'last_name', 'password']
    
    def create(self, validated_data):
        # Extract user data
        user_data = {
            'username': validated_data.pop('username'),
            'email': validated_data.pop('email'),
            'first_name': validated_data.pop('first_name'),
            'last_name': validated_data.pop('last_name'),
            'password': validated_data.pop('password'),
        }
        
        # Create user
        user = User.objects.create_user(**user_data)
        
        # Create student
        student = Student.objects.create(user=user, **validated_data)
        return student

class CourseSerializer(serializers.ModelSerializer):
    department_name = serializers.CharField(source='department.name', read_only=True)
    current_enrollment = serializers.ReadOnlyField()
    is_full = serializers.ReadOnlyField()
    
    class Meta:
        model = Course
        fields = '__all__'

class EnrollmentSerializer(serializers.ModelSerializer):
    student_name = serializers.CharField(source='student.user.get_full_name', read_only=True)
    student_id = serializers.CharField(source='student.student_id', read_only=True)
    course_name = serializers.CharField(source='course.name', read_only=True)
    course_code = serializers.CharField(source='course.code', read_only=True)
    
    class Meta:
        model = Enrollment
        fields = '__all__'

class EnrollmentCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Enrollment
        fields = ['course']
    
    def validate(self, data):
        course = data['course']
        student = self.context['request'].user.student
        
        # Check if course is full
        if course.is_full:
            raise serializers.ValidationError("Course is full")
        
        # Check if student is already enrolled
        if Enrollment.objects.filter(student=student, course=course).exists():
            raise serializers.ValidationError("Already enrolled in this course")
        
        return data
    
    def create(self, validated_data):
        student = self.context['request'].user.student
        return Enrollment.objects.create(student=student, **validated_data)

# views.py
from rest_framework import generics, status, permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from django.db.models import Q
from django.shortcuts import get_object_or_404
from .models import Department, Student, Course, Enrollment
from .serializers import *

class DepartmentListView(generics.ListCreateAPIView):
    queryset = Department.objects.all()
    serializer_class = DepartmentSerializer
    permission_classes = [permissions.IsAuthenticated]

class DepartmentDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Department.objects.all()
    serializer_class = DepartmentSerializer
    permission_classes = [permissions.IsAuthenticated]

class StudentListView(generics.ListAPIView):
    queryset = Student.objects.select_related('user', 'department').all()
    serializer_class = StudentSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        queryset = super().get_queryset()
        department = self.request.query_params.get('department', None)
        search = self.request.query_params.get('search', None)
        
        if department:
            queryset = queryset.filter(department_id=department)
        
        if search:
            queryset = queryset.filter(
                Q(user__first_name__icontains=search) |
                Q(user__last_name__icontains=search) |
                Q(student_id__icontains=search)
            )
        
        return queryset

class StudentCreateView(generics.CreateAPIView):
    serializer_class = StudentCreateSerializer
    permission_classes = [permissions.IsAdminUser]

class StudentDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Student.objects.select_related('user', 'department').all()
    serializer_class = StudentSerializer
    permission_classes = [permissions.IsAuthenticated]

class CourseListView(generics.ListCreateAPIView):
    queryset = Course.objects.select_related('department').all()
    serializer_class = CourseSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        queryset = super().get_queryset()
        department = self.request.query_params.get('department', None)
        semester = self.request.query_params.get('semester', None)
        year = self.request.query_params.get('year', None)
        available_only = self.request.query_params.get('available', None)
        
        if department:
            queryset = queryset.filter(department_id=department)
        
        if semester:
            queryset = queryset.filter(semester=semester)
        
        if year:
            queryset = queryset.filter(year=year)
        
        if available_only:
            queryset = queryset.filter(is_active=True)
        
        return queryset

class CourseDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Course.objects.select_related('department').all()
    serializer_class = CourseSerializer
    permission_classes = [permissions.IsAuthenticated]

class EnrollmentListView(generics.ListAPIView):
    serializer_class = EnrollmentSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        user = self.request.user
        
        # If user is admin, show all enrollments
        if user.is_staff:
            queryset = Enrollment.objects.select_related('student__user', 'course').all()
            
            # Filter by student if specified
            student_id = self.request.query_params.get('student', None)
            if student_id:
                queryset = queryset.filter(student_id=student_id)
            
            # Filter by course if specified
            course_id = self.request.query_params.get('course', None)
            if course_id:
                queryset = queryset.filter(course_id=course_id)
            
            return queryset
        
        # If user is student, show only their enrollments
        try:
            student = user.student
            return Enrollment.objects.filter(student=student).select_related('course')
        except:
            return Enrollment.objects.none()

@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def enroll_course(request):
    """Enroll current user (student) in a course"""
    try:
        student = request.user.student
    except:
        return Response(
            {'error': 'User is not a student'}, 
            status=status.HTTP_400_BAD_REQUEST
        )
    
    serializer = EnrollmentCreateSerializer(data=request.data, context={'request': request})
    if serializer.is_valid():
        enrollment = serializer.save()
        response_serializer = EnrollmentSerializer(enrollment)
        return Response(response_serializer.data, status=status.HTTP_201_CREATED)
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def drop_course(request, enrollment_id):
    """Drop a course enrollment"""
    try:
        student = request.user.student
        enrollment = get_object_or_404(Enrollment, id=enrollment_id, student=student)
        
        if enrollment.status == 'COMPLETED':
            return Response(
                {'error': 'Cannot drop completed course'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        enrollment.status = 'DROPPED'
        enrollment.save()
        
        serializer = EnrollmentSerializer(enrollment)
        return Response(serializer.data)
        
    except Student.DoesNotExist:
        return Response(
            {'error': 'User is not a student'}, 
            status=status.HTTP_400_BAD_REQUEST
        )

@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def student_dashboard(request):
    """Get student dashboard data"""
    try:
        student = request.user.student
        enrollments = Enrollment.objects.filter(student=student).select_related('course')
        
        dashboard_data = {
            'student_info': StudentSerializer(student).data,
            'total_courses': enrollments.count(),
            'active_enrollments': enrollments.filter(status='ENROLLED').count(),
            'completed_courses': enrollments.filter(status='COMPLETED').count(),
            'current_enrollments': EnrollmentSerializer(
                enrollments.filter(status='ENROLLED'), many=True
            ).data,
        }
        
        return Response(dashboard_data)
        
    except Student.DoesNotExist:
        return Response(
            {'error': 'User is not a student'}, 
            status=status.HTTP_400_BAD_REQUEST
        )

# urls.py
from django.urls import path
from . import views

urlpatterns = [
    # Departments
    path('departments/', views.DepartmentListView.as_view(), name='department-list'),
    path('departments/<int:pk>/', views.DepartmentDetailView.as_view(), name='department-detail'),
    
    # Students
    path('students/', views.StudentListView.as_view(), name='student-list'),
    path('students/create/', views.StudentCreateView.as_view(), name='student-create'),
    path('students/<int:pk>/', views.StudentDetailView.as_view(), name='student-detail'),
    path('students/dashboard/', views.student_dashboard, name='student-dashboard'),
    
    # Courses
    path('courses/', views.CourseListView.as_view(), name='course-list'),
    path('courses/<int:pk>/', views.CourseDetailView.as_view(), name='course-detail'),
    
    # Enrollments
    path('enrollments/', views.EnrollmentListView.as_view(), name='enrollment-list'),
    path('enrollments/enroll/', views.enroll_course, name='enroll-course'),
    path('enrollments/<int:enrollment_id>/drop/', views.drop_course, name='drop-course'),
]

# admin.py
from django.contrib import admin
from .models import Department, Student, Course, Enrollment

@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = ['code', 'name', 'created_at']
    search_fields = ['name', 'code']

@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ['student_id', 'get_full_name', 'department', 'enrollment_date', 'is_active']
    list_filter = ['department', 'is_active', 'enrollment_date']
    search_fields = ['student_id', 'user__first_name', 'user__last_name', 'user__email']
    
    def get_full_name(self, obj):
        return obj.user.get_full_name()
    get_full_name.short_description = 'Full Name'

@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ['code', 'name', 'department', 'credits', 'semester', 'year', 'current_enrollment', 'max_enrollment']
    list_filter = ['department', 'semester', 'year', 'is_active']
    search_fields = ['name', 'code', 'instructor']
    
    def current_enrollment(self, obj):
        return obj.current_enrollment
    current_enrollment.short_description = 'Current Enrollment'

@admin.register(Enrollment)
class EnrollmentAdmin(admin.ModelAdmin):
    list_display = ['student', 'course', 'status', 'enrollment_date', 'grade']
    list_filter = ['status', 'course__semester', 'course__year', 'enrollment_date']
    search_fields = ['student__student_id', 'student__user__first_name', 'course__name', 'course__code']

# settings.py additions
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'rest_framework.authtoken',  # For token authentication
    'enrollment',  # Your app name
]

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.TokenAuthentication',
        'rest_framework.authentication.SessionAuthentication',
    ],
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
    ],
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 20
}

# tests.py
from django.test import TestCase
from django.contrib.auth.models import User
from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from datetime import date
from .models import Department, Student, Course, Enrollment

class EnrollmentSystemTestCase(APITestCase):
    def setUp(self):
        # Create test department
        self.department = Department.objects.create(
            name='Computer Science',
            code='CS',
            description='Computer Science Department'
        )
        
        # Create test user and student
        self.user = User.objects.create_user(
            username='teststudent',
            email='test@example.com',
            first_name='Test',
            last_name='Student',
            password='testpass123'
        )
        
        self.student = Student.objects.create(
            user=self.user,
            student_id='ST001',
            phone='1234567890',
            date_of_birth=date(2000, 1, 1),
            address='Test Address',
            department=self.department
        )
        
        # Create test course
        self.course = Course.objects.create(
            name='Introduction to Programming',
            code='CS101',
            description='Basic programming',
            credits=3,
            department=self.department,
            semester='FALL',
            max_enrollment=2,
            instructor='Dr. Smith',
            schedule='MWF 10:00-11:00'
        )
        
        # Admin user
        self.admin_user = User.objects.create_user(
            username='admin',
            password='adminpass',
            is_staff=True
        )

    def test_student_enrollment(self):
        """Test student can enroll in course"""
        self.client.force_authenticate(user=self.user)
        
        url = reverse('enroll-course')
        data = {'course': self.course.id}
        
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        
        # Verify enrollment created
        enrollment = Enrollment.objects.get(student=self.student, course=self.course)
        self.assertEqual(enrollment.status, 'PENDING')

    def test_course_full_enrollment(self):
        """Test enrollment fails when course is full"""
        # Fill up the course
        for i in range(2):
            user = User.objects.create_user(username=f'student{i}', password='pass')
            student = Student.objects.create(
                user=user,
                student_id=f'ST{i+2:03d}',
                phone='1234567890',
                date_of_birth=date(2000, 1, 1),
                address='Address',
                department=self.department
            )
            Enrollment.objects.create(student=student, course=self.course, status='ENROLLED')
        
        # Try to enroll when full
        self.client.force_authenticate(user=self.user)
        url = reverse('enroll-course')
        data = {'course': self.course.id}
        
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('Course is full', response.data['non_field_errors'][0])

    def test_student_dashboard(self):
        """Test student dashboard endpoint"""
        # Create an enrollment
        enrollment = Enrollment.objects.create(
            student=self.student,
            course=self.course,
            status='ENROLLED'
        )
        
        self.client.force_authenticate(user=self.user)
        url = reverse('student-dashboard')
        
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['total_courses'], 1)
        self.assertEqual(response.data['active_enrollments'], 1)

    def test_drop_course(self):
        """Test student can drop a course"""
        enrollment = Enrollment.objects.create(
            student=self.student,
            course=self.course,
            status='ENROLLED'
        )
        
        self.client.force_authenticate(user=self.user)
        url = reverse('drop-course', kwargs={'enrollment_id': enrollment.id})
        
        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        enrollment.refresh_from_db()
        self.assertEqual(enrollment.status, 'DROPPED')

# management/commands/create_sample_data.py
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from enrollment.models import Department, Student, Course, Enrollment
import random
from datetime import date

class Command(BaseCommand):
    help = 'Create sample data for student enrollment system'
    
    def handle(self, *args, **options):
        # Create departments
        departments = [
            {'name': 'Computer Science', 'code': 'CS', 'description': 'Computer Science Department'},
            {'name': 'Mathematics', 'code': 'MATH', 'description': 'Mathematics Department'},
            {'name': 'Physics', 'code': 'PHYS', 'description': 'Physics Department'},
        ]
        
        for dept_data in departments:
            dept, created = Department.objects.get_or_create(
                code=dept_data['code'],
                defaults=dept_data
            )
            if created:
                self.stdout.write(f'Created department: {dept.name}')
        
        # Create sample courses
        cs_dept = Department.objects.get(code='CS')
        courses = [
            {
                'name': 'Introduction to Programming',
                'code': 'CS101',
                'description': 'Basic programming concepts',
                'credits': 3,
                'department': cs_dept,
                'semester': 'FALL',
                'instructor': 'Dr. Smith',
                'schedule': 'MWF 10:00-11:00'
            },
            {
                'name': 'Data Structures',
                'code': 'CS201',
                'description': 'Data structures and algorithms',
                'credits': 4,
                'department': cs_dept,
                'semester': 'SPRING',
                'instructor': 'Dr. Johnson',
                'schedule': 'TTh 14:00-16:00'
            }
        ]
        
        for course_data in courses:
            course, created = Course.objects.get_or_create(
                code=course_data['code'],
                defaults=course_data
            )
            if created:
                self.stdout.write(f'Created course: {course.name}')
        
        self.stdout.write(self.style.SUCCESS('Sample data created successfully!'))