from django import forms
from .models import comment

class comment_form(forms.ModelForm):

    class Meta:
        model=comment
        fields=['subject','comment_text']
        labels={'comment_text':'متن نظر','subject':'عنوان نظر'}
        widgets={'comment_text':forms.Textarea()}
