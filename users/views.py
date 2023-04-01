from django.db.models import Sum, Count
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.views import LoginView, LogoutView
from django.views.generic import CreateView
from django.urls import reverse_lazy

from core.models import Question, QuestionView
from users.forms import UserCreateForm, ProfileForm
from users.models import User


# Create your views here.
class CustomLoginView(LoginView):
    template_name = 'auth/sign_in.html'
    redirect_authenticated_user = True
    next_page = reverse_lazy('core:home')


class CustomLogoutView(LogoutView):
    next_page = reverse_lazy('core:home')


class UserSignUpView(CreateView):
    template_name = 'auth/sign_up.html'
    form_class = UserCreateForm
    success_url = reverse_lazy('core:home')


def user_page(request):
    user = get_object_or_404(User, username=request.user.username)
    questions = Question.objects.filter(user=user)
    total_views = QuestionView.objects.filter(user=user).count()
    answers_count = Question.objects.filter(answer__user=user).count()

    context = {
        'user': user,
        'questions': questions,
        'answers_count': answers_count,
        'total_views': total_views
    }
    return render(request, 'user_page.html', context)


def edit_profile(request):
    profile = request.user.profile
    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('users:profile')
    else:
        form = ProfileForm(instance=profile)
    return render(request, 'profile_edit.html', {'form': form})
