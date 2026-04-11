import mimetypes
import os

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import FileResponse, Http404
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.clickjacking import xframe_options_sameorigin

from .models import Course, StudyMaterial, Video


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

    chapters = course.chapters.prefetch_related('videos', 'assignments').all()
    materials = course.materials.select_related('chapter').all()
    return render(
        request,
        'courses/course_detail.html',
        {
            'course': course,
            'chapters': chapters,
            'materials': materials,
            'is_enrolled': False,
        },
    )


def video_lecture(request, video_id):
    video = get_object_or_404(Video, id=video_id)
    chapter = video.chapter
    other_videos = chapter.videos.exclude(id=video.id)
    return render(
        request,
        'courses/video_lecture.html',
        {
            'video': video,
            'chapter': chapter,
            'other_videos': other_videos,
        },
    )


@login_required
def material_viewer(request, material_id):
    material = get_object_or_404(
        StudyMaterial.objects.select_related('course', 'chapter'),
        id=material_id,
    )
    return render(
        request,
        'courses/material_viewer.html',
        {
            'material': material,
        },
    )


@login_required
@xframe_options_sameorigin
def material_stream(request, material_id):
    material = get_object_or_404(
        StudyMaterial.objects.select_related('course', 'chapter'),
        id=material_id,
    )
    if material.requires_login and not request.user.is_authenticated:
        raise Http404('Material not found.')
    if not material.file or not material.file.name:
        raise Http404('Material file is missing.')

    file_path = material.file.path
    if not os.path.exists(file_path):
        raise Http404('Material file is missing.')

    content_type, _ = mimetypes.guess_type(file_path)
    response = FileResponse(open(file_path, 'rb'), content_type=content_type or 'application/octet-stream')
    response['Content-Disposition'] = f'inline; filename="{material.filename or "material.pdf"}"'
    response['Cache-Control'] = 'private, no-store, no-cache, must-revalidate, max-age=0'
    response['Pragma'] = 'no-cache'
    response['Expires'] = '0'
    response['X-Content-Type-Options'] = 'nosniff'
    response['Referrer-Policy'] = 'same-origin'
    response['Cross-Origin-Resource-Policy'] = 'same-origin'
    response['Content-Security-Policy'] = "frame-ancestors 'self';"
    response['Accept-Ranges'] = 'none'
    return response
