from django.urls import path
from django.urls import re_path

from . import views
from .forms import LoginForm

app_name = "accounts"

urlpatterns = [re_path(r'^login/$',
                       views.LoginView.as_view(success_url='/'),
                       name='login',
                       kwargs={'authentication_form': LoginForm}),
               re_path(r'^register/$',
                       views.RegisterView.as_view(success_url="/"),
                       name='register'),
               re_path(r'^logout/$',
                       views.LogoutView.as_view(),
                       name='logout'),
               path(r'account/result.html',
                    views.account_result,
                    name='result'),
               re_path(r'^forget_password/$',
                       views.ForgetPasswordView.as_view(),
                       name='forget_password'),
               re_path(r'^forget_password_code/$',
                       views.ForgetPasswordEmailCode.as_view(),
                       name='forget_password_code'),
               # Notifications
               re_path(r'^notifications/$', views.notification_list, name='notification_list'),
               re_path(r'^notifications/(?P<notification_id>\d+)/read/$', views.mark_notification_as_read, name='mark_notification_as_read'),
               re_path(r'^notifications/mark-all-read/$', views.mark_all_as_read, name='mark_all_as_read'),
               ]
