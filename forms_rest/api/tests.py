import django.urls
import rest_framework.status
import rest_framework.test

import api.models


def valid_create_test(self, url, data, model_class):
    response = self.client.post(
        url, data, format='json',
    )
    self.assertEqual(
        response.status_code,
        rest_framework.status.HTTP_201_CREATED,
    )
    self.assertEqual(
        model_class.objects.count(), 1
    )
    

def invalid_create_test(self, url, data, model_class):
    response = self.client.post(
        url, data, format='json',
    )
    self.assertEqual(
        response.status_code,
        rest_framework.status.HTTP_400_BAD_REQUEST,
    )
    self.assertEqual(
        model_class.objects.count(), 0,
    )


class RadioQuestionTestCase(rest_framework.test.APITestCase):
    list_url = django.urls.reverse('radio-question-list')
    
    def setUp(self):
        api.models.Form.objects.create(title='test_form')

    def test_valid_correct_answer(self):
        valid_data = {
            'question': 'test_question',
            'order': 1,
            'choices_list_string': '["choice_1", "choice_2"]',
            "correct_answer": "choice_1",
            "form": 1,
        }
        valid_create_test(self.list_url, valid_data, api.models.RadioQuestion)

    def test_invalid_correct_answer(self):
        invalid_data = {
            'question': 'test_question',
            'order': 1,
            'choices_list_string': '["choice_1", "choice_2"]',
            "correct_answer": "choice_not_in_choices",
            "form": 1,
        }
        invalid_create_test(self.list_url, invalid_data, api.models.RadioQuestion)


class CheckboxQuestionTestCase(rest_framework.test.APITestCase):
    list_url = django.urls.reverse('checkbox-question-list')

    def setUp(self):
        api.models.Form.objects.create(title='test_form')

    def test_valid_correct_answers_1(self):
        valid_data = {
            'question': 'test_question',
            'order': 1,
            'choices_list_string': '["choice_1", "choice_2", "choice_3"]',
            'correct_answers': '["choice_1"]',
            'form': 1,
        }
        valid_create_test(self.list_url, valid_data, api.models.RadioQuestion)
    
    def test_invalid_correct_answers(self):
        invalid_data = {
            'question': 'test_question',
            'order': 1,
            'choices_list_string': '["choice_1", "choice_2"]',
            "correct_answer": "choice_not_in_choices",
            "form": 1,
        }