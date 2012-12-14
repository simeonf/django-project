from django.contrib.auth.models import User, Group
import floppyforms as forms

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit

from django.db import IntegrityError

from polls.models import Choice, SocialUser

class ProfileForm(forms.ModelForm):
    class Meta:
        model = SocialUser
        exclude = ['user']

    def __init__(self, *args, **kwargs):
        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helper.add_input(Submit("submit", "Submit"))
        super(ProfileForm, self).__init__(*args, **kwargs)
        
        
class VoteForm(forms.Form):
    choice = forms.ModelChoiceField(queryset=Choice.objects.none(),
                                    label="",
                                    widget=forms.RadioSelect,
                                    empty_label=None)
    def __init__(self, *args, **kwargs):
        self.helper = FormHelper()
        self.helper.form_class = 'form-horizontal'
        self.helper.add_input(Submit("submit", "Submit"))
        super(VoteForm, self).__init__(*args, **kwargs)

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

    def __init__(self, *args, **kwargs):
        self.helper = FormHelper()
        self.helper.form_tag = False
        super(RegistrationForm, self).__init__(*args, **kwargs)
        
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
