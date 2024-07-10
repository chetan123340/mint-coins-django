from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import MintUser

class MintUserCreationForm(UserCreationForm):

    class Meta(UserCreationForm):
        model = MintUser
        fields = ('username', 'email', 'password1', 'password2')

class MintUserChangeForm(UserChangeForm):

    class Meta(UserChangeForm):
        model = MintUser
        fields = ('username', 'amount')