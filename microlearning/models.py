from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse
from django.conf import settings


class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    subscribed_category = models.CharField(max_length=50, blank=True)

    objects = models.Manager()

    def get_my_articles(self):
        if self.subscribed_category:
            return Article.objects.filter(type=self.subscribed_category)

        return []


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    if not hasattr(instance, 'profile'):
        Profile.objects.create(user=instance)

    instance.profile.save()


class PublishedManager(models.Manager):
    def get_queryset(self):
        return super(PublishedManager, self).get_queryset().filter(type='familymedicine', publish__year=2020)


class Article(models.Model):

    ARTICLE_TYPES = (
        ('allergy-immunology', 'Allergy & Clinical Immunology'),
        ('anesthesiology', 'Anesthesiology'),
        ('businessmedicine', 'Business of Medicine'),
        ('cardiology', 'Cardiology'),
        ('criticalcare', 'Critical Care'),
        ('dermatology', 'Dermatology'),
        ('diabetes-endocrinology', 'Diabetes & Endocrinology'),
        ('emergencymedicine', 'Emergency Medicine'),
        ('familymedicine', 'Family Medicine'),
        ('gastroenterology', 'Gastroenterology'),
        ('generalsurgery', 'General Surgery'),
        ('oncology', 'Oncology'),
        ('hiv', 'HIV/AIDS'),
        ('hospitalmedicine', 'Hospital Medicine'),
        ('infectiousdiseases', 'Infectious Diseases'),
        ('internalmedicine', 'Internal Medicine'),
        ('nephrology', 'Nephrology'),
        ('neurology', 'Neurology'),
        ('womenshealth', "Ob/Gyn & Women's Health"),
        ('ophthalmology', 'Ophthalmology'),
        ('orthopedics', 'Orthopedics'),
        ('pathology', 'Pathology & Lab Medicine'),
        ('pediatrics', 'Pediatrics'),
        ('plastic-surgery', 'Plastic Surgery'),
        ('psychiatry', 'Psychiatry'),
        ('publichealth', 'Public Health & Prevention'),
        ('pulmonarymedicine', 'Pulmonary Medicine'),
        ('radiology', 'Radiology'),
        ('rheumatology', 'Rheumatology'),
        ('transplantation', 'Transplantation'),
        ('urology', 'Urology'),
    )
    STATUS_TYPES = (
        ('new', 'New'),
        ('finished', 'Finished'),
    )
    title = models.CharField(max_length=250)
    slug = models.SlugField(max_length=250,
                            unique_for_date='publish')
    body = models.TextField()
    publish = models.DateTimeField(default=timezone.now)
    type = models.CharField(max_length=50,
                            choices=ARTICLE_TYPES,
                            default='theory')
    status = models.CharField(max_length=20,
                              choices=STATUS_TYPES,
                              default='new')
    author = models.CharField(max_length=250)
    objects = models.Manager()
    published = PublishedManager()

    # def __str__(self):
    #     return self.title
    def get_absolute_url(self):
        return reverse('microlearning:article_details',
                       args=[self.publish.year,
                             self.publish.month,
                             self.publish.day,
                             self.slug])
