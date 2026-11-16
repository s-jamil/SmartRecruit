from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import JobPost, Application
class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', 'password1', 'password2']
        help_texts = {
            'username': "Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.",
            'email': "Please enter a valid email address.",
            'first_name': "",
            'last_name': "",
         }
    def save(self, commit=True):
        user = super(RegisterForm, self).save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
        return user


class JobPostForm(forms.ModelForm):
    class Meta:
        model = JobPost
        fields = ["job_title", "job_description"]
       

class ApplicationForm(forms.ModelForm):
    class Meta:
        model = Application
        fields = ['cv']