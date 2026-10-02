from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from .models import Course, Category

class CourseModelTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpassword'
        )
        self.category = Category.objects.create(
            name='Test Category',
            slug='test-category'
        )
        
    def test_course_creation(self):
        course = Course.objects.create(
            title='Test Course',
            slug='test-course',
            description='This is a test course',
            category=self.category,
            trainer_name='Test Trainer',
            price=1000,
            duration='3 months',
            created_by=self.user
        )
        self.assertEqual(course.title, 'Test Course')
        self.assertEqual(course.created_by, self.user)
        self.assertEqual(str(course), 'Test Course')

class CourseViewTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpassword'
        )
        self.category = Category.objects.create(
            name='Test Category',
            slug='test-category'
        )
        self.course = Course.objects.create(
            title='Test Course',
            slug='test-course',
            description='This is a test course',
            category=self.category,
            trainer_name='Test Trainer',
            price=1000,
            duration='3 months',
            created_by=self.user
        )
        
    def test_home_view(self):
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test Course')
        
    def test_course_detail_view(self):
        response = self.client.get(reverse('course_detail', args=[self.course.id]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test Course')
        self.assertContains(response, 'Test Trainer')
