from django import forms
from .models import Material
from .models import Info


class MaterialForm(forms.ModelForm):
    class Meta:
        model = Material
        fields = ('m_name', 'm_file', )