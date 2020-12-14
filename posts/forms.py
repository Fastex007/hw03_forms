from django.forms import ModelForm

from .models import Post


class PostForm(ModelForm):

    class Meta:
        model = Post
        fields = ['group', 'text']
        help_texts = {
            'group': 'Группа в которой может быть опубликован текст',
            'text': 'Текст публикации'
        }
