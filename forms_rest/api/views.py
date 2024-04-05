import rest_framework.decorators
import rest_framework.generics
import rest_framework.permissions
import rest_framework.response
import rest_framework.reverse
import rest_framework.viewsets

import api.models
import api.permissions
import api.serializers


class QuestionBaseViewSet(rest_framework.viewsets.ModelViewSet):
    permission_classes = [
        rest_framework.permissions.IsAuthenticatedOrReadOnly,
        api.permissions.IsFormOwnerOrReadonly,
    ]


class TextQuestionViewSet(QuestionBaseViewSet):
    queryset = api.models.TextQuestion.objects.all()
    serializer_class = api.serializers.TextQuestionSerializer
    

class RadioQuestionViewSet(QuestionBaseViewSet):
    queryset = api.models.RadioQuestion.objects.all()
    serializer_class = api.serializers.RadioQuestionSerializer


class CheckboxQuestionViewSet(QuestionBaseViewSet):
    queryset = api.models.CheckboxQuestion.objects.all()
    serializer_class = api.serializers.CheckboxQuestionSerializer


class FormViewSet(rest_framework.viewsets.ModelViewSet):
    queryset = api.models.Form.objects.all()
    serializer_class = api.serializers.FormSerializer
    permission_classes = [
        rest_framework.permissions.IsAuthenticatedOrReadOnly,
        api.permissions.IsOwnerOrReadonly,
    ]

    @rest_framework.decorators.action(detail=True)
    def qlist(self, request, *args, **kwargs):
        form = self.get_object()
        questions = form.get_ordered_questions_list()
        question_serializers = {
            'text': api.serializers.TextQuestionSerializer,
            'radio': api.serializers.RadioQuestionSerializer,
            'checkbox': api.serializers.CheckboxQuestionSerializer,
        }
        serialized_questions = [
            question_serializers[q.question_type](q).data for q in questions
        ]

        return rest_framework.response.Response(
            serialized_questions
        )
    
    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)
