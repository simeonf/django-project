from django.contrib.auth.models import User, Group
from django import forms
from django.db import IntegrityError

from polls.models import Choice

class VoteForm(forms.Form):
    choice = forms.ModelChoiceField(queryset=Choice.objects.none(),
                                    widget=forms.RadioSelect,
                                    empty_label=None)
    def save(self):
        c = self.cleaned_data['choice']
        c.votes += 1
        c.save()
    
class RegistrationForm(forms.Form):
    username = forms.CharField(max_length=30, min_length=3,
                               help_text="Usernames must be between 3-30 alpha-numeric characters.")
    email = forms.EmailField(label="E-mail")
    password1 = forms.CharField(label="Password", widget=forms.PasswordInput)
    password2 = forms.CharField(label="Password Again", widget=forms.PasswordInput)

    def clean_username(self):
        username = self.cleaned_data['username']
        if not username.isalnum():
            raise forms.ValidationError('Usernames must be letters and characters only.')
        if User.objects.filter(username=username):
            raise forms.ValidationError('That username is not available.')
        return username
    
    def clean(self):
        data = self.cleaned_data
        p1 = data.get('password1')
        p2 = data.get('password2') 
        if p1 != p2:
            # attach the error message to the password control
            forms.errors['password2'] = ['The passwords you entered did not match!']
        return data
            
    def save(self):
        username = self.cleaned_data['username']
        password = self.cleaned_data['password1']
        email = self.cleaned_data['email']
        try:
            u = User.objects.create_user(username, email, password)
            # user can login to admin
            u.is_staff = True
            u.save()
            # Add to the poll_users group for permissions            
            g = Group.objects.get(name="poll_users")
            u.groups.add(g)
        except IntegrityError:
            self.errors['username'] = ['That username is taken!']
        return self.is_valid()