from django.contrib.auth.forms import AuthenticationForm
from django import forms
from django.contrib.auth.models import User, Group, Permission
from django.contrib.auth import get_user_model

class LoginForm(AuthenticationForm):
    pass

User = get_user_model()

class AdminUserCreationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    groups = forms.ModelMultipleChoiceField(queryset=Group.objects.all(), required=False)
    user_permissions = forms.ModelMultipleChoiceField(queryset=Permission.objects.all(), required=False, widget=forms.CheckboxSelectMultiple)

    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', 'password', 'groups', 'user_permissions']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password'])
        if commit:
            user.save()
            user.groups.set(self.cleaned_data['groups'])
            user.user_permissions.set(self.cleaned_data['user_permissions'])
        return user
    
