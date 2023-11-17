from django import forms

class CSVUploadForm(forms.Form):
    file_name = forms.FileField(label='Upload a CSV file')
