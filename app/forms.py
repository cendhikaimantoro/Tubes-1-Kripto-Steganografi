from django import forms

class InsertionForm(forms.Form):
	medium_image = forms.FileField(label='Medium Image')
	message = forms.FileField(label='Message')
	key = forms.CharField(label='Key')
	treshold = forms.IntegerField(label='BPCS Treshold')

class ExtractionForm(forms.Form):
	stegano_image = forms.FileField(label='Stegano Image')
	key = forms.CharField(label='Key')
	treshold = forms.IntegerField(label='BPCS Treshold')
