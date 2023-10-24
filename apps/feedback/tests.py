from django.test import TestCase
from django.contrib.auth.models import User
from apps.feedback.models import Feedback

from django.test import TestCase
from django.urls import reverse


# class FeedbackModelTest(TestCase):
#
#     def test_feedback_model(self):
#         user = User.objects.create(username="testuser", email="test@example.com")
#         feedback = Feedback.objects.create(user=user, content="This is a test feedback", page_url="http://example.com")
#         self.assertEqual(str(feedback), f"Feedback {feedback.pk}")
#         self.assertEqual(feedback.user, user)


class FeedbackViewTest(TestCase):

    # def test_submit_feedback(self):
    #     url = reverse('feedback:submit-feedback')
    #     response = self.client.post(url, {'content': 'Example feedback being sent', 'page_url': 'http://example.com'})
    #     self.assertEqual(response.status_code, 200)

    def test_empty_feedback(self):
        url = reverse('feedback:submit-feedback')
        response = self.client.post(url, {'page_url': 'http://example.com'})
        self.assertEqual(response.status_code, 500)




# class FeedbackViewTest(TestCase):
#
#     def test_submit_feedback(self):
#         url = reverse('feedback:submit-feedback')
#         response = self.client.post(url, {'content': 'Example feedback being sent', 'page_url': 'http://example.com'})
#         self.assertEqual(response.status_code, 200)