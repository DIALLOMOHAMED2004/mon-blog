from django.contrib import admin
from .models import Articles, Category, Tag, Comment  # Import du modèle Comment

class ArticleAdmin(admin.ModelAdmin):
    list_display = ('title', 'summary', 'date_pub', 'category')
    search_fields = ('title', 'summary', 'content')
    list_filter = ('category', 'tags')
    filter_horizontal = ('tags',)

class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)

class TagAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)

# Nouveau : configuration de l'administration pour les commentaires
class CommentAdmin(admin.ModelAdmin):
    list_display = ('author', 'article', 'content', 'date_pub')  # Afficher les champs principaux
    search_fields = ('author', 'content')  # Rechercher par auteur et contenu
    list_filter = ('article', 'date_pub')  # Filtrer par article et date de publication

admin.site.register(Articles, ArticleAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Tag, TagAdmin)
admin.site.register(Comment, CommentAdmin)  # Enregistrement du modèle Comment
