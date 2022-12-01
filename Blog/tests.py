from django.test import TestCase


# test Ticket_creation view
class Ticket_creation(TestCase):
    def test_ticket_creation(self):
        #test ticket creation
        response = self.client.get('/blog/ticket_creation/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'Blog/ticket_creation.html')

    def test_ticket_creation_post(self):
        #test ticket creation post
        response = self.client.post('/blog/ticket_creation/', {'title': 'test_ticket', 'description': 'test_description', 'image': 'test_image'})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'Blog/ticket_creation.html')
