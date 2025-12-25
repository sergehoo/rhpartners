# website/forms.py
from django import forms
from .models import ContactRequest, NewsletterSubscriber, JobApplication


class ContactForm(forms.ModelForm):
    class Meta:
        model = ContactRequest
        fields = ["full_name", "company", "email", "phone", "service", "message", "consent"]
        widgets = {
            "full_name": forms.TextInput(attrs={
                "class": "w-full rounded-xl border border-slate-300 bg-white px-3 py-2 text-xs text-slate-900 form-input dark:border-slate-600 dark:bg-slate-900/60 dark:text-slate-100",
            }),
            "company": forms.TextInput(attrs={
                "class": "w-full rounded-xl border border-slate-300 bg-white px-3 py-2 text-xs text-slate-900 form-input dark:border-slate-600 dark:bg-slate-900/60 dark:text-slate-100",
            }),
            "email": forms.EmailInput(attrs={
                "class": "w-full rounded-xl border border-slate-300 bg-white px-3 py-2 text-xs text-slate-900 form-input dark:border-slate-600 dark:bg-slate-900/60 dark:text-slate-100",
            }),
            "phone": forms.TextInput(attrs={
                "class": "w-full rounded-xl border border-slate-300 bg-white px-3 py-2 text-xs text-slate-900 form-input dark:border-slate-600 dark:bg-slate-900/60 dark:text-slate-100",
            }),
            "service": forms.Select(attrs={
                "class": "w-full rounded-xl border border-slate-300 bg-white px-3 py-2 text-xs text-slate-900 form-input dark:border-slate-600 dark:bg-slate-900/60 dark:text-slate-100",
            }),
            "message": forms.Textarea(attrs={
                "rows": 4,
                "class": "w-full rounded-xl border border-slate-300 bg-white px-3 py-2 text-xs text-slate-900 form-input dark:border-slate-600 dark:bg-slate-900/60 dark:text-slate-100",
            }),
            "consent": forms.CheckboxInput(attrs={
                "class": "rounded border-slate-300 text-gold focus:ring-gold",
            }),
        }
        labels = {
            "full_name": "Nom complet",
            "company": "Entreprise",
            "email": "Email",
            "phone": "Téléphone",
            "service": "Service souhaité",
            "message": "Message",
            "consent": "J’accepte d’être recontacté par RH Partners Afric",
        }


class NewsletterSubscribeForm(forms.ModelForm):
    class Meta:
        model = NewsletterSubscriber
        fields = ["email", "full_name"]
        widgets = {
            "email": forms.EmailInput(attrs={
                "placeholder": "Votre email",
                "class": "w-full rounded-xl border border-slate-300 bg-white px-3 py-2 text-xs dark:border-slate-600 dark:bg-slate-900/60 dark:text-slate-100",
            }),
            "full_name": forms.TextInput(attrs={
                "placeholder": "Nom complet (optionnel)",
                "class": "w-full rounded-xl border border-slate-300 bg-white px-3 py-2 text-xs dark:border-slate-600 dark:bg-slate-900/60 dark:text-slate-100",
            }),
        }
        labels = {
            "email": "",
            "full_name": "",
        }

class JobApplicationForm(forms.ModelForm):
    class Meta:
        model = JobApplication
        fields = [
            "first_name", "last_name", "email", "phone",
            "cv", "cover_letter", "notes",
        ]
        widgets = {
            "first_name": forms.TextInput(attrs={
                "class": "w-full rounded-xl border border-slate-300 bg-white px-3 py-2 text-xs dark:border-slate-600 dark:bg-slate-900/60 dark:text-slate-100",
            }),
            "last_name": forms.TextInput(attrs={
                "class": "w-full rounded-xl border border-slate-300 bg-white px-3 py-2 text-xs dark:border-slate-600 dark:bg-slate-900/60 dark:text-slate-100",
            }),
            "email": forms.EmailInput(attrs={
                "class": "w-full rounded-xl border border-slate-300 bg-white px-3 py-2 text-xs dark:border-slate-600 dark:bg-slate-900/60 dark:text-slate-100",
            }),
            "phone": forms.TextInput(attrs={
                "class": "w-full rounded-xl border border-slate-300 bg-white px-3 py-2 text-xs dark:border-slate-600 dark:bg-slate-900/60 dark:text-slate-100",
            }),
            "cv": forms.ClearableFileInput(attrs={
                "class": "w-full text-xs",
            }),
            "cover_letter": forms.ClearableFileInput(attrs={
                "class": "w-full text-xs",
            }),
            "notes": forms.Textarea(attrs={
                "rows": 4,
                "class": "w-full rounded-xl border border-slate-300 bg-white px-3 py-2 text-xs dark:border-slate-600 dark:bg-slate-900/60 dark:text-slate-100",
            }),
        }
        labels = {
            "first_name": "Prénom",
            "last_name": "Nom",
            "email": "Email",
            "phone": "Téléphone",
            "cv": "CV (PDF, DOC, etc.)",
            "cover_letter": "Lettre de motivation",
            "notes": "Message au recruteur (optionnel)",
        }