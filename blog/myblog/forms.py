from django import forms
from .models import Articles, Category, Tag

class ArticleForm(forms.ModelForm):
    class Meta:
        model = Articles
        fields = '__all__'
        
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Titre de l\'article'}),
            'summary': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Résumé'}),
            'content': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Contenu de l\'article'}),
            'date_pub': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'image': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'link': forms.URLInput(attrs={'class': 'form-control', 'placeholder': 'Lien (facultatif)'}),
            'category': forms.Select(attrs={'class': 'form-control'}),  # Nouveau champ pour la catégorie
            'tags': forms.CheckboxSelectMultiple(attrs={'class': 'form-check'}),  # Nouveau champ pour les tags
        }
        labels = {
            'title': 'Titre',
            'summary': 'Résumé',
            'content': 'Contenu',
            'date_pub': 'Date de publication',
            'link': 'Lien',
            'category': 'Catégorie',
            'tags': 'Étiquettes',
        }
        
    def clean_title(self):
        title = self.cleaned_data.get('title')
        if len(title) < 5:
            raise forms.ValidationError('Le titre doit contenir au moins 5 caractères.')
        return title

class ArticleSearchForm(forms.Form):
    keyword = forms.CharField(required=False, label='Mot-clé', widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Rechercher...'}))
    category = forms.ModelChoiceField(required=False, queryset=Category.objects.all(), label='Catégorie', empty_label='Toutes les catégories', widget=forms.Select(attrs={'class': 'form-control'}))
    tags = forms.ModelMultipleChoiceField(required=False, queryset=Tag.objects.all(), label='Tags', widget=forms.CheckboxSelectMultiple(attrs={'class': 'form-check'}))
