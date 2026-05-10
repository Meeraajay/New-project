from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.register_view, name='register'),
    path('', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),

    path('student-dashboard/', views.student_dashboard, name='student_dashboard'),
    path('admin-dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('profile/', views.profile_view, name='profile'),
    path("save-profile/", views.save_profile, name="save_profile"),
    path("cbse/", views.cbse_view, name="cbse"),
    path("kerala/", views.kerala_view, name="kerala"),
    path('extracurricular/', views.extracurricular, name='extracurricular'),
    path('course-preference/',views.course_preference,name='course_preference'),
    path('download-allotment/', views.download_allotment, name='download_allotment'),

]