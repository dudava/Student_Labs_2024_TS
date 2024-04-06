import json
import django.db
import django.core.exceptions


class Question(django.db.models.Model):
    question_type = ""
    question = django.db.models.CharField(max_length=200)
    order = django.db.models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.form.title}: {self.question}"
    
    class Meta:
        abstract = True


class MultipleChoicesQuestion(Question):
    def validate_list(value):
        try:
            value = json.loads(value)
        except:
            raise django.core.exceptions.ValidationError(
                f'{value} is not correct json format',
                params={'value': value},
            )
        if not isinstance(value, list):
            raise django.core.exceptions.ValidationError(
                f'{value} is not list',
                params={'value': value},
            )
    
    choices_list_string = django.db.models.CharField(max_length=300, validators=[validate_list])

    @property
    def choices_list(self):
        return json.loads(self.choices_list_string)

    class Meta:
        abstract = True


class FormManager(django.db.models.Manager):
    def get_queryset(self):
        return (
            super().get_queryset()
                   .prefetch_related('textquestions')
                   .prefetch_related('radioquestions')
                   .prefetch_related('checkboxquestions')
        )



class Form(django.db.models.Model):
    objects = FormManager()

    created = django.db.models.DateTimeField(auto_now_add=True)
    title = django.db.models.CharField(max_length=50)
    owner = django.db.models.ForeignKey('auth.User', related_name='forms', on_delete=django.db.models.CASCADE)

    def get_ordered_questions_list(self):
        questions_related = [
            self.textquestions,
            self.radioquestions, self.checkboxquestions
        ]

        questions = []
        for q_related in questions_related:
            for question in q_related.all():
                questions.append(question)
        return sorted(questions, key=lambda q: q.order)
        
    def __str__(self):
        return self.title
    

class TextQuestion(Question):
    question_type = 'text'
    correct_answer = django.db.models.CharField(max_length=100)
    form = django.db.models.ForeignKey(Form, related_name="textquestions", on_delete=django.db.models.CASCADE)


class RadioQuestion(MultipleChoicesQuestion):
    question_type = 'radio'
    correct_answer = django.db.models.CharField(max_length=100)
    form = django.db.models.ForeignKey(Form, related_name="radioquestions", on_delete=django.db.models.CASCADE)


class CheckboxQuestion(MultipleChoicesQuestion):
    question_type = 'checkbox'
    correct_answers_string = django.db.models.CharField(max_length=300, validators=[MultipleChoicesQuestion.validate_list])
    form = django.db.models.ForeignKey(Form, related_name="checkboxquestions", on_delete=django.db.models.CASCADE)

    @property
    def correct_answers_list(self):
        return json.loads(self.correct_answers_string)
    