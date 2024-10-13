from django.urls import path, include
from .views import FeedbackListView, FeedbackCreateView
from django.conf.urls.i18n import i18n_patterns

app_name = 'feedback'

urlpatterns = [
    path('', FeedbackListView.as_view(), name='feedback_list'),
    path('add/', FeedbackCreateView.as_view(), name='feedback_add'),
    path('', include('django.conf.urls.i18n')),

]

urlpatterns += i18n_patterns(
    path('', include('feedback.urls')),
)