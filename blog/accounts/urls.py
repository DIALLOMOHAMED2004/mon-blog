from django.urls import path
from .views import SignUpView, LoginView,ProfileView,EditProfileView,custom_logout,CustomPasswordChangeView
from django.contrib.auth import views as auth_views
from django.contrib.auth.views import PasswordChangeDoneView

urlpatterns = [
    path('signup/', SignUpView.as_view(), name='signup'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', custom_logout, name='logout'),  # Route pour la déconnexion
    path('password_reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('password_reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('password_reset/complete/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
    # Route pour afficher le profil utilisateur
    path('profile/', ProfileView.as_view(), name='profile'),

    # Route pour modifier le profil utilisateur
    path('profile/edit/', EditProfileView.as_view(), name='edit_profile'),
    # Route pour la modification du mot de passe
    path('password-change/', CustomPasswordChangeView.as_view(), name='password_change'),

    # Route pour la confirmation de la modification du mot de passe réussie
    path('password-change/done/', PasswordChangeDoneView.as_view(template_name='registration/password_change_done.html'), name='password_change_done'),
]