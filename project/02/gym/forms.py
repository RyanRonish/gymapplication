from django import forms
from .models import Profile

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['apartment_number', 'bio', 'profile_picture']



from django.contrib.auth.forms import UserCreationForm
from django import forms
from .models import Profile

class CustomUserCreationForm(UserCreationForm):
    apartment_number = forms.CharField(max_length=10)

    class Meta(UserCreationForm.Meta):
        fields = UserCreationForm.Meta.fields + ('apartment_number',)


from django import forms
from .models import Profile

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['profile_picture', 'apartment_number', 'bio', 'twitter', 'linkedin', 'github']
