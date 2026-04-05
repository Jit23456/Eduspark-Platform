from django.shortcuts import render


def exam_list(request):
    return render(request, 'exams/exam_list.html', {'exams': [], 'attempted_ids': []})
