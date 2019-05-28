from django import forms

from .models import Task, Comment
from datetimepicker.widgets import DateTimePicker


class TaskForm(forms.ModelForm):

    class Meta:
        model = Task
        fields = ('author','title','status','completion_date', )

        widgets = {
            'title': forms.TextInput(attrs={'class': 'textinputclass'}),
            'completion_date':forms.DateInput()


        }



class UpdateForm(forms.ModelForm):

    class Meta:
        model = Task
        fields = ('status','completion_date', )

        widgets = {

            'completion_date':forms.DateInput()


        }



class CommentForm(forms.ModelForm):

    class Meta:
        model = Comment
        fields = ( 'author','text',)

        widgets = {

            'text': forms.Textarea(attrs={'class': 'editable medium-editor-textarea'}),
        }
