from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect

# Create your views here.
# website/views.py
from django.urls import reverse_lazy
from django.views.decorators.http import require_POST
from django.views.generic import FormView, ListView, DetailView
from django.contrib import messages

from .models import Service, PricingPlan, Testimonial, FAQ, NewsletterSubscriber, JobOffer
from .forms import ContactForm, JobApplicationForm, NewsletterSubscribeForm


class HomePageView(FormView):
    """
    One-page pour tout le site (sections Accueil, À propos, Services,
    Process, Tarifs, Témoignages, FAQ, Contact).
    """
    template_name = "website/reference.html"
    form_class = ContactForm
    success_url = reverse_lazy("website:home")

    def form_valid(self, form):
        form.save()  # enregistrement en base
        # Optionnel: ici tu peux ajouter un envoi d’email
        messages.success(
            self.request,
            "Votre demande a bien été envoyée. Un consultant vous contactera rapidement."
        )
        return super().form_valid(form)



@require_POST
def newsletter_subscribe(request):
    form = NewsletterSubscribeForm(request.POST)
    if form.is_valid():
        subscriber, created = NewsletterSubscriber.objects.get_or_create(
            email=form.cleaned_data["email"],
            defaults={"full_name": form.cleaned_data.get("full_name", "")},
        )
        if not created and not subscriber.is_active:
            subscriber.is_active = True
            subscriber.save(update_fields=["is_active"])
        messages.success(request, "Merci, vous êtes inscrit à notre newsletter.")
    else:
        messages.error(request, "Veuillez saisir un email valide.")
    return HttpResponseRedirect(request.META.get("HTTP_REFERER", reverse_lazy("website:home")))


class JobOfferListView(ListView):
    model = JobOffer
    template_name = "website/job_list.html"
    context_object_name = "offers"

    def get_queryset(self):
        qs = JobOffer.objects.filter(is_published=True)
        return qs


class JobOfferDetailView(DetailView):
    model = JobOffer
    template_name = "website/job_detail.html"
    context_object_name = "offer"
    slug_field = "slug"
    slug_url_kwarg = "slug"

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["form"] = JobApplicationForm()
        return ctx

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = JobApplicationForm(request.POST, request.FILES)
        if form.is_valid():
            application = form.save(commit=False)
            application.job_offer = self.object
            application.save()
            messages.success(
                request,
                "Votre candidature a bien été envoyée. Merci pour votre intérêt."
            )
            return redirect("website:job_detail", slug=self.object.slug)

        ctx = self.get_context_data()
        ctx["form"] = form
        return self.render_to_response(ctx)


from pathlib import Path
import json
import uuid
from django.http import JsonResponse, FileResponse, HttpResponseForbidden
from django.views.generic import TemplateView
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from django.utils import timezone
from .models import CandidateProfile


def reference_content(request):
    from django.db.models import Q
    from django.utils import timezone
    from .models import GalleryPhoto
    today = timezone.localdate()
    offers = JobOffer.objects.filter(is_published=True).filter(Q(published_at__isnull=True) | Q(published_at__lte=timezone.now())).filter(Q(closing_date__isnull=True) | Q(closing_date__date__gte=today))
    return JsonResponse({'jobs': [dict(id=j.slug, title=j.title, location=j.location,
        contract=j.short_description or j.get_contract_type_display(), description=j.description,
        deadline=j.closing_date.date().isoformat() if j.closing_date else '', published=True) for j in offers],
        'photos': [dict(id=str(p.pk), title=p.title, caption=p.caption, date=p.date.isoformat()) for p in GalleryPhoto.objects.filter(is_published=True)],
        'email': 'recrutement@rhpartnersafric.com'})


def gallery_media(request, pk):
    from .models import GalleryPhoto
    from django.shortcuts import get_object_or_404
    photo = get_object_or_404(GalleryPhoto, pk=pk, is_published=True)
    return FileResponse(photo.image.open('rb'))


@require_POST
def candidate_submit(request):
    p = request.POST
    required = ('name', 'email', 'phone', 'profession', 'sector', 'job_function', 'experience')
    if any(not p.get(key, '').strip() for key in required) or not p.get('consent'):
        return JsonResponse({'error': 'Complétez les champs obligatoires et le consentement.'}, status=400)
    try:
        validate_email(p['email'])
        reference = uuid.UUID(p.get('submission_id', ''))
    except (ValidationError, ValueError):
        return JsonResponse({'error': 'Adresse e-mail ou référence invalide.'}, status=400)
    cv = request.FILES.get('cv')
    if not cv or cv.size > 5 * 1024 * 1024 or Path(cv.name).suffix.lower() not in ('.pdf', '.doc', '.docx'):
        return JsonResponse({'error': 'Joignez un CV PDF ou Word de 5 Mo maximum.'}, status=400)
    if p.get('website'):
        return JsonResponse({'error': 'Dépôt refusé.'}, status=400)
    if p.get('profile_type') == 'consultant' and (not p.getlist('expertise') or not p.get('expertise_details', '').strip()):
        return JsonResponse({'error': 'Précisez vos domaines et vos expertises.'}, status=400)
    kind = 'consultant' if p.get('profile_type') == 'consultant' else 'candidate'
    details = {k: p.getlist(k) if len(p.getlist(k)) > 1 else p.get(k) for k in p if k not in ('csrfmiddlewaretoken', 'website')}
    offer = JobOffer.objects.filter(slug=p.get('job_id'), is_published=True).first()
    if p.get('job_id') and (not offer or (offer.closing_date and offer.closing_date.date() < timezone.localdate())):
        return JsonResponse({'error': 'Cette offre n’est plus disponible.'}, status=400)
    profile, _ = CandidateProfile.objects.get_or_create(reference=reference, defaults=dict(
        name=p['name'][:120], email=p['email'], phone=p['phone'][:40], profession=p['profession'][:180],
        sector=p['sector'][:180], job_function=p['job_function'][:180], profile_type=kind,
        details=details, cv=cv, consent=True, job_offer=offer))
    return JsonResponse({'reference': str(profile.reference)})


def private_cv(request, pk):
    if not request.user.is_active or not request.user.is_staff or not request.user.has_perm('website.view_candidateprofile'):
        return HttpResponseForbidden()
    from django.shortcuts import get_object_or_404
    profile = get_object_or_404(CandidateProfile, pk=pk)
    return FileResponse(profile.cv.open('rb'), as_attachment=True)


@require_POST
def contact_submit(request):
    from .models import ContactRequest
    p = request.POST
    if any(not p.get(k, '').strip() for k in ('name', 'email', 'interest', 'message')) or p.get('consent') != 'on':
        return JsonResponse({'error': 'Complétez les champs obligatoires et acceptez le consentement.'}, status=400)
    try:
        validate_email(p['email'])
    except ValidationError:
        return JsonResponse({'error': 'Saisissez une adresse e-mail valide.'}, status=400)
    if len(p['name']) > 100 or len(p['message']) > 4000 or len(p.get('company', '')) > 160:
        return JsonResponse({'error': 'Le texte saisi dépasse la longueur autorisée.'}, status=400)
    ContactRequest.objects.create(full_name=p['name'].strip(), email=p['email'].strip(), company=p.get('company', '').strip()[:150], service='autre', message='Besoin : '+p['interest'][:180]+'\n\n'+p['message'].strip(), consent=True)
    return JsonResponse({'message': 'Votre demande a bien été enregistrée. Notre équipe vous recontactera.'})
