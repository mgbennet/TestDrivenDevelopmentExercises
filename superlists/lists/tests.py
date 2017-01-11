from django.test import TestCase
from django.http import HttpRequest

from lists.views import home_page
from lists.models import Item


class HomePageTest(TestCase):
    def test_home_page_returns_correct_http(self):
        response = self.client.get("/")
        self.assertTemplateUsed(response, "home.html")

    def test_home_page_can_save_a_POST_request(self):
        request = HttpRequest()
        request.method = "POST"
        request.POST["item_text"] = "A new list item"

        response = home_page(request)

        self.assertEquals(Item.objects.count(), 1)
        newest_item = Item.objects.first()
        self.assertEquals(newest_item.text, "A new list item")

    def test_home_page_redirects_after_POST(self):
        request = HttpRequest()
        request.method = "POST"
        request.POST["item_text"] = "A new list item"

        response = home_page(request)

        self.assertEqual(response.status_code, 302)
        self.assertEqual(response['location'], '/')

    def test_home_page_only_saves_items_when_necessary(self):
        request = HttpRequest()
        home_page(request)
        self.assertEqual(Item.objects.count(), 0)

    def test_home_page_displays_all_list_items(self):
        Item.objects.create(text="item1")
        Item.objects.create(text="item2")

        request = HttpRequest()
        response = home_page(request)

        self.assertIn("item1", response.content.decode("utf8"))
        self.assertIn("item2", response.content.decode("utf8"))



class ItemModelTest(TestCase):
    def test_saving_and_retrieving_items(self):
        first_item = Item()
        first_item.text = "The first (ever) list item"
        first_item.save()

        second_item = Item()
        second_item.text = "Item the second"
        second_item.save()

        saved_items = Item.objects.all()
        self.assertEqual(saved_items.count(), 2)

        first_saved_item = saved_items[0]
        second_saved_item = saved_items[1]
        self.assertEqual(first_saved_item.text, "The first (ever) list item")
        self.assertEqual(second_saved_item.text, "Item the second")