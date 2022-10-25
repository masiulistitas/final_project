from django.urls import path, include
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.index, name='index'),
    path("register", views.register_request, name="register"),
    path("login", views.login_request, name="login"),
    path("logout", views.logout_request, name= "logout"),
    path("notes", views.add_note, name= "notes"),
    path("edit_note/<int:id>", views.edit_note, name= "edit_note"),
    path("delete_note/<int:id>", views.delete_note, name="delete_note"),
    path('filter/<int:id>', views.filter, name='category'),
    path("add_category", views.add_category, name= "category"),
    path("update_category/<int:id>", views.update_category, name= "update_category"),
    path("delete_category/<int:id>", views.delete_category, name= "delete_category"),
    path('search/', views.search, name='search'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(template_name='password/password_reset_done.html'), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name="password/password_reset_confirm.html"), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(template_name='password/password_reset_complete.html'), name='password_reset_complete'),
    path("password_reset", views.password_reset_request, name="password_reset"),
    ]

