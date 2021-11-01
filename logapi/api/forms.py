from django.db.models import fields
from django.forms import forms
from .models import UserDetails


class userForm(forms.Form):
    class Meta:
        model = UserDetails
        fields = "__all__"