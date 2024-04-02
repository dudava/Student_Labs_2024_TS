import rest_framework.serializers
import json

import api.models


class QuestionBaseSerializer(rest_framework.serializers.ModelSerializer):
    question_type = rest_framework.serializers.CharField(
        max_length=10, read_only=True
    )


class TextQuestionSerializer(QuestionBaseSerializer):
    class Meta:
        model = api.models.TextQuestion
        fields = ('id', 'question_type', 'question',
                  'order', 'correct_answer', 'form')

class MultipleChoicesQuestionSerializer(QuestionBaseSerializer):
    def validate(self, data):
        choices = json.loads(data['choices_list_string'])
        if len(choices) <= 1:
            raise rest_framework.serializers.ValidationError(
                'Choices list is empty or has a length of 1'
            )


class RadioQuestionSerializer(MultipleChoicesQuestionSerializer):
    class Meta:
        model = api.models.RadioQuestion
        fields = ('id', 'question_type', 'question', 'order',
                  'choices_list_string', 'correct_answer', 'form')

    def validate(self, data):
        super().validate(data)
        choices = json.loads(data['choices_list_string'])
        if data['correct_answer'] not in choices:
            raise rest_framework.serializers.ValidationError(
                'Correct answer not in choices'
            )
        return data


class CheckboxQuestionSerializer(MultipleChoicesQuestionSerializer):
    class Meta:
        model = api.models.CheckboxQuestion
        fields = ('id', 'question_type', 'question', 'order',
                  'choices_list_string', 'correct_answers_string', 'form')

    def validate(self, data):
        super().validate(data)
        choices = set(json.loads(data['choices_list_string']))
        correct_answers = set(json.loads(data['correct_answers_string']))
        if len(correct_answers) == 0:
            raise rest_framework.serializers.ValidationError(
                'List of correct answers is empty'
            )
        if not set(correct_answers).issubset(set(choices)):
            raise rest_framework.serializers.ValidationError(
                'Not all the correct answers in choices'
            )
        return data


class FormSerializer(rest_framework.serializers.ModelSerializer): 
    class Meta:
        model = api.models.Form
        fields = ('id', 'title')
