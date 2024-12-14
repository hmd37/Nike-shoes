from django import forms
from .models import Shoe


class ShoeForm(forms.ModelForm):
    class Meta:
        model = Shoe
        fields = ['name', 'category' ,'size', 'num_of_colors', 'price', 'image', 'info']  # Adjust fields as needed
