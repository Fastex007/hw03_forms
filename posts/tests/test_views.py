from django.urls import reverse
from django import forms

from posts.lib.MyTestCase import MyTestCase


class PostsPagesTests(MyTestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.templates_pages_names = {
            'index.html': reverse('posts:index'),
            'group.html': (
                reverse('posts:group', kwargs={'slug': 'test_group'})
            ),
            'new_post.html': reverse('posts:new_post'),
        }

    def test_pages_uses_correct_template(self):
        """URL-адрес использует соответствующий шаблон."""
        for template, reverse_name in PostsPagesTests.templates_pages_names.items():
            with self.subTest(reverse_name=reverse_name):
                response = self.authorized_client.get(reverse_name)
                self.assertTemplateUsed(response, template)

    def check_index_context(self, response):
        """Проверяем контекст index. Вынесено в отдельную функцию
        чтобы не дублировать код"""
        post_text_0 = response.context.get('posts')[0].text
        post_author_0 = response.context.get('posts')[0].author
        post_group_0 = response.context.get('posts')[0].group

        self.assertEqual(post_text_0, PostsPagesTests.test_post.text)
        self.assertEqual(post_author_0, PostsPagesTests.test_user)
        self.assertEqual(post_group_0, PostsPagesTests.test_group)

    def test_index_page_show_correct_context(self):
        """Шаблон index сформирован с правильным контекстом."""
        response = self.authorized_client.get(reverse('posts:index'))

        self.check_index_context(response)

    def test_group_pages_show_correct_context(self):
        """Шаблон group сформирован с правильным контекстом."""
        response = self.authorized_client.get(
            reverse('posts:group', kwargs={'slug': 'test_group'})
        )
        self.assertEqual(response.context.get('group').title, 'Тестовая группа')
        self.assertEqual(response.context.get('group').slug, 'test_group')
        # Провряем на месте ли оказался новый пост
        self.check_index_context(response)

    def test_new_post_page_show_correct_context(self):
        """Шаблон new_post сформирован с правильным контекстом."""
        response = self.authorized_client.get(reverse('posts:new_post'))
        form_fields = {
            'text': forms.fields.CharField,
            'group': forms.fields.ChoiceField,
        }

        for value, expected in form_fields.items():
            with self.subTest(value=value):
                form_field = response.context.get('form').fields.get(value)
                self.assertIsInstance(form_field, expected)
