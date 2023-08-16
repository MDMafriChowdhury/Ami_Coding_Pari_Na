from django import forms

class KhojSearchForm(forms.Form):
    input_values = forms.CharField(label='Input Values', widget=forms.TextInput(attrs={'placeholder': '9, 1, 5, 7, 10, 11, 0'}))
    search_value = forms.IntegerField(label='Search Value')
