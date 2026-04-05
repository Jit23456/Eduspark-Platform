from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect, render

from .models import Course


def course_list(request):
    grade_filter = request.GET.get('grade', '')
    subject_filter = request.GET.get('subject', '')

    courses = Course.objects.all()
    if grade_filter.isdigit():
        courses = courses.filter(class_grade=int(grade_filter))
    if subject_filter:
        courses = courses.filter(subject=subject_filter)

    grades = list(range(1, 11))
    return render(
        request,
        'courses/course_list.html',
        {
            'courses': courses,
            'grades': grades,
            'grade_filter': grade_filter,
            'subject_filter': subject_filter,
        },
    )


def course_detail(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    if request.method == 'POST' and 'enroll' in request.POST:
        messages.success(request, 'You have been enrolled in this course.')
        return redirect('course_detail', course_id=course.id)

    return render(
        request,
        'courses/course_detail.html',
        {
            'course': course,
            'chapters': [],
            'is_enrolled': False,
        },
    )


def video_lecture(request, video_id):
    return redirect('course_list')
