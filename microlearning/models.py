from django.db import models
from django.utils import timezone
import uuid
from django.contrib.auth.models import User
from django.urls import reverse


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    subscribed_category = models.CharField(max_length=50, blank=True)


class PublishedManager(models.Manager):
    def get_queryset(self):
        return super(PublishedManager, self).get_queryset().filter(type='Family Medicine', publish__year=2020)


class Article(models.Model):
    ARTICLE_TYPES = (
        ('Allergy & Immunology', 'Allergy & Clinical Immunology'),
        ('Anesthesiology', 'Anesthesiology'),
        ('Business of Medicine', 'Business of Medicine'),
        ('Cardiology', 'Cardiology'),
        ('Critical Care', 'Critical Care'),
        ('Dermatology', 'Dermatology'),
        ('Diabetes & Endocrinology', 'Diabetes & Endocrinology'),
        ('Emergency Medicine', 'Emergency Medicine'),
        ('Family Medicine', 'Family Medicine'),
        ('Gastroenterology', 'Gastroenterology'),
        ('General Surgery', 'General Surgery'),
        ('Hematology-Oncology', 'Oncology'),  # ссылка повторяется ниже
        ('HIV/AIDS', 'HIV/AIDS'),
        ('Hospital Medicine', 'Hospital Medicine'),
        ('Infectious Diseases', 'Infectious Diseases'),
        ('Internal Medicine', 'Internal Medicine'),
        ('Nephrology', 'Nephrology'),
        ('Neurology', 'Neurology'),
        ("Ob/Gyn & Women's Health", "Ob/Gyn & Women's Health"),
        ('Oncology', 'Oncology'),  # повторяется ссылка
        ('Ophthalmology', 'Ophthalmology'),
        ('Orthopedics', 'Orthopedics'),
        ('Pathology & Lab Medicine', 'Pathology & Lab Medicine'),
        ('Pediatrics', 'Pediatrics'),
        ('Plastic Surgery', 'Plastic Surgery'),
        ('Psychiatry', 'Psychiatry'),
        ('Public Health', 'Public Health & Prevention'),
        ('Pulmonary Medicine', 'Pulmonary Medicine'),
        ('Radiology', 'Radiology'),
        ('Rheumatology', 'Rheumatology'),
        ('Transplantation', 'Transplantation'),
        ('Urology', 'Urology'),
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
