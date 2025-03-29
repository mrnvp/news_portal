from django import forms
from django_filters import FilterSet, CharFilter, ModelChoiceFilter, DateFilter
from .models import Post, Author

# по названию
# по имени автора
# позже указываемой даты

class PostFilter(FilterSet):
    name = CharFilter(lookup_expr='icontains', label='Название') 
    author = ModelChoiceFilter(
        queryset=Author.objects.all(),
        label='Автор'
    )
    datetime_in = DateFilter(field_name='datetime_in', lookup_expr='gt', label='Позже даты', widget=forms.DateInput(attrs={'type': 'date'}))

    class Meta:
        model = Post
        fields = ['name', 'author', 'datetime_in']
    