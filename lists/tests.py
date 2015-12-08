from django.test import TestCase
from django.http import HttpRequest
from django.template.loader import render_to_string
from .views import home_page
from .models import Item
# Create your tests here.


class HomePageViewTest(TestCase):

    def test_home_page_returns_correct_html(self):
        request = HttpRequest()
        response = home_page(request)        
        # print response.content
        # self.assertIn('<title>To-Do lists</title>', response.content)
        # self.assertTrue(response.content.startswith('<html>'))
        # self.assertTrue(response.content.endswith('</html>'))

        # expected_content = open('lists/templates/home.html').read()
        expected_content = render_to_string('home.html')
        self.assertEqual(
            response.content,
            expected_content)


    def test_home_page_can_save_a_POST_request(self):
        request = HttpRequest()
        request.method = 'POST'
        request.POST['item_text'] = 'A new list item'

        response = home_page(request)
        # self.assertIn('A new list item', response.content)

        expected_html = render_to_string(
            'home.html',
            {'new_item_text': 'A new list item'})
        self.assertEqual(response.content, expected_html)


class ItemModelTest(TestCase):

    def test_saving_and_retrieving_items(self):
        first_item = Item()
        first_item.text = 'The first (ever) list item'
        first_item.save()

        second_item = Item()
        second_item.text = 'Item the second'
        second_item.save()

        saved_item = Item.objects.all()
        self.assertEqual(saved_item.count(), 2)

        first_saved_item = saved_item[0]
        second_saved_item = saved_item[1]
        self.assertEqual(first_saved_item.text, 'The first (ever) list item')
        self.assertEqual(second_saved_item.text, 'Item the second')
        