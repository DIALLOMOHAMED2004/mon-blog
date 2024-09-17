from django.shortcuts import render, HttpResponse, redirect, get_object_or_404
from .models import Articles, Category, Tag,Comment
from .forms import ArticleForm, ArticleSearchForm,CommentForm
from django.http import HttpResponseForbidden
from django.contrib.auth.decorators import login_required



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

@login_required
def create_article(request):
    if request.method == 'POST':
        form = ArticleForm(request.POST, request.FILES)
        if form.is_valid():
            article = form.save(commit=False)  # Ne pas sauvegarder immédiatement
            article.author = request.user  # Assigner l'utilisateur connecté comme auteur
            article.save()  # Maintenant, sauvegarder l'article avec l'auteur
            form.save_m2m()  # Sauvegarder les relations ManyToMany (comme les tags)
            return redirect('articles')
    else:
        form = ArticleForm()

    return render(request, 'articles/formulaires.html', {'form': form})

def edit_article(request, article_id):
    article = get_object_or_404(Articles, id=article_id)

    # Vérifier si l'utilisateur est l'auteur de l'article
    if request.user != article.author:
        return HttpResponseForbidden("Vous n'êtes pas autorisé à modifier cet article.")

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

    # Vérifier si l'utilisateur est l'auteur de l'article
    if request.user != article.author:
        return HttpResponseForbidden("Vous n'êtes pas autorisé à supprimer cet article.")

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

# Vue pour afficher les détails de l'article et gérer les commentaires
def article_detail(request, article_id):
    article = get_object_or_404(Articles, id=article_id)
    # print(article.tags.all())  # Affiche les tags associés dans la console
    comments = Comment.objects.filter(article=article)  # Récupérer les commentaires liés à l'article
    
    # Initialiser les formulaires d'édition pour les commentaires de l'utilisateur connecté
    comment_forms = {}
    
    if request.user.is_authenticated:
        for comment in comments:
            if comment.author == request.user:
                comment_forms[comment.id] = CommentForm(instance=comment)  # Pré-remplir les formulaires avec les commentaires de l'utilisateur

    if request.method == 'POST':
        if 'comment_id' in request.POST:  # Vérifier si la requête POST concerne l'édition d'un commentaire existant
            comment_id = request.POST.get('comment_id')
            comment_to_edit = get_object_or_404(Comment, id=comment_id)
            if comment_to_edit.author == request.user:
                comment_form = CommentForm(request.POST, instance=comment_to_edit)
                if comment_form.is_valid():
                    comment_form.save()
                    return redirect('article_detail', article_id=article.id)
        else:
            # Sinon, traiter comme un nouveau commentaire
            comment_form = CommentForm(request.POST)
            if comment_form.is_valid():
                new_comment = comment_form.save(commit=False)
                new_comment.article = article
                if request.user.is_authenticated:
                    new_comment.author = request.user
                new_comment.save()
                return redirect('article_detail', article_id=article.id)
    else:
        comment_form = CommentForm()

    return render(request, 'articles/article_detail.html', {
        'article': article,
        'comments': comments,
        'comment_form': comment_form,
        'comment_forms': comment_forms  # Inclure les formulaires d'édition dans le contexte
    })





def delete_comment(request, comment_id):
    comment = get_object_or_404(Comment, id=comment_id)

    # Vérifier si l'utilisateur est l'auteur du commentaire
    if request.user != comment.author:
        return HttpResponse("Vous n'avez pas l'autorisation de supprimer ce commentaire.")

    if request.method == 'POST':
        article_id = comment.article.id  # Sauvegarder l'ID de l'article avant de supprimer le commentaire
        comment.delete()  # Supprime le commentaire
        return redirect('article_detail', article_id=article_id)

    return render(request, 'articles/confirm_delete_comment.html', {'comment': comment})
