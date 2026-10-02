from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.contrib import messages
from django.core.paginator import Paginator
from .models import Course, Category, Enrollment, Testimonial
from .forms import CourseForm, SearchForm, TestimonialForm, CategoryForm

def home(request):
    courses = Course.objects.all()
    testimonials = Testimonial.objects.filter(is_active=True)[:3]
    
    paginator = Paginator(courses, 9)  # Show 9 courses per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'courses': page_obj,
        'testimonials': testimonials,
        'category': None,
    }
    return render(request, 'courses/home.html', context)

def course_detail(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    
    # Get similar courses based on category
    similar_courses = Course.objects.filter(category=course.category).exclude(id=course.id)[:3]
    
    # Check if user is enrolled
    is_enrolled = False
    if request.user.is_authenticated:
        is_enrolled = Enrollment.objects.filter(user=request.user, course=course).exists()
   
    context = {
        'course': course,
        'similar_courses': similar_courses,
        'is_enrolled': is_enrolled,
    }
    return render(request, 'courses/course_detail.html', context)

@login_required
def course_add(request):
    if request.method == 'POST':
        form = CourseForm(request.POST)
        if form.is_valid():
            course = form.save(commit=False)
            course.created_by = request.user
            course.save()
            messages.success(request, 'Course added successfully!')
            return redirect('course_detail', course_id=course.id)
    else:
        form = CourseForm()
    
    context = {
        'form': form,
        'title': 'Add New Course',
    }
    return render(request, 'courses/course_form.html', context)

@login_required
def course_edit(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    
    # Check if the user is the creator of the course
    if course.created_by != request.user:
        messages.error(request, 'You do not have permission to edit this course.')
        return redirect('course_detail', course_id=course.id)
    
    if request.method == 'POST':
        form = CourseForm(request.POST, instance=course)
        if form.is_valid():
            form.save()
            messages.success(request, 'Course updated successfully!')
            return redirect('course_detail', course_id=course.id)
    else:
        form = CourseForm(instance=course)
    
    context = {
        'form': form,
        'title': 'Edit Course',
        'course': course,
    }
    return render(request, 'courses/course_form.html', context)

@login_required
def course_delete(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    
    # Check if the user is the creator of the course
    if course.created_by != request.user:
        messages.error(request, 'You do not have permission to delete this course.')
        return redirect('course_detail', course_id=course.id)
    
    if request.method == 'POST':
        course.delete()
        messages.success(request, 'Course deleted successfully!')
        return redirect('home')
    
    context = {
        'course': course,
    }
    return render(request, 'courses/course_delete.html', context)

def category_filter(request, category_slug):
    category = get_object_or_404(Category, slug=category_slug)
    courses = Course.objects.filter(category=category)
    
    paginator = Paginator(courses, 9)  # Show 9 courses per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'category': category,
        'courses': page_obj,
    }
    return render(request, 'courses/home.html', context)

def search(request):
    query = request.GET.get('q', '')
    
    if query:
        courses = Course.objects.filter(
            Q(title__icontains=query) | 
            Q(description__icontains=query) | 
            Q(trainer_name__icontains=query)
        )
    else:
        courses = Course.objects.all()
    
    paginator = Paginator(courses, 9)  # Show 9 courses per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'courses': page_obj,
        'query': query,
    }
    return render(request, 'courses/search_results.html', context)

@login_required
def enroll_course(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    
    # Check if already enrolled
    if Enrollment.objects.filter(user=request.user, course=course).exists():
        messages.info(request, 'You are already enrolled in this course.')
    else:
        Enrollment.objects.create(user=request.user, course=course)
        messages.success(request, f'Successfully enrolled in {course.title}!')
    
    return redirect('course_detail', course_id=course.id)

def categories(request):
    categories_list = Category.objects.all()
    
    context = {
        'categories': categories_list,
    }
    return render(request, 'courses/categories.html', context)

def contact(request):
    return render(request, 'courses/contact.html')

@login_required
def add_category(request):
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Category added successfully!')
            return redirect('add_category')  # Or redirect to a category list if you have one
    else:
        form = CategoryForm()
    return render(request, 'courses/category_form.html', {'form': form})

@login_required
def add_testimonial(request):
    if request.method == 'POST':
        form = TestimonialForm(request.POST)
        if form.is_valid():
            testimonial = form.save(commit=False)
            testimonial.save()
            messages.success(request, 'Thank you for your testimonial!')
            return redirect('home')
    else:
        form = TestimonialForm()
    
    context = {
        'form': form,
    }
    return render(request, 'courses/testimonial_form.html', context)
