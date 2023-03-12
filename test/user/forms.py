from django.contrib.auth.forms import UserCreationForm, UserChangeForm

from test.user.models import User


class UserAdminCreationForm(UserCreationForm):

    class Meta:
        model = User
        fields = ('email',)


class UserAdminChangeForm(UserChangeForm):

    class Meta:
        model = User
        fields = ('email',)
