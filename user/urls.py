from django.urls import path
from user import views
from django.contrib import admin
from django.urls import path, include

urlpatterns = [

    path('sending-email/', views.SendEmailView.as_view(), name='send_email'),
    path('success/', views.success, name='success'),
    path('login/', views.LoginPageView.as_view(), name='login_page'),
    path('register/', views.register_page, name='register_page'),
    path('activation-link/<uidb64>/<token>/', views.activate, name='activate'),
    path('logout/', views.logout_page, name='logout_page'),
    path('admin/', admin.site.urls),
    path('', include('feedback.urls')),
]
