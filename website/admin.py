from django.contrib import admin

# Register your models here.
# website/admin.py
from django.contrib import admin
from .models import Service, PricingPlan, Testimonial, FAQ, ContactRequest, NewsletterCampaign, JobOffer, \
    JobApplication, NewsletterSubscriber


class BaseTimestampedAdmin(admin.ModelAdmin):
    """Options communes : dates en readonly, ordre par -created_at."""
    readonly_fields = ("created_at", "updated_at")
    ordering = ("-created_at",)


@admin.register(Service)
class ServiceAdmin(BaseTimestampedAdmin):
    list_display = (
        "title",
        "slug",
        "order",
        "is_active",
        "created_at",
    )
    list_filter = ("is_active",)
    search_fields = ("title", "slug", "short_description", "description")
    prepopulated_fields = {"slug": ("title",)}
    list_editable = ("order", "is_active")
    fieldsets = (
        (None, {
            "fields": ("title", "slug", "short_description", "description")
        }),
        ("Affichage & icône", {
            "fields": ("icon_class", "order", "is_active"),
            "classes": ("collapse",),
        }),
        ("Métadonnées", {
            "fields": ("created_at", "updated_at"),
            "classes": ("collapse",),
        }),
    )


@admin.register(PricingPlan)
class PricingPlanAdmin(BaseTimestampedAdmin):
    list_display = (
        "name",
        "slug",
        "price_label",
        "target_segment",
        "is_featured",
        "is_active",
        "order",
    )
    list_filter = ("is_active", "is_featured")
    search_fields = ("name", "slug", "price_label", "tagline", "target_segment")
    prepopulated_fields = {"slug": ("name",)}
    list_editable = ("order", "is_featured", "is_active")
    fieldsets = (
        (None, {
            "fields": ("name", "slug", "tagline")
        }),
        ("Tarification", {
            "fields": ("price_label", "price_amount", "target_segment"),
        }),
        ("Contenu & affichage", {
            "fields": ("features", "is_featured", "order", "is_active"),
        }),
        ("Métadonnées", {
            "fields": ("created_at", "updated_at"),
            "classes": ("collapse",),
        }),
    )


@admin.register(Testimonial)
class TestimonialAdmin(BaseTimestampedAdmin):
    list_display = (
        "full_name",
        "company",
        "role",
        "rating",
        "order",
        "is_active",
        "created_at",
    )
    list_filter = ("is_active", "rating")
    search_fields = ("full_name", "company", "role", "quote")
    list_editable = ("order", "is_active", "rating")
    fieldsets = (
        (None, {
            "fields": ("full_name", "initials", "role", "company")
        }),
        ("Contenu", {
            "fields": ("quote", "rating"),
        }),
        ("Affichage", {
            "fields": ("order", "is_active"),
        }),
        ("Métadonnées", {
            "fields": ("created_at", "updated_at"),
            "classes": ("collapse",),
        }),
    )


@admin.register(FAQ)
class FAQAdmin(BaseTimestampedAdmin):
    list_display = ("question", "order", "is_active", "created_at")
    list_filter = ("is_active",)
    search_fields = ("question", "answer")
    list_editable = ("order", "is_active")
    fieldsets = (
        (None, {
            "fields": ("question", "answer")
        }),
        ("Affichage", {
            "fields": ("order", "is_active"),
        }),
        ("Métadonnées", {
            "fields": ("created_at", "updated_at"),
            "classes": ("collapse",),
        }),
    )


@admin.register(ContactRequest)
class ContactRequestAdmin(BaseTimestampedAdmin):
    list_display = (
        "full_name",
        "company",
        "email",
        "phone",
        "service",
        "created_at",
    )
    list_filter = ("service", "created_at")
    search_fields = ("full_name", "company", "email", "phone", "message")
    date_hierarchy = "created_at"
    readonly_fields = ("created_at", "updated_at")
    fieldsets = (
        ("Identité", {
            "fields": ("full_name", "company")
        }),
        ("Contact", {
            "fields": ("email", "phone"),
        }),
        ("Besoin", {
            "fields": ("service", "message", "consent"),
        }),
        ("Métadonnées", {
            "fields": ("created_at", "updated_at"),
            "classes": ("collapse",),
        }),
    )


@admin.register(NewsletterSubscriber)
class NewsletterSubscriberAdmin(admin.ModelAdmin):
    list_display = ("email", "full_name", "is_active", "created_at")
    list_filter = ("is_active", "created_at")
    search_fields = ("email", "full_name")
    date_hierarchy = "created_at"
    list_editable = ("is_active",)


@admin.register(NewsletterCampaign)
class NewsletterCampaignAdmin(admin.ModelAdmin):
    list_display = ("title", "subject", "status", "scheduled_at", "sent_at", "created_at")
    list_filter = ("status", "scheduled_at", "created_at")
    search_fields = ("title", "subject", "body_html")
    date_hierarchy = "scheduled_at"
    actions = ["mark_as_scheduled", "mark_as_draft"]

    def mark_as_scheduled(self, request, queryset):
        updated = queryset.update(status=NewsletterCampaign.STATUS_SCHEDULED)
        self.message_user(request, f"{updated} campagne(s) marquée(s) comme planifiées.")

    mark_as_scheduled.short_description = "Marquer comme planifiées"

    def mark_as_draft(self, request, queryset):
        updated = queryset.update(status=NewsletterCampaign.STATUS_DRAFT)
        self.message_user(request, f"{updated} campagne(s) repassée(s) en brouillon.")

    mark_as_draft.short_description = "Repasser en brouillon"


@admin.register(JobOffer)
class JobOfferAdmin(BaseTimestampedAdmin):
    list_display = ("title", "location", "contract_type", "is_published", "published_at", "closing_date")
    list_filter = ("is_published", "contract_type", "location")
    search_fields = ("title", "short_description", "description")
    prepopulated_fields = {"slug": ("title",)}
    list_editable = ("is_published",)
    fieldsets = (
        (None, {
            "fields": ("title", "slug", "short_description", "description")
        }),
        ("Contrat & affichage", {
            "fields": ("location", "contract_type", "is_published", "published_at", "closing_date"),
        }),
        ("Métadonnées", {
            "fields": ("created_at", "updated_at"),
            "classes": ("collapse",),
        }),
    )


@admin.register(JobApplication)
class JobApplicationAdmin(BaseTimestampedAdmin):
    list_display = ("last_name", "first_name", "job_offer", "email", "phone", "status", "processed", "created_at")
    list_filter = ("job_offer", "status", "processed", "created_at")
    search_fields = ("last_name", "first_name", "email", "phone", "notes")
    list_editable = ("status", "processed")
    date_hierarchy = "created_at"
    fieldsets = (
        ("Candidat", {
            "fields": ("job_offer", "first_name", "last_name", "email", "phone"),
        }),
        ("Documents", {
            "fields": ("cv", "cover_letter"),
        }),
        ("Notes & suivi", {
            "fields": ("notes", "status", "processed"),
        }),
        ("Métadonnées", {
            "fields": ("created_at", "updated_at"),
            "classes": ("collapse",),
        }),
    )
