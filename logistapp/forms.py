from django import forms
from .models import *


class ItemForm(forms.ModelForm):

    name = forms.CharField(widget=forms.TextInput, )

    class Meta:
        model = Item
        fields = ('name', 'sender', 'address_from', 'recipient', 'address_to', 'weight', 'category')
