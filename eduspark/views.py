import json

from django import forms
from django.conf import settings
from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib.auth.views import LoginView
from django.http import JsonResponse
from django.shortcuts import redirect, render
from django.utils.text import slugify
from django.views.decorators.http import require_GET, require_POST

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


class CustomLoginView(LoginView):
    template_name = 'accounts/login.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['google_client_id'] = settings.GOOGLE_CLIENT_ID
        context['google_login_enabled'] = settings.GOOGLE_LOGIN_ENABLED
        return context


def build_unique_username(email, first_name='', last_name=''):
    candidates = [
        slugify(f'{first_name} {last_name}').replace('-', ''),
        slugify(email.split('@')[0]).replace('-', ''),
        'student',
    ]
    base = next((candidate for candidate in candidates if candidate), 'student')
    username = base[:120]
    suffix = 1
    while User.objects.filter(username=username).exists():
        suffix += 1
        username = f'{base[:110]}{suffix}'
    return username


def build_mira_response(question):
    from django.conf import settings
    normalized = (question or '').strip().lower()[:300]

    if settings.MIRA_AI_ENABLED:
        try:
            import openai
            client = openai.OpenAI(api_key=settings.OPENAI_API_KEY)
            response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are Mira, an AI assistant for EduSpark, a secure educational platform. Help users with courses, materials, login, and navigation. Keep responses helpful, secure, and focused on education. Do not share sensitive information."},
                    {"role": "user", "content": question}
                ],
                max_tokens=200
            )
            answer = response.choices[0].message.content.strip()
            return {
                'answer': answer,
                'suggestions': [
                    'How do I access Class 10 materials?',
                    'How to sign in?',
                    'Where are my courses?',
                ],
                'link': '',
            }
        except Exception as e:
            # Fallback to rule-based
            pass

    # Rule-based fallback
    class_10_course = (
        Course.objects.filter(class_grade=10, materials__isnull=False)
        .prefetch_related('materials')
        .distinct()
        .first()
    )

    if not normalized:
        return {
            'answer': (
                'I am Mira. I can help with courses, Class 10 materials, login, '
                'exams, and where to find things on EduSpark.'
            ),
            'suggestions': [
                'How do I open the Class 10 PDF?',
                'How do I sign in with Google?',
                'Where can I find my courses?',
            ],
            'link': '',
        }

    if any(keyword in normalized for keyword in ['pdf', 'thermodynamics', 'class 10', 'material', 'notes']):
        return {
            'answer': (
                'Open the Class 10 course material from the course page. The PDF is '
                'served in a protected viewer for signed-in users and is configured '
                'for in-browser reading instead of direct downloading.'
            ),
            'suggestions': [
                'Take me to Class 10 courses',
                'How is the PDF protected?',
                'How do I log in first?',
            ],
            'link': f'/courses/{class_10_course.id}/' if class_10_course else '/courses/?grade=10',
        }

    if any(keyword in normalized for keyword in ['google', 'sign in', 'login', 'log in', 'account']):
        return {
            'answer': (
                'Use the Google button on the login page if it is shown. EduSpark '
                'verifies the Google identity token on the server before creating '
                'or signing in the account.'
            ),
            'suggestions': [
                'Open login page',
                'What if the Google button is missing?',
                'Can I still use username and password?',
            ],
            'link': '/login/',
        }

    if any(keyword in normalized for keyword in ['exam', 'test', 'quiz']):
        return {
            'answer': (
                'Your exams are available from the Exams section after login. If '
                'you are signed in, you can also reach them from the dashboard.'
            ),
            'suggestions': [
                'Open exams',
                'Open dashboard',
                'Show me courses',
            ],
            'link': '/exams/',
        }

    if any(keyword in normalized for keyword in ['dashboard', 'progress', 'profile']):
        return {
            'answer': (
                'Your dashboard is the best place to track learning activity and '
                'quickly jump back into courses and exams.'
            ),
            'suggestions': [
                'Open dashboard',
                'Show Class 10 courses',
                'How do I sign in?',
            ],
            'link': '/dashboard/',
        }

    return {
        'answer': (
            'I can guide you to courses, secure study materials, login, Google '
            'sign-in, dashboard, and exams. Try asking about Class 10, PDF access, or login.'
        ),
        'suggestions': [
            'How do I open the Class 10 PDF?',
            'Where is the dashboard?',
            'How do I use Google login?',
        ],
        'link': '/courses/',
    }


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

    return render(
        request,
        'accounts/signup.html',
        {
            'form': form,
            'google_client_id': settings.GOOGLE_CLIENT_ID,
            'google_login_enabled': settings.GOOGLE_LOGIN_ENABLED,
        },
    )


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


@require_POST
def google_login(request):
    if not settings.GOOGLE_LOGIN_ENABLED:
        return JsonResponse(
            {'ok': False, 'message': 'Google login is not configured yet.'},
            status=400,
        )

    try:
        payload = json.loads(request.body.decode('utf-8'))
    except (json.JSONDecodeError, UnicodeDecodeError):
        return JsonResponse({'ok': False, 'message': 'Invalid login request.'}, status=400)

    credential = (payload.get('credential') or '').strip()
    if not credential:
        return JsonResponse({'ok': False, 'message': 'Missing Google credential.'}, status=400)

    try:
        from google.auth.transport import requests as google_requests
        from google.oauth2 import id_token
    except ImportError:
        return JsonResponse(
            {'ok': False, 'message': 'Google login dependency is not installed.'},
            status=503,
        )

    try:
        token_info = id_token.verify_oauth2_token(
            credential,
            google_requests.Request(),
            settings.GOOGLE_CLIENT_ID,
        )
    except Exception:
        return JsonResponse({'ok': False, 'message': 'Google verification failed.'}, status=400)

    email = (token_info.get('email') or '').strip().lower()
    if not email or not token_info.get('email_verified'):
        return JsonResponse(
            {'ok': False, 'message': 'Google account email is not verified.'},
            status=400,
        )

    first_name = (token_info.get('given_name') or '').strip()
    last_name = (token_info.get('family_name') or '').strip()

    user = User.objects.filter(email__iexact=email).first()
    if user is None:
        user = User.objects.create_user(
            username=build_unique_username(email, first_name, last_name),
            email=email,
            first_name=first_name,
            last_name=last_name,
        )
        user.set_unusable_password()
        user.save(update_fields=['password'])
    else:
        updated_fields = []
        if first_name and user.first_name != first_name:
            user.first_name = first_name
            updated_fields.append('first_name')
        if last_name and user.last_name != last_name:
            user.last_name = last_name
            updated_fields.append('last_name')
        if updated_fields:
            user.save(update_fields=updated_fields)

    login(request, user, backend='django.contrib.auth.backends.ModelBackend')
    return JsonResponse({'ok': True, 'redirect_url': settings.LOGIN_REDIRECT_URL})


@require_GET
def mira_assistant(request):
    return JsonResponse(build_mira_response(request.GET.get('q', '')))
