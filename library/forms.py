from django import forms
from django.contrib.auth.forms import AuthenticationForm
from library.models import Account, Book

class RegisterForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    # confirm_password = forms.CharField(widget=forms.PasswordInput)
    class Meta:
        model = Account
        fields = ['first_name', 'last_name', 'email', 'password']
    
    # def save(self, commit=True):
    #     user = super().save(commit=False)
    #     password = self.cleaned_data.get('password')
    #     user.set_password(password)
    #     if commit:
    #         user.save()
    #     return user
        
    def save(self, commit=True):
        manager = Account.objects
        user = manager.create_user(
            first_name=self.cleaned_data['first_name'],
            last_name=self.cleaned_data['last_name'],
            email=self.cleaned_data['email'],
            password=self.cleaned_data['password'],
        )
        return user

class LoginForm(forms.Form):
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)


class AdminRegisterForm(forms.ModelForm):
    password =  forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = Account
        fields = ['first_name', 'last_name', 'email', 'password']

    def save(self, commit=True):
        user = Account.objects.create_admin(
            first_name=self.cleaned_data['first_name'],
            last_name=self.cleaned_data['last_name'],
            email=self.cleaned_data['email'],
            password=self.cleaned_data['password'],
        )
        return user

class RegisterBook(forms.ModelForm):
    class Meta:
        model = Book
        fields = ['name', 'author', 'category','description','cover_image','language','isbn']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'author': forms.TextInput(attrs={'class': 'form-control'}),
            'category': forms.Select(attrs={'class': 'form-control'}),
        }

