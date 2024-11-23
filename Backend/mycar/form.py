from django import forms
from django.contrib.auth.models import User
from .models import Admin, Client

class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username', 'email', 'password']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password'])
        if commit:
            user.save()
        return user

class AdminForm(forms.ModelForm):
    class Meta:
        model = Admin
        fields = ['role']

class ClientForm(forms.ModelForm):
    class Meta:
        model = Client
        fields = ['age', 'carburant_prefere', 'budget_min', 'budget_max', 'boite_preferee', 'is_user_authenticated', 'last_activity']
