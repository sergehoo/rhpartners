from django.test import TestCase, override_settings

# Create your tests here.

from datetime import timedelta
from django.test import TestCase, override_settings
from django.contrib.auth import get_user_model
from django.utils import timezone
from django.core.management import call_command
from .models import JobOffer, GalleryPhoto, Mission


@override_settings(STATICFILES_STORAGE='django.contrib.staticfiles.storage.StaticFilesStorage')
class CabinetAdministrationTests(TestCase):
    def test_only_current_published_offers_are_public(self):
        for slug, published, delta in [('open', True, 1), ('draft', False, 1), ('expired', True, -1)]:
            JobOffer.objects.create(title=slug, slug=slug, is_published=published, closing_date=timezone.now()+timedelta(days=delta))
        self.assertEqual([j['id'] for j in self.client.get('/api/content').json()['jobs']], ['open'])

    def test_gallery_hides_drafts(self):
        for published in [True, False]:
            GalleryPhoto.objects.create(title='Photo', image='gallery/example.jpg', date=timezone.localdate(), is_published=published)
        self.assertEqual(len(self.client.get('/api/content').json()['photos']), 1)
        self.assertEqual(self.client.get('/api/media/2').status_code, 404)

    def test_admin_requires_login_and_permissions(self):
        self.assertEqual(self.client.get('/admin/website/candidateprofile/').status_code, 302)
        user = get_user_model().objects.create_user('operator', password='test', is_staff=True)
        self.client.force_login(user)
        self.assertEqual(self.client.get('/admin/website/candidateprofile/').status_code, 403)
        self.assertEqual(self.client.get('/private-cv/1/').status_code, 403)

    def test_reference_import_does_not_overwrite_edits(self):
        call_command('import_reference_offers', verbosity=0)
        offer = JobOffer.objects.first()
        offer.title = 'Titre modifié'
        offer.save()
        call_command('import_reference_offers', verbosity=0)
        offer.refresh_from_db()
        self.assertEqual(offer.title, 'Titre modifié')
        self.assertEqual(JobOffer.objects.count(), 4)

    def test_admin_modules_render(self):
        user = get_user_model().objects.create_superuser('manager', 'test@example.com', 'test')
        self.client.force_login(user)
        for model in ['candidateprofile', 'mission', 'galleryphoto', 'joboffer']:
            self.assertEqual(self.client.get(f'/admin/website/{model}/').status_code, 200)
            self.assertEqual(self.client.get(f'/admin/website/{model}/add/').status_code, 200)

    def test_contact_requires_consent_and_saves_request(self):
        from .models import ContactRequest
        data = dict(name='Test', email='test@example.com', interest='Formation', message='Bonjour')
        self.assertEqual(self.client.post('/api/contact', data).status_code, 400)
        data['consent'] = 'on'
        self.assertEqual(self.client.post('/api/contact', data).status_code, 200)
        self.assertEqual(ContactRequest.objects.count(), 1)

    def test_candidate_and_consultant_with_csrf(self):
        from django.test import Client
        from django.core.files.uploadedfile import SimpleUploadedFile
        from .models import CandidateProfile
        import uuid
        c = Client(enforce_csrf_checks=True)
        c.get('/')
        token = c.cookies['csrftoken'].value
        for kind in ['candidate', 'consultant']:
            data = dict(name='Test', email='test@example.com', phone='123', profession='Consultant', sector='Conseil', job_function='RH', experience='2', consent='on', submission_id=str(uuid.uuid4()), profile_type=kind, csrfmiddlewaretoken=token)
            if kind == 'consultant':
                data.update(expertise='Formation', expertise_details='Management')
            data['cv'] = SimpleUploadedFile('test.pdf', b'%PDF-1.4 test')
            with self.settings(MEDIA_ROOT='/tmp/rh-tests-media'):
                response = c.post('/api/candidates', data)
            self.assertEqual(response.status_code, 200, response.content)
        self.assertEqual(CandidateProfile.objects.count(), 2)
        for profile in CandidateProfile.objects.all():
            profile.cv.delete()
