from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('course/<int:course_id>/', views.course_detail, name='course_detail'),
    path('course/add/', views.course_add, name='course_add'),
    path('course/<int:course_id>/edit/', views.course_edit, name='course_edit'),
    path('course/<int:course_id>/delete/', views.course_delete, name='course_delete'),
    path('course/<int:course_id>/enroll/', views.enroll_course, name='enroll_course'),
    path('category/<slug:category_slug>/', views.category_filter, name='category_filter'),
    path('categories/', views.categories, name='categories'),
    path('add/category/', views.add_category, name='add_category'),
    path('search/', views.search, name='search'),
    path('contact/', views.contact, name='contact'),
    path('testimonial/add/', views.add_testimonial, name='add_testimonial'),
]
