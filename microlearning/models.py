from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse
from django.conf import settings
from django.utils.text import slugify


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

    id_med = models.IntegerField()
    title = models.CharField(max_length=250)
    slug = models.SlugField(max_length=250)
    body = models.TextField()
    publish = models.DateTimeField(default=timezone.now)
    type = models.CharField(max_length=50,
                            choices=ARTICLE_TYPES)
    status = models.CharField(max_length=20,
                              choices=STATUS_TYPES,
                              default='new')
    author = models.CharField(max_length=250)

    objects = models.Manager()
    published = PublishedManager()

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['type', 'id_med'], name='unique_article'),
        ]

    def get_absolute_url(self):
        return reverse('microlearning:article_details',
                       args=[self.type,
                             self.id_med,
                             self.slug])

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title, allow_unicode=True)

        super().save(*args, **kwargs)


class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    subscribed_category = models.CharField(max_length=50, blank=True, choices=Article.ARTICLE_TYPES)

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
