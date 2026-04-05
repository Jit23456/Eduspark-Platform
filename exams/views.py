from django.shortcuts import get_object_or_404, redirect, render

from .models import Exam, ExamAnswer, ExamAttempt


def exam_list(request):
    exams = Exam.objects.prefetch_related('questions').all()
    attempted_ids = request.session.get('attempted_exams', [])
    return render(request, 'exams/exam_list.html', {'exams': exams, 'attempted_ids': attempted_ids})


def take_exam(request, exam_id):
    exam = get_object_or_404(Exam, id=exam_id)
    questions = exam.questions.all()

    if request.method == 'POST':
        correct_answers = 0
        for question in questions:
            selected_answer = request.POST.get(f'q_{question.id}', '').strip().upper()
            if selected_answer == question.correct_answer:
                correct_answers += 1

        attempt = ExamAttempt.objects.create(
            exam=exam,
            user=request.user if request.user.is_authenticated else None,
            correct_answers=correct_answers,
            total_questions=questions.count(),
        )

        for question in questions:
            selected_answer = request.POST.get(f'q_{question.id}', '').strip().upper()
            ExamAnswer.objects.create(
                attempt=attempt,
                question=question,
                selected_answer=selected_answer,
            )

        attempted_ids = request.session.get('attempted_exams', [])
        if exam.id not in attempted_ids:
            attempted_ids.append(exam.id)
            request.session['attempted_exams'] = attempted_ids

        request.session[f'exam_{exam.id}_attempt_id'] = attempt.id
        return redirect('exam_results', exam_id=exam.id)

    return render(request, 'exams/take_exam.html', {
        'exam': exam,
        'questions': questions,
    })


def exam_results(request, exam_id):
    attempt_id = request.session.get(f'exam_{exam_id}_attempt_id')
    attempt = get_object_or_404(ExamAttempt, id=attempt_id, exam_id=exam_id)
    answers = attempt.answers.select_related('question').all()
    return render(request, 'exams/results.html', {'attempt': attempt, 'answers': answers})
