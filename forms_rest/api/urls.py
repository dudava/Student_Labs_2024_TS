import django.urls
import rest_framework.routers
import rest_framework.urlpatterns

import api.views

router = rest_framework.routers.DefaultRouter()
router.register(r'questions/text', api.views.TextQuestionViewSet, basename='text-question')
router.register(r'questions/radio', api.views.RadioQuestionViewSet, basename='radio-question')
router.register(r'questions/checkbox', api.views.CheckboxQuestionViewSet, basename='checkbox-question')
router.register(r'forms', api.views.FormViewSet, basename='form'),

urlpatterns = [
    django.urls.path('', django.urls.include(router.urls)),
]
