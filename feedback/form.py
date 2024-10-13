from django import forms
from .models import Problem, Offer, Comment,Feedback

class ProblemForm(forms.ModelForm):
    class Meta:
        model = Problem
        fields = ['title', 'description']

class OfferForm(forms.ModelForm):
    class Meta:
        model = Offer
        fields = ['description']

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']

class FeedbackForm(forms.ModelForm):
    class Meta:
        model = Feedback
        fields = ['content', 'is_anonymous']