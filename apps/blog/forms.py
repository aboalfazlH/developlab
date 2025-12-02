from django import forms
from .models import Article
from django_summernote.widgets import SummernoteWidget

class ArticleForm(forms.ModelForm):
    class Meta:
        model = Article
        fields = [
            "title",
            "slug",
            "thumbnail",
            "short_description",
            "description",
            "categories",
        ]
        widgets = {
            "description": SummernoteWidget(
                attrs={"class": "summernote"}
            ),
            "categories": forms.SelectMultiple(
                attrs={"class": "django-select2"}
            ),
        }
