from django.db.models import Count
from django.shortcuts import render
from django.http import HttpRequest, HttpResponse
from django.views.generic import ListView, DetailView, CreateView, DeleteView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from core.models import Question, QuestionView
from core.forms import QuestionCreateForm
from django.urls import reverse_lazy, reverse
from typing import Dict, Any


from users.models import User


def home_view(request: HttpRequest) -> HttpResponse:
    questions = Question.objects.annotate(view_amount=Count('view_amount'))
    return render(request, 'home.html', context={
        'questions': questions,
    })


class HomeView(ListView):
    template_name = 'home.html'
    context_object_name = 'questions'
    ordering = ['-create_time']
    paginate_by = 5

    def get_queryset(self):
        query = self.request.GET.get('q')

        if query:
            if query.startswith('tag:'):
                tag = query[4:]
                queryset = Question.objects.filter(tags__title=tag)
            elif query.startswith('user:'):
                username = query[5:]
                queryset = Question.objects.filter(user__username=username)
            else:
                queryset = Question.objects.filter(title__icontains=query)
        else:
            queryset = Question.objects.all()

        ordering = self.get_ordering()
        if ordering:
            if isinstance(ordering, str):
                ordering = (ordering,)
            queryset = queryset.order_by(*ordering)

        return queryset


def questions_by_tag(request, tag):
    questions = Question.objects.filter(tags__title=tag)
    context = {
        'object_list': questions,
        'tag': tag,
    }
    return render(request, 'home.html', context)


class QuestionDetailView(DetailView):
    template_name = 'question_detail.html'
    model = Question

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        user = request.user

        # check if the user is authenticated
        if user.is_authenticated:
            # check if the question has already been viewed by the user
            question_viewed = QuestionView.objects.filter(question=self.object, user=user).exists()

            # if the question has not been viewed, add it to the views
            if not question_viewed:
                QuestionView.objects.create(question=self.object, user=user)

        context = self.get_context_data(object=self.object)
        return self.render_to_response(context)


class QuestionCreateView(LoginRequiredMixin, CreateView):
    model = Question
    form_class = QuestionCreateForm
    template_name = 'question_create.html'
    success_url = reverse_lazy('core:home')

    def get_form_kwargs(self) -> Dict[str, Any]:
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def form_valid(self, form):
        self.object = form.save()
        self.object.tags.add(
            *[tag.id for tag in form.cleaned_data['tags']]
        )
        return super().form_valid(form)


class QuestonDeleteView(LoginRequiredMixin, DeleteView):
    model = Question
    template_name = 'question_delete.html'
    success_url = reverse_lazy('core:home')

    def get_queryset(self):
        return Question.objects.filter(user=self.request.user)


class QuestionUpdateView(LoginRequiredMixin, UpdateView):
    model = Question
    template_name = 'question_update.html'
    fields = ['tags', 'title', 'text']

    def get_success_url(self) -> str:
        return reverse('core:question-detail', kwargs={'pk': self.get_object().pk})

    def get_queryset(self):
        return Question.objects.filter(user=self.request.user)


def about_us_view(request: HttpRequest) -> HttpResponse:
    return render(request, 'about.html')


def contact_us_view(request: HttpRequest) -> HttpResponse:
    return render(request, 'contact_us.html')
