from django.forms import ModelForm, forms
from .models import Post


class PostForm(ModelForm):

    class Meta:
        model = Post
        fields = ['group', 'text']

    def clean_text(self):
        text = self.cleaned_data['text']
        if text == '':
            raise forms.ValidationError('Вы не заполнили поле "Текст"')
        return text
