from django import forms
from .models import QuoteRequest, Contact

class QuoteRequestForm(forms.ModelForm):
    class Meta:
        model = QuoteRequest
        fields = ['name', 'email', 'phone', 'service', 'project_description', 
                 'budget_range', 'timeline', 'attachments']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'peer w-full bg-primary-900 border border-metal-500/30 rounded-xl px-4 py-3 text-gray-100',
                'placeholder': ' '
            }),
            'email': forms.EmailInput(attrs={
                'class': 'peer w-full bg-primary-900 border border-metal-500/30 rounded-xl px-4 py-3 text-gray-100',
                'placeholder': ' '
            }),
            'phone': forms.TextInput(attrs={
                'class': 'peer w-full bg-primary-900 border border-metal-500/30 rounded-xl px-4 py-3 text-gray-100',
                'placeholder': ' '
            }),
            'service': forms.Select(attrs={
                'class': 'peer w-full bg-primary-900 border border-metal-500/30 rounded-xl px-4 py-3 text-gray-100'
            }),
            'project_description': forms.Textarea(attrs={
                'class': 'peer w-full bg-primary-900 border border-metal-500/30 rounded-xl px-4 py-3 text-gray-100',
                'rows': 4,
                'placeholder': ' '
            }),
            'budget_range': forms.Select(attrs={
                'class': 'peer w-full bg-primary-900 border border-metal-500/30 rounded-xl px-4 py-3 text-gray-100'
            }, choices=[
                ('', 'Select Budget Range'),
                ('under_1000', 'Under $1,000'),
                ('1000_5000', '$1,000 - $5,000'),
                ('5000_10000', '$5,000 - $10,000'),
                ('over_10000', 'Over $10,000')
            ]),
            'timeline': forms.Select(attrs={
                'class': 'peer w-full bg-primary-900 border border-metal-500/30 rounded-xl px-4 py-3 text-gray-100'
            }, choices=[
                ('', 'Select Timeline'),
                ('urgent', 'Urgent (Within a week)'),
                ('normal', 'Normal (2-4 weeks)'),
                ('flexible', 'Flexible (1-3 months)')
            ]),
            'attachments': forms.FileInput(attrs={
                'class': 'hidden'
            })
        }


class ContactForm(forms.ModelForm):
    class Meta:
        model = Contact
        fields = ['name', 'email', 'subject', 'message']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'peer w-full bg-primary-900 border border-metal-500/30 rounded-xl px-4 py-3 text-gray-100 focus:outline-none focus:border-accent-500 focus:ring-2 focus:ring-accent-500/30 transition duration-300 ease-in-out',
                'placeholder': ' ',
                'required': True
            }),
            'email': forms.EmailInput(attrs={
                'class': 'peer w-full bg-primary-900 border border-metal-500/30 rounded-xl px-4 py-3 text-gray-100 focus:outline-none focus:border-accent-500 focus:ring-2 focus:ring-accent-500/30 transition duration-300 ease-in-out',
                'placeholder': ' ',
                'required': True
            }),
            'subject': forms.TextInput(attrs={
                'class': 'peer w-full bg-primary-900 border border-metal-500/30 rounded-xl px-4 py-3 text-gray-100 focus:outline-none focus:border-accent-500 focus:ring-2 focus:ring-accent-500/30 transition duration-300 ease-in-out',
                'placeholder': ' ',
                'required': True
            }),
            'message': forms.Textarea(attrs={
                'class': 'peer w-full bg-primary-900 border border-metal-500/30 rounded-xl px-4 py-3 text-gray-100 focus:outline-none focus:border-accent-500 focus:ring-2 focus:ring-accent-500/30 transition duration-300 ease-in-out resize-none',
                'placeholder': ' ',
                'rows': 5,
                'required': True
            })
        }
