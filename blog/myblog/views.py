from django.shortcuts import render, HttpResponse, redirect, get_object_or_404
from .models import Articles, Category, Tag
from .forms import ArticleForm, ArticleSearchForm



def list_articles(request):
    # Initialiser les variables pour les articles, catégories et tags
    articles = Articles.objects.all()
    categories = Category.objects.all()
    tags = Tag.objects.all()
    
    # Initialiser le formulaire de recherche
    search_form = ArticleSearchForm(request.GET or None)
    
    # Appliquer les filtres si le formulaire est valide
    if search_form.is_valid():
        keyword = search_form.cleaned_data.get('keyword')
        category = search_form.cleaned_data.get('category')
        selected_tags = search_form.cleaned_data.get('tags')  # Renommé pour éviter la confusion
        
        if keyword:
            articles = articles.filter(title__icontains=keyword)  # Filtrer par mot-clé dans le titre
        
        if category:
            articles = articles.filter(category=category)  # Filtrer par catégorie
        
        if selected_tags:
            articles = articles.filter(tags__in=selected_tags).distinct()  # Filtrer par tags
    
    # Passer le formulaire de recherche et les données aux templates
    dictionnaire = {
        'articles': articles,
        'categories': categories,
        'tags': tags,
        'search_form': search_form,
    }
    
    return render(request, 'articles/list_articles.html', dictionnaire)

def create_article(request):
    if request.method == 'POST':
        form = ArticleForm(request.POST, request.FILES)  # Gérer les fichiers avec request.FILES
        if form.is_valid():
            form.save()  # Enregistre l'article avec l'image
            return redirect('articles')
    else:
        form = ArticleForm()
    
    return render(request, 'articles/formulaires.html', {'form': form})

def edit_article(request, article_id):
    article = get_object_or_404(Articles, id=article_id)
    if request.method == 'POST':
        form = ArticleForm(request.POST, request.FILES, instance=article)
        if form.is_valid():
            form.save()  # Met à jour l'article avec les nouvelles données
            return redirect('articles')
    else:
        form = ArticleForm(instance=article)
    
    return render(request, 'articles/formulaires.html', {'form': form, 'article': article})

def delete_article(request, article_id):
    article = get_object_or_404(Articles, id=article_id)
    if request.method == 'POST':
        article.delete()  # Supprime l'article
        return redirect('articles')
    
    return render(request, 'articles/confirm_delete.html', {'article': article})

def articles_by_category(request, category_id):
    category = get_object_or_404(Category, id=category_id)
    articles = Articles.objects.filter(category=category)
    return render(request, 'articles/list_articles.html', {'articles': articles, 'current_category': category})

def articles_by_tag(request, tag_id):
    tag = get_object_or_404(Tag, id=tag_id)
    articles = Articles.objects.filter(tags=tag)
    return render(request, 'articles/list_articles.html', {'articles': articles, 'current_tag': tag})

def article_detail(request, article_id):
    article = get_object_or_404(Articles, id=article_id)
    return render(request, 'articles/article_detail.html', {'article': article})
