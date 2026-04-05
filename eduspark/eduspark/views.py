from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.shortcuts import redirect, render
from django import forms

from eduspark.courses.models import Course


class SignUpForm(UserCreationForm):
    first_name = forms.CharField(max_length=30, required=True)
    last_name = forms.CharField(max_length=30, required=True)
    email = forms.EmailField(required=True)
    phone = forms.CharField(max_length=20, required=False)
    class_grade = forms.ChoiceField(
        choices=[(str(i), f'Class {i}') for i in range(1, 11)],
        required=False,
    )

    class Meta:
        model = User
        fields = [
            'first_name',
            'last_name',
            'username',
            'email',
            'phone',
            'class_grade',
            'password1',
            'password2',
        ]


def home(request):
    if not Course.objects.exists():
        sample_courses = [
            Course(
                title='Foundation Mathematics for Class 6',
                description='Build strong basics with video lessons and practice exercises.',
                subject='mathematics',
                class_grade=6,
            ),
            Course(
                title='Science Explorer: Class 7',
                description='Discover science with fun experiments and concept videos.',
                subject='science',
                class_grade=7,
            ),
            Course(
                title='English Grammar Essentials',
                description='Improve reading and writing with simple English lessons.',
                subject='english',
                class_grade=8,
            ),
            Course(
                title='Computer Basics for Kids',
                description='Learn computing fundamentals with interactive examples.',
                subject='computer',
                class_grade=5,
            ),
        ]
        Course.objects.bulk_create(sample_courses)

    courses = Course.objects.all()[:6]
    return render(request, 'home.html', {'courses': courses, 'feat': []})


def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.email = form.cleaned_data['email']
            user.first_name = form.cleaned_data['first_name']
            user.last_name = form.cleaned_data['last_name']
            user.save()
            login(request, user)
            messages.success(request, 'Your account has been created successfully.')
            return redirect('dashboard')
    else:
        form = SignUpForm()

    return render(request, 'accounts/signup.html', {'form': form})


@login_required
def dashboard(request):
    return render(
        request,
        'courses/dashboard.html',
        {
            'enrollments': Course.objects.none(),
            'all_courses': Course.objects.all(),
            'recent_exams': [],
            'profile': None,
        },
    )
