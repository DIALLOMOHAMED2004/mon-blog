from django.shortcuts import render,get_object_or_404,redirect
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic.edit import FormView
from .forms  import CustomUserCreationForm
from django.contrib.auth import login,logout
from django.contrib.auth.views import LoginView,PasswordChangeView
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import UpdateView
from django.contrib.auth.models import User
from .forms import EditProfileForm



class HomePageView(TemplateView):
    template_name = 'accounts/home.html'


class SignUpView(FormView):
    template_name = 'accounts/signup.html'
    form_class = CustomUserCreationForm
    success_url = reverse_lazy('login')

    def form_valid(self, form):
        user = form.save()  # Enregistre le nouvel utilisateur
        login(self.request, user)  # Connecte automatiquement l'utilisateur après l'inscription
        return super().form_valid(form)


class LoginView(LoginView):
    template_name = 'accounts/login.html'


# Vue pour afficher le profil utilisateur
class ProfileView(LoginRequiredMixin, TemplateView):
    template_name = 'accounts/profile.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Passer l'utilisateur authentifié au template
        context['user'] = self.request.user
        return context

# Vue pour modifier le profil utilisateur
class EditProfileView(LoginRequiredMixin, UpdateView):
    model = User
    form_class = EditProfileForm
    template_name = 'accounts/edit_profile.html'
    success_url = reverse_lazy('articles')

    def get_object(self, queryset=None):
        # Retourner l'utilisateur authentifié
        return get_object_or_404(User, pk=self.request.user.pk)
    
# Vue personnalisée pour la déconnexion
def custom_logout(request):
    logout(request)
    return redirect('home')  # Rediriger vers la page d'accueil après déconnexion

class CustomPasswordChangeView(LoginRequiredMixin, PasswordChangeView):
    template_name = 'registration/password_change_form.html'  # Le template pour la modification du mot de passe
    success_url = reverse_lazy('edit_profile')  # Redirection après un changement réussi
    
