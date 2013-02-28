from django import forms
from django.core.mail import send_mail
from apps.pages.models import HeardFrom


class ContactForm(forms.Form):

    name = forms.CharField(max_length=510)
    email = forms.EmailField()
    subject = forms.CharField(max_length=510)
    message = forms.CharField(widget=forms.Textarea())
    what_brings_you_here = forms.ModelChoiceField(queryset=HeardFrom.objects.all(), required=False)

    def send_mail(self, **kwargs):
        return send_mail(from_email=self.cleaned_data.get('email'),
                         message=self.cleaned_data.get('message'),
                         subject=self.cleaned_data.get('subject'),
                         recipient_list=['uidev@whitelabel.co.uk'],
                         **kwargs)