from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify


class Project(models.Model):

    TECHNOLOGY_CHOICES = [
        ("Python Django", "Python Django"),
        ("Python Flask", "Python Flask"),
        ("Java Spring Boot", "Java Spring Boot"),
        ("Node.js", "Node.js"),
        ("React", "React"),
        ("Angular", "Angular"),
        ("Docker", "Docker"),
        ("Other", "Other"),
    ]

    VISIBILITY_CHOICES = [
        ("Private", "Private"),
        ("Public", "Public"),
    ]

    STATUS_CHOICES = [
        ("Active", "Active"),
        ("Inactive", "Inactive"),
        ("Archived", "Archived"),
    ]

    owner = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="projects"
    )

    name = models.CharField(max_length=200)

    slug = models.SlugField(
        unique=True,
        blank=True
    )

    description = models.TextField(blank=True)

    repository_url = models.URLField(blank=True)
    default_branch = models.CharField(
        max_length=100,
        default="main"
    )

    technology = models.CharField(
        max_length=100,
        choices=TECHNOLOGY_CHOICES,
        default="Python Django"
    )

    visibility = models.CharField(
        max_length=20,
        choices=VISIBILITY_CHOICES,
        default="Private"
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="Active"
    )

    is_archived = models.BooleanField(
        default=False
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    def save(self, *args, **kwargs):

        if not self.slug:
            self.slug = slugify(self.name)

        super().save(*args, **kwargs)

    def __str__(self):
        return self.name