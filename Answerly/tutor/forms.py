from django.forms import ModelForm
from .models import Tutor, Message


class TutorForm(ModelForm):
    class Meta:
        model = Tutor
        fields = "__all__"
        exclude = ['user']

class MessageForm(ModelForm):
    class Meta:
        model = Message
        fields = "__all__"
        exclude = ['sender']