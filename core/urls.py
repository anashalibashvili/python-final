from django.urls import path
from core.views import HomeView, QuestionDetailView, QuestionCreateView, QuestonDeleteView, QuestionUpdateView, \
    questions_by_tag, about_us_view, contact_us_view

app_name = 'core'

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('tags/<str:tag>/', questions_by_tag, name='tags'),
    path('questions/<int:pk>/', QuestionDetailView.as_view(), name='question-detail'),
    path('questions/<int:pk>/delete/', QuestonDeleteView.as_view(), name='question-delete'),
    path('questions/<int:pk>/update/', QuestionUpdateView.as_view(), name='question-update'),
    path('ask/', QuestionCreateView.as_view(), name='question-create'),
    path('about-us/', about_us_view, name='about-us'),
    path('contact-us/', contact_us_view, name='contact-us'),
]
