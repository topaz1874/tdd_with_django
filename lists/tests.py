from django.test import TestCase
from django.http import HttpRequest
from django.template.loader import render_to_string
from .views import home_page
from .models import Item, List
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


class ListAndItemModelsTest(TestCase):

    def test_saving_and_retrieving_items(self):
        list_ = List()
        list_.save()

        first_item = Item()
        first_item.text = 'The first (ever) list item'
        first_item.list = list_
        first_item.save()

        second_item = Item()
        second_item.text = 'Item the second'
        second_item.list = list_
        second_item.save()

        saved_list = List.objects.first()
        self.assertEqual(saved_list, list_)

        saved_item = Item.objects.all()
        self.assertEqual(saved_item.count(), 2)

        first_saved_item = saved_item[0]
        second_saved_item = saved_item[1]
        self.assertEqual(first_saved_item.text, 'The first (ever) list item')
        self.assertEqual(first_saved_item.list, list_)
        self.assertEqual(second_saved_item.text, 'Item the second')
        self.assertEqual(second_saved_item.list, list_)


# class HomePageTest(TestCase):

#     def test_home_page_only_saves_items_when_necessary(self):
#         request = HttpRequest()
#         home_page(request)
#         self.assertEqual(Item.objects.count(), 0)

    # def test_home_page_displays_all_list_items(self):
    #     Item.objects.create(text='itemey 1')
    #     Item.objects.create(text='itemey 2')

    #     request = HttpRequest()
    #     response = home_page(request)

    #     self.assertIn('itemey 1', response.content)
    #     self.assertIn('itemey 2', response.content)


class ListViewTest(TestCase):

    def test_uses_list_template(self):
        list_ = List.objects.create()
        response = self.client.get('/lists/%d/' % (list_.id,))
        self.assertTemplateUsed(response, 'list.html')

    def test_displays_only_itmes_for_that_list(self):
        list_corrected = List.objects.create()
        Item.objects.create(text='itemey 1', list=list_corrected)
        Item.objects.create(text='itemey 2', list=list_corrected)
        other_list = List.objects.create()
        Item.objects.create(text='other list item 1', list=other_list)
        Item.objects.create(text='other list item 2', list=other_list)

        response = self.client.get('/lists/%d/' % (list_corrected.id, ))

        self.assertContains(response, 'itemey 1')
        self.assertContains(response, 'itemey 2')
        self.assertNotContains(response, 'other list item 1')
        self.assertNotContains(response, 'other list item 2')

    def test_passes_correct_list_to_template(self):

        other_list = List.objects.create()
        list_corrected = List.objects.create()
        response = self.client.get('/lists/%d/' % (list_corrected.id,))
        self.assertEqual(response.context['list'], list_corrected)

class NewListTest(TestCase):

    def test_saving_a_POST_request(self):
        self.client.post(
            '/lists/new',
            data={'item_text': 'A new list item'})

        self.assertEqual(Item.objects.count(), 1)
        new_item = Item.objects.first()
        self.assertEqual(new_item.text, 'A new list item')

    def test_redirects_after_POST(self):
        response = self.client.post(
            '/lists/new',
            data={'item_text': 'A new list item'})

        # self.assertEqual(response.status_code, 302)
        # self.assertEqual(response['location'], '/lists/the-only-list-in-the-world/')
        new_list = List.objects.first()
        self.assertRedirects(response, 'lists/%d/' % (new_list.id,))


class NewItemTest(TestCase):

    def test_can_save_a_POST_request_to_an_existing_list(self):
        other_list = List.objects.create()
        list_corrected = List.objects.create()

        self.client.post(
            '/lists/%d/add_item' % (list_corrected.id,),
            data={'item_text': 'A new item for an existing list'})

        self.assertEqual(Item.objects.count(), 1)
        new_item = Item.objects.first()
        self.assertEqual(new_item.text, 'A new item for an existing list')
        self.assertEqual(new_item.list, list_corrected)

    def test_redirects_to_list_view(self):
        other_list = List.objects.create()
        list_corrected = List.objects.create()

        response = self.client.post(
            '/lists/%d/add_item' % (list_corrected.id,),
            data={'item_text': 'A new item for an existing list'})
        self.assertRedirects(response, '/lists/%d/' % (list_corrected.id,))





