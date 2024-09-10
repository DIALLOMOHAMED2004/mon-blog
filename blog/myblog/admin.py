from django.contrib import admin
from .models import Articles, Category, Tag

class ArticleAdmin(admin.ModelAdmin):
    list_display = ('title', 'summary', 'date_pub', 'category')
    search_fields = ('title', 'summary', 'content')
    list_filter = ('category', 'tags')
    filter_horizontal = ('tags',)  # Pour afficher les tags dans un champ de sélection multiple

class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)

class TagAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)

admin.site.register(Articles, ArticleAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Tag, TagAdmin)
