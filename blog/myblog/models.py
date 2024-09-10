from django.db import models

class Category(models.Model):
    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.name

class Tag(models.Model):
    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.name

class Articles(models.Model):
    title = models.CharField(max_length=255)
    summary = models.CharField(max_length=255, null=True, blank=True)
    content = models.TextField()
    image = models.ImageField(upload_to='articles_images/', null=True, blank=True)
    date_pub = models.DateField(null=True)
    link = models.URLField(null=True, blank=True)  # Nouveau champ pour les liens
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True)  # Relation avec la catégorie
    tags = models.ManyToManyField(Tag, blank=True)  # Relation avec les tags

    def __str__(self):
        return self.title
