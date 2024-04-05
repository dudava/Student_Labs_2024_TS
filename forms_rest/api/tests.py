import django.urls
import django.contrib.auth.models
import rest_framework.authtoken.models
import rest_framework.status
import rest_framework.test

from parameterized import parameterized

import api.models


class QuestionTestCase(rest_framework.test.APITestCase):
    list_url = ''
    test_data = {}

    def get_test_data(self):
        return self.test_data.copy()

    def setUp(self):
        self.owner = django.contrib.auth.models.User.objects.create_user(
            'test_user', 'test_user@mail.com', 'test_password'
        )
        self.client = rest_framework.test.APIClient()
        self.client.force_authenticate(user=self.owner)
        
        self.form = api.models.Form.objects.create(title='test_form', owner=self.owner)

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


class TextQuestionTestCase(QuestionTestCase):
    list_url = django.urls.reverse('text-question-list')
    test_data = {
        'question': 'test_question',
        'order': 1,
        'correct_answer': 'some_correct_answer',
        'form': 1,
    }

    @parameterized.expand([
        ('some_correct_answer', ),
    ])
    def test_valid_answer(self, correct_answer):
        valid_data = self.get_test_data()
        valid_data['correct_answer'] = correct_answer
        self.valid_create_test(self.list_url, valid_data, api.models.TextQuestion)

    @parameterized.expand([
        ('', ),
    ])
    def test_invalid_answer(self, correct_answer):
        invalid_data = self.get_test_data()
        invalid_data['correct_answer'] = correct_answer
        self.invalid_create_test(self.list_url, invalid_data, api.models.TextQuestion)

# Since the RadioQuestion and the CheckboxQuestion inherit the list of choices from a single model,
# we will provide tests on one of them, the RadioQuestion  
class MultipleChoiceTestCase(QuestionTestCase):
    list_url = django.urls.reverse('radio-question-list')
    test_data = {
        'question': 'test_question',
        'order': 1,
        'choices_list_string': None,
        "correct_answer": "choice_1",
        "form": 1,
    }

    @parameterized.expand([
        ('["choice_1", "choice_2"]', ),
    ])
    def test_valid_choices(self, choices):
        valid_data = self.get_test_data()
        valid_data['choices_list_string'] = choices
        self.valid_create_test(self.list_url, valid_data, api.models.RadioQuestion)

    @parameterized.expand([
        ('', ),
        ('[]', ),
        ('[" "]', ),
        ('["choice_1"]', ),
        ('[" ", " "]', ), 
    ])
    def test_invalid_choices(self, choices):
        invalid_data = self.get_test_data()
        invalid_data['choices_list_string'] = choices
        self.invalid_create_test(self.list_url, invalid_data, api.models.RadioQuestion)


class RadioQuestionTestCase(QuestionTestCase):
    list_url = django.urls.reverse('radio-question-list')
    test_data = {
        'question': 'test_question',
        'order': 1,
        'choices_list_string': '["choice_1", "choice_2"]',
        "correct_answer": "choice_1",
        "form": 1,
    }
    
    @parameterized.expand([
        ('choice_1', ),
    ])
    def test_valid_correct_answer(self, correct_answer):
        valid_data = self.get_test_data()
        valid_data['correct_answer'] = correct_answer
        self.valid_create_test(self.list_url, valid_data, api.models.RadioQuestion)

    @parameterized.expand([
        ('answer_not_in_choices', ),
        ('["choice_1", "choice_2"]', ),
    ])
    def test_invalid_correct_answer(self, correct_answer):
        invalid_data = self.get_test_data()
        invalid_data['correct_answer'] = correct_answer
        self.invalid_create_test(self.list_url, invalid_data, api.models.RadioQuestion)


class CheckboxQuestionTestCase(QuestionTestCase):
    list_url = django.urls.reverse('checkbox-question-list')
    test_data = {
        'question': 'test_question',
        'order': 1,
        'choices_list_string': '["choice_1", "choice_2", "choice_3"]',
        'correct_answers_string': '["choice_1", "choice_2"]',
        'form': 1,
    }
    
    @parameterized.expand([
        ('["choice_1"]', ),
        ('["choice_1", "choice_2"]', ),
    ])
    def test_valid_correct_answers(self, correct_answers):
        valid_data = self.get_test_data()
        valid_data['correct_answers_string'] = correct_answers
        self.valid_create_test(self.list_url, valid_data, api.models.CheckboxQuestion)
    
    @parameterized.expand([
        ('[]', ),
        ('choice_1', ),
        ('["answer_not_in_choices"]', ),
        ('["choice_1", "choice_2", "answer_not_in_choices"]', ),
    ])
    def test_invalid_correct_answers(self, correct_answers):
        invalid_data = self.get_test_data()
        invalid_data['correct_answers_string'] = correct_answers
        self.invalid_create_test(self.list_url, invalid_data, api.models.CheckboxQuestion)
