from django.shortcuts import render, get_object_or_404
from django.views import generic
from django.contrib.auth.forms import UserChangeForm, PasswordChangeForm
from .forms import SignUpForm, EditProfileForm, PasswordChangingForm, ProfilePageForm
from django.urls import reverse_lazy
from django.contrib.auth.views import PasswordChangeView
from django.views.generic import DetailView, CreateView
from theblog.models import Profile


class CreateProfilePageView(CreateView):
    model= Profile
    form_class= ProfilePageForm # this is written in place of fields
    template_name= "registration/create_user_profile_page.html"
    # fields= "__all__"

    def form_valid(self, form): # we pass the entire form in here 
        form.instance.user= self.request.user # this get the user who is filling this form 
        return super().form_valid(form)


class EditProfilePageView(generic.UpdateView):
    model= Profile
    template_name= 'registration/edit_profile_page.html'
    fields= ['bio', 'profile_pic', 'website_url', 'facebook_url', 'twitter_url', 'instagram_url', 'pinterest_url']
    success_url= reverse_lazy('home')


class ShowProfilePageView(DetailView):
    model= Profile
    template_name= 'registration/user_profile.html'

    def get_context_data(self, *args, **kwargs): # get_context_data provided by django class 
        users= Profile.objects.all()
        context= super(ShowProfilePageView, self).get_context_data(*args, **kwargs)
        page_user= get_object_or_404(Profile, id=self.kwargs['pk'])
        context['page_user']= page_user
        return context


class PasswordsChangeView(PasswordChangeView):
    form_class= PasswordChangingForm
    success_url= reverse_lazy('password_success')


def password_success(request):
    return render(request, 'registration/password_success.html', {})


class UserRegisterView(generic.CreateView):
    form_class= SignUpForm
    template_name= 'registration/register.html'
    success_url= reverse_lazy('login')
    

class UserEditView(generic.UpdateView):
    form_class= EditProfileForm
    template_name= 'registration/edit_profile.html'
    success_url= reverse_lazy('home')

    def get_object(self): # buit-in django def. Tells UserEditView which user is updated
        return self.request.user


