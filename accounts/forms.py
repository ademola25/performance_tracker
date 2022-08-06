from django import forms
from django.contrib.auth.forms import UserCreationForm, ReadOnlyPasswordHashField, PasswordChangeForm
from .models import User


class RegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    password2 = forms.CharField(
        label='Confirm password', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('email',)

    def clean_email(self):
        email = self.cleaned_data.get('email')
        qs = User.objects.filter(email=email)
        if qs.exists():
            raise forms.ValidationError("email is taken")
        return email

    def clean_password2(self):
        # Check that the two password entries match
        password1 = self.cleaned_data.get("password")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):
        user = super(RegistrationForm, self).save(commit=False)
        user.set_password(self.cleaned_data['password'])
        user.active = True

        if commit:
            user.save()
        return user


class UserAdminRegisterForm(forms.ModelForm):
    ''' class for allowing admins to create bew users '''

    password = forms.CharField(
        label='Password', widget=forms.PasswordInput, max_length=254)
    password2 = forms.CharField(
        label='Confirm Password', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('email', 'admin', 'staff')

    def clean_email(self):
        email = self.cleaned_data.get('email')
        qs = User.objects.filter(email=email)

        if qs.exists():
            raise forms.ValidationError('Email already taken')
        return email

    def clean_password2(self):
        password1 = self.cleaned_data.get('password')
        password2 = self.cleaned_data.get('password2')
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError('Passwords do not match!')
        return password2

    def save(self, commit=True):
        # hash the provided password
        user = super(UserAdminRegisterForm, self).save(commit=False)
        user.set_password(self.cleaned_data.get('password'))
        if commit:
            user.save()
        return user


class UserAdminUpdateForm(forms.ModelForm):
    # update user details from the admin interface
    password = ReadOnlyPasswordHashField(help_text="Raw passwords are not stored, so there is no way to see "
                                         "this user's password, but you can change the password "
                                         "using <a href=\"password/\">this form</a>.")

    # password = forms.CharField(label='Password', widget=forms.PasswordInput, max_length=254)

    class Meta:
        models = User
        fields = ('email', 'password', 'staff', 'is_active', 'admin',)

    def clean_password(self):
        # render salted password
        return self.initial.get('password')

    # def save(self, commit=True):
    #     # hash the provided password
    #     user = super(UserAdminUpdateForm, self).save(commit=False)
    #     user.set_password(self.cleaned_data.get('password'))
    #     if commit:
    #         user.save()
    #     return user


class LoginForm(forms.Form):
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        fields = ['email', 'password']

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop("request", None)
        super(LoginForm, self).__init__(*args, **kwargs)

    def clean_password(self):
        password = self.cleaned_data.get('password')
        if password:
            if len(password) < 4:
                raise forms.ValidationError(
                    'Password must be at least 4 characters long!')
        return password
