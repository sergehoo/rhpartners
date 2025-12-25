# website/models.py
from django.db import models


class TimeStampedModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Service(TimeStampedModel):
    title = models.CharField("Titre", max_length=150)
    slug = models.SlugField(unique=True)
    icon_class = models.CharField(
        "Icône Font Awesome",
        max_length=80,
        blank=True,
        help_text="Ex: 'fas fa-file-invoice-dollar'"
    )
    short_description = models.TextField("Description courte")
    description = models.TextField("Description détaillée", blank=True)
    order = models.PositiveIntegerField("Ordre d'affichage", default=0)
    is_active = models.BooleanField("Actif", default=True)

    class Meta:
        ordering = ["order", "title"]
        verbose_name = "Service"
        verbose_name_plural = "Services"

    def __str__(self):
        return self.title


class PricingPlan(TimeStampedModel):
    name = models.CharField("Nom du pack", max_length=150)
    slug = models.SlugField(unique=True)
    tagline = models.CharField("Sous-titre", max_length=255, blank=True)
    price_label = models.CharField(
        "Libellé de prix",
        max_length=150,
        help_text="Ex: 'À partir de 250 000 FCFA / mois' ou 'Sur devis'"
    )
    price_amount = models.DecimalField(
        "Montant numérique (optionnel)",
        max_digits=12,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Pour tri / stats, optionnel"
    )
    target_segment = models.CharField(
        "Segment cible",
        max_length=150,
        blank=True,
        help_text="Ex: TPE, PME, Grandes entreprises"
    )
    features = models.TextField(
        "Points forts (1 par ligne)",
        help_text="Saisir une fonctionnalité par ligne"
    )
    is_featured = models.BooleanField("Mettre en avant", default=False)
    order = models.PositiveIntegerField("Ordre d'affichage", default=0)
    is_active = models.BooleanField("Actif", default=True)

    class Meta:
        ordering = ["order", "name"]
        verbose_name = "Pack tarifaire"
        verbose_name_plural = "Packs tarifaires"

    def __str__(self):
        return self.name

    @property
    def features_list(self):
        return [f.strip() for f in self.features.splitlines() if f.strip()]


class Testimonial(TimeStampedModel):
    full_name = models.CharField("Nom complet", max_length=150)
    initials = models.CharField(
        "Initiales",
        max_length=4,
        help_text="Ex: 'AK', 'SD'"
    )
    role = models.CharField("Poste", max_length=150)
    company = models.CharField("Entreprise", max_length=150, blank=True)
    quote = models.TextField("Témoignage")
    rating = models.PositiveSmallIntegerField("Note (1-5)", default=5)
    order = models.PositiveIntegerField("Ordre d'affichage", default=0)
    is_active = models.BooleanField("Actif", default=True)

    class Meta:
        ordering = ["order", "-created_at"]
        verbose_name = "Témoignage"
        verbose_name_plural = "Témoignages"

    def __str__(self):
        return f"{self.full_name} – {self.company}".strip(" –")


class FAQ(TimeStampedModel):
    question = models.CharField("Question", max_length=255)
    answer = models.TextField("Réponse")
    order = models.PositiveIntegerField("Ordre d'affichage", default=0)
    is_active = models.BooleanField("Actif", default=True)

    class Meta:
        ordering = ["order", "question"]
        verbose_name = "Question fréquente"
        verbose_name_plural = "Questions fréquentes"

    def __str__(self):
        return self.question


class ContactRequest(TimeStampedModel):
    SERVICE_CHOICES = [
        ("gestion-rh", "Gestion RH externalisée"),
        ("paie", "Paie externalisée"),
        ("recrutement", "Recrutement & intégration"),
        ("creation-entreprise", "Création / structuration d’entreprise"),
        ("multi", "Plusieurs services"),
        ("autre", "Autre / à préciser"),
    ]

    full_name = models.CharField("Nom complet", max_length=150)
    company = models.CharField("Entreprise", max_length=150, blank=True)
    email = models.EmailField("Email")
    phone = models.CharField("Téléphone", max_length=50, blank=True)
    service = models.CharField(
        "Service souhaité",
        max_length=40,
        choices=SERVICE_CHOICES,
        default="gestion-rh"
    )
    message = models.TextField("Message")
    consent = models.BooleanField(
        "J’accepte d’être recontacté",
        default=True
    )

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "Demande de contact"
        verbose_name_plural = "Demandes de contact"

    def __str__(self):
        return f"{self.full_name} – {self.company or 'Sans entreprise'}"


class NewsletterSubscriber(models.Model):
    email = models.EmailField("Email", unique=True)
    full_name = models.CharField("Nom complet", max_length=150, blank=True)
    is_active = models.BooleanField("Actif / abonné", default=True)
    created_at = models.DateTimeField("Date d'inscription", auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "Abonné newsletter"
        verbose_name_plural = "Abonnés newsletter"

    def __str__(self):
        return self.email


class NewsletterCampaign(models.Model):
    STATUS_DRAFT = "draft"
    STATUS_SCHEDULED = "scheduled"
    STATUS_SENT = "sent"
    STATUS_CHOICES = [
        (STATUS_DRAFT, "Brouillon"),
        (STATUS_SCHEDULED, "Planifiée"),
        (STATUS_SENT, "Envoyée"),
    ]

    title = models.CharField("Titre interne", max_length=200)
    subject = models.CharField("Objet de l'email", max_length=255)
    body_html = models.TextField(
        "Contenu HTML",
        help_text="Contenu de la newsletter (HTML)."
    )
    scheduled_at = models.DateTimeField(
        "Date/heure d'envoi prévue",
        null=True,
        blank=True
    )
    sent_at = models.DateTimeField("Envoyée le", null=True, blank=True)
    status = models.CharField(
        "Statut",
        max_length=20,
        choices=STATUS_CHOICES,
        default=STATUS_DRAFT,
    )
    created_at = models.DateTimeField("Créée le", auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "Campagne newsletter"
        verbose_name_plural = "Campagnes newsletter"

    def __str__(self):
        return f"{self.title} ({self.get_status_display()})"

    @property
    def is_due(self):
        return (
                self.status == self.STATUS_SCHEDULED
                and self.scheduled_at is not None
                and self.scheduled_at <= timezone.now()
        )


class JobOffer(TimeStampedModel):
    CONTRACT_CHOICES = [
        ("cdi", "CDI"),
        ("cdd", "CDD"),
        ("stage", "Stage"),
        ("freelance", "Freelance"),
        ("autre", "Autre"),
    ]

    title = models.CharField("Titre du poste", max_length=200)
    slug = models.SlugField(unique=True)
    location = models.CharField("Localisation", max_length=150, default="Abidjan, Côte d’Ivoire")
    contract_type = models.CharField("Type de contrat", max_length=20, choices=CONTRACT_CHOICES, default="cdi")
    short_description = models.TextField("Résumé de l’offre")
    description = models.TextField("Description détaillée")
    is_published = models.BooleanField("Publiée sur le site", default=True)
    published_at = models.DateTimeField("Date de publication", null=True, blank=True)
    closing_date = models.DateTimeField("Date limite de candidature", null=True, blank=True)

    class Meta:
        ordering = ["-published_at", "-created_at"]
        verbose_name = "Offre d'emploi"
        verbose_name_plural = "Offres d'emploi"

    def __str__(self):
        return self.title


def cv_upload_path(instance, filename):
    return f"candidatures/{instance.job_offer.slug}/{instance.last_name}_{instance.first_name}_cv_{filename}"


def cover_letter_upload_path(instance, filename):
    return f"candidatures/{instance.job_offer.slug}/{instance.last_name}_{instance.first_name}_lm_{filename}"


class JobApplication(TimeStampedModel):
    job_offer = models.ForeignKey(JobOffer, on_delete=models.CASCADE, related_name="applications", verbose_name="Offre")
    first_name = models.CharField("Prénom", max_length=100)
    last_name = models.CharField("Nom", max_length=100)
    email = models.EmailField("Email")
    phone = models.CharField("Téléphone", max_length=50)
    cv = models.FileField("CV", upload_to=cv_upload_path)
    cover_letter = models.FileField("Lettre de motivation", upload_to=cover_letter_upload_path)
    notes = models.TextField("Message / Notes du candidat", blank=True)
    processed = models.BooleanField("Dossier traité", default=False)
    status = models.CharField(
        "Statut",
        max_length=30,
        default="reçu",
        help_text="Ex: reçu, en cours, retenu, rejeté..."
    )

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "Candidature"
        verbose_name_plural = "Candidatures"

    def __str__(self):
        return f"{self.last_name} {self.first_name} – {self.job_offer.title}"
class HeroSlide(models.Model):
    POSITION_TEXT = "text"
    POSITION_VISUAL = "visual"

    POSITION_CHOICES = (
        (POSITION_TEXT, "Colonne texte"),
        (POSITION_VISUAL, "Colonne visuelle"),
    )

    THEME_AUTO = "auto"
    THEME_LIGHT = "light"
    THEME_DARK = "dark"

    THEME_CHOICES = (
        (THEME_AUTO, "Automatique (suivre le thème)"),
        (THEME_LIGHT, "Forcer clair"),
        (THEME_DARK, "Forcer sombre"),
    )

    pair_key = models.SlugField(
        "Clé de paire (slide 1, slide-2…)",
        help_text="Permet d’associer une slide texte et une slide visuelle (même valeur pour les deux)."
    )
    position = models.CharField(
        max_length=10,
        choices=POSITION_CHOICES,
        default=POSITION_TEXT,
    )
    order = models.PositiveSmallIntegerField(
        "Ordre dans le slider",
        default=0,
        help_text="Plus petit = affiché en premier."
    )
    is_active = models.BooleanField(default=True)

    # Contenu commun
    badge_label = models.CharField(
        "Badge",
        max_length=120,
        blank=True,
        help_text="Ex: 'Cabinet RH & Paie – Afrique'"
    )
    badge_icon = models.CharField(
        "Classe icône FontAwesome",
        max_length=80,
        blank=True,
        help_text="Ex: 'fas fa-file-invoice-dollar' (optionnel)."
    )

    title = models.CharField(
        "Titre principal",
        max_length=200,
        blank=True,
    )
    highlighted_text = models.CharField(
        "Texte mis en valeur (span gold)",
        max_length=120,
        blank=True,
        help_text="Ex: 'Ressources Humaines' ou 'bulletins de paie'"
    )
    subtitle = models.TextField(
        "Texte descriptif",
        blank=True,
    )

    # Bouton principal
    primary_label = models.CharField(
        "Texte bouton principal",
        max_length=100,
        blank=True,
    )
    primary_url = models.CharField(
        "Lien bouton principal",
        max_length=200,
        blank=True,
        help_text="Ex: #contact, #pricing ou URL complète."
    )
    primary_icon = models.CharField(
        "Classe icône bouton principal",
        max_length=80,
        blank=True,
        help_text="Ex: 'fas fa-calendar-check'."
    )

    # Bouton secondaire
    secondary_label = models.CharField(
        "Texte bouton secondaire",
        max_length=100,
        blank=True,
    )
    secondary_url = models.CharField(
        "Lien bouton secondaire",
        max_length=200,
        blank=True,
    )
    secondary_icon = models.CharField(
        "Classe icône bouton secondaire",
        max_length=80,
        blank=True,
    )

    # Stats (simple, 3 lignes max)
    stat_1_value = models.CharField(max_length=50, blank=True)
    stat_1_label = models.CharField(max_length=120, blank=True)
    stat_2_value = models.CharField(max_length=50, blank=True)
    stat_2_label = models.CharField(max_length=120, blank=True)
    stat_3_value = models.CharField(max_length=50, blank=True)
    stat_3_label = models.CharField(max_length=120, blank=True)

    # Visuels
    image = models.ImageField(
        upload_to="hero_slides/",
        blank=True,
        null=True,
        help_text="Image principale (pour les slides visuelles surtout)."
    )
    visual_title = models.CharField(
        "Titre visuel",
        max_length=150,
        blank=True,
    )
    visual_subtitle = models.CharField(
        "Sous-titre visuel",
        max_length=200,
        blank=True,
    )
    visual_badge = models.CharField(
        "Badge visuel / pill",
        max_length=120,
        blank=True,
    )

    theme_variant = models.CharField(
        max_length=10,
        choices=THEME_CHOICES,
        default=THEME_AUTO,
        help_text="Permet d’ajuster certains contrastes si besoin."
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["order", "pair_key", "position"]

    def __str__(self):
        return f"{self.get_position_display()} – {self.title or self.pair_key}"