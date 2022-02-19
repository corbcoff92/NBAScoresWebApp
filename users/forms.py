from django.contrib.auth.forms import UserCreationForm


class CustomUserCreationForm(UserCreationForm):
    '''
    Form used to create a custom user. 
    This form includes the user's first name in addition to the standard Django User fields. 
    '''
    class Meta(UserCreationForm.Meta):
        fields = UserCreationForm.Meta.fields + ("first_name",)
