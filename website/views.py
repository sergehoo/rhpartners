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
    template_name = "website/home.html"
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

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)

        ctx["services"] = Service.objects.filter(is_active=True)
        ctx["pricing_plans"] = PricingPlan.objects.filter(is_active=True)
        ctx["featured_plan"] = ctx["pricing_plans"].filter(is_featured=True).first()
        ctx["testimonials"] = Testimonial.objects.filter(is_active=True)[:4]
        ctx["faqs"] = FAQ.objects.filter(is_active=True)

        return ctx


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
