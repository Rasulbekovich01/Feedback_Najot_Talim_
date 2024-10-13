from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, CreateView, DetailView
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from .models import Problem, Offer, Comment
from .form import ProblemForm, OfferForm, CommentForm
from .models import Feedback
from .form import FeedbackForm
class ProblemListView(ListView):
    model = Problem
    template_name = 'feedback/problem_list.html'

@method_decorator(login_required, name='dispatch')
class ProblemCreateView(CreateView):
    model = Problem
    form_class = ProblemForm
    template_name = 'feedback/problem_form.html'
    success_url = '/problems/'

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

class ProblemDetailView(DetailView):
    model = Problem
    template_name = 'feedback/problem_detail.html'

@method_decorator(login_required, name='dispatch')
class OfferCreateView(CreateView):
    model = Offer
    form_class = OfferForm
    template_name = 'feedback/offer_form.html'

    def get_initial(self):
        initial = super().get_initial()
        initial['problem'] = self.kwargs['pk']  # Pre-fill the problem ID
        return initial

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return f'/problems/{self.object.problem.id}/'

@method_decorator(login_required, name='dispatch')
class CommentCreateView(CreateView):
    model = Comment
    form_class = CommentForm
    template_name = 'feedback/comment_form.html'

    def get_initial(self):
        initial = super().get_initial()
        initial['offer'] = self.kwargs['pk']  # Pre-fill the offer ID
        return initial

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return f'/problems/{self.object.offer.problem.id}/'

class FeedbackListView(ListView):
    model = Feedback
    template_name = 'feedback/feedback_list.html'

class FeedbackCreateView(CreateView):
    model = Feedback
    form_class = FeedbackForm
    template_name = 'feedback/feedback_form.html'
    success_url = '/feedback/'

    def form_valid(self, form):
        form.instance.user = self.request.user  
        return super().form_valid(form)