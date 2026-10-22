# RH PARTNERS AFRIC

Projet Django dont la page d’accueil et l’espace consultants reprennent le site de référence fourni le 22 octobre 2026.

Les styles, scripts, images, logos, descriptions des quatre offres et plaquette sont copiés dans `static/reference/`. Aucun accès au site de référence n’est nécessaire à l’affichage.

## Mise en service

Avec la configuration PostgreSQL habituelle du projet :

```sh
python manage.py migrate
python manage.py import_reference_offers
python manage.py collectstatic --noinput
```

Les candidatures et profils consultants sont enregistrés dans `CandidateProfile` et consultables dans l’administration Django. Les CV sont stockés dans `private_uploads/`, à sauvegarder sur un volume persistant. Ce dossier ne doit pas être servi par le serveur web : les téléchargements passent par la vue réservée au personnel connecté.

Les offres sont gérées dans l’administration Django (brouillon/publication, calendrier, contenu). La commande `import_reference_offers` importe les quatre offres initiales sans écraser les modifications. L’API affiche les offres publiées et non expirées, ainsi que les photos publiées de la galerie. Le formulaire de contact enregistre les demandes dans l’administration. Le volume `private_cv_volume` conserve les CV en dehors des fichiers publics et permet leur écriture dans le conteneur en lecture seule.

## Vérifications réalisées

- Contrôle système Django sans erreur.
- Accueil, espace consultants et contenu : réponses HTTP 200 sur une base SQLite de test isolée.
- Dépôt de CV valide, refus de formulaire incomplet et refus d’accès anonyme aux CV.
- Vérification dans le navigateur du filtre de formations et de l’ouverture du détail d’une offre.

Les migrations de la base PostgreSQL configurée restent à appliquer sur l’environnement cible. Le site en production n’a pas été déployé depuis cette session.

## Administration du cabinet

Accès : `/admin/` avec un compte du personnel disposant des permissions des modules.

- **Offres d’emploi** : titre, description, contrat, lieu, publication et clôture.
- **CVthèque** : candidats et consultants, offre visée, recherche par métier et secteur, statut de traitement, chargé du suivi, date de relance, notes internes signées et téléchargement privé du CV.
- **Missions** : client, objectifs, dates, responsable, intervenants et statut.
- **Galerie photos** : image, légende, date, mission, ordre et publication.

Attribuer les permissions « voir/modifier » des profils uniquement aux utilisateurs autorisés à traiter les candidatures. Les notes internes et missions ne sont pas exposées par l’API publique. Aucune décision de sélection n’est automatisée.
