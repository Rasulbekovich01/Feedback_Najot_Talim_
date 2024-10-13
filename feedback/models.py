from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import User

class Problem(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

class Offer(models.Model):
    problem = models.ForeignKey(Problem, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Offer for {self.problem.title}"

class Comment(models.Model):
    offer = models.ForeignKey(Offer, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Comment on {self.offer.problem.title}" 

class User(AbstractUser):
        pass

class Feedback(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_anonymous = models.BooleanField(default=False)

    def __str__(self):
        return self.content[:50]