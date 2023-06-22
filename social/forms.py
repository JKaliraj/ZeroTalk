from django import forms
from .models import Talk,Profile
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class TalkForm(forms.ModelForm):
    body = forms.CharField(
        required=True,
        widget=forms.widgets.Textarea(
            attrs={
                "placeholder":"Enter Your Tweet!",
                "class":"form-control"
            },
        ),
        label="")
    
    class Meta:
        model=Talk
        exclude = ("user","likes",)

class RegisterForm(UserCreationForm):
    email = forms.EmailField(label="",widget=forms.TextInput(attrs={"class":"form-control","placeholder":"Email Address"}))
    first_name = forms.CharField(max_length=100, label="",widget=forms.TextInput(attrs={"class":"form-control","placeholder":"First Name"}))
    last_name = forms.CharField(max_length=100, label="",widget=forms.TextInput(attrs={"class":"form-control","placeholder":"Last Name"}))
        
    class Meta:
        model = User
        fields=('username','first_name','last_name','email','password1','password2')

    def __init__(self, *args, **kwargs):
        super(RegisterForm, self).__init__(*args, **kwargs)

        self.fields['username'].widget.attrs['class'] = 'form-control'
        self.fields['username'].widget.attrs['placeholder'] = 'User Name'
        self.fields['username'].label = ''
        self.fields['username'].help_text = '<span class="form-text text-muted"><small>Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.</small></span>'

        self.fields['password1'].widget.attrs['class'] = 'form-control'
        self.fields['password1'].widget.attrs['placeholder'] = 'Password'
        self.fields['password1'].label = ''
        self.fields['password1'].help_text = '<ul class="form-text text-muted small"><li>Your password can\'t be too similar to your other personal information.</li><li>Your password must contain at least 8 characters.</li><li>Your password can\'t be a commonly used password.</li><li>Your password can\'t be entirely numeric.</li></ul>'

        self.fields['password2'].widget.attrs['class'] = 'form-control'
        self.fields['password2'].widget.attrs['placeholder'] = 'Confirm Password'
        self.fields['password2'].label = ''
        self.fields['password2'].help_text = '<span class="form-text text-muted"><small>Enter the same password as before, for verification.</small></span>'

class UpdateUserForm(forms.ModelForm):
    # username = forms.CharField(max_length=100, required=True, widget=forms.TextInput(attrs={'class': 'form-control'}))
    email = forms.EmailField(label="Email",widget=forms.TextInput(attrs={"class":"form-control","placeholder":"Email Address"}))
    first_name = forms.CharField(max_length=100, label="First Name",widget=forms.TextInput(attrs={"class":"form-control","placeholder":"First Name"}))
    last_name = forms.CharField(max_length=100, label="Last Name",widget=forms.TextInput(attrs={"class":"form-control","placeholder":"Last Name"}))
    

    class Meta:
        model = User
        # fields=('username','first_name','last_name','email')
        fields=('first_name','last_name','email')

class ProfileImageForm(forms.ModelForm):
    profile_image = forms.ImageField(label="Profile Image")

    bio = forms.CharField(required=False,max_length=500, label="",widget=forms.Textarea(attrs={"class":"form-control","placeholder":"Bio"}))
    website_link = forms.CharField(required=False,max_length=100, label="",widget=forms.TextInput(attrs={"class":"form-control","placeholder":"Website Link"}))
    facebook_link = forms.CharField(required=False,max_length=100, label="",widget=forms.TextInput(attrs={"class":"form-control","placeholder":"Facebook Link"}))
    instagram_link = forms.CharField(required=False,max_length=100, label="",widget=forms.TextInput(attrs={"class":"form-control","placeholder":"Instagram Link"}))
    linkedin_link = forms.CharField(required=False,max_length=100, label="",widget=forms.TextInput(attrs={"class":"form-control","placeholder":"Linkedin Link"}))

    class Meta:
        model = Profile
        fields = ('profile_image','bio','website_link','facebook_link','instagram_link','linkedin_link', )