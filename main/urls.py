from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
urlpatterns = [
    path('', views.home, name='home'),
    path('home/', views.home, name='home'),
    path('login/', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('sign-up/', views.sign_up, name='sign_up'),
    path('logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),
    path('new-job/', views.create_job_post, name='create_job_post'),
    path('delete-job/<int:post_id>/', views.delete_job_post, name='delete_job_post'),
    path('apply-job/<int:post_id>/', views.apply_job, name='apply_job'),
    path('edit_job_post/<int:post_id>/', views.edit_job_post, name='edit_job_post'),
    path('hr-dashboard/', views.hr_dashboard, name='hr_dashboard'),
    path('job-posts/<int:post_id>/applicants/', views.view_applicants, name='view_applicants'),
    path('job-posts/<int:post_id>/generate-analysis-report/', views.generate_analysis_report, name='generate_analysis_report'),



]
