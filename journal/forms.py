from django import forms
from .models import ContactMessage


class ContactForm(forms.ModelForm):
    """Форма обратной связи"""
    
    class Meta:
        model = ContactMessage
        fields = ['name', 'phone', 'email', 'message']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ваше имя',
                'id': 'Name-input'
            }),
            'phone': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '+7-(999)-999-99-99',
                'id': 'tel-input'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'ivan_ivanov@miigaik.ru',
                'id': 'email-input'
            }),
            'message': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Текст сообщения',
                'id': 'message-input',
                'rows': 4
            })
        }
        labels = {
            'name': 'Имя',
            'phone': 'Телефон',
            'email': 'Email',
            'message': 'Сообщение'
        }
