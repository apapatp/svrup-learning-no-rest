from django import forms
from .models import Comment
from crispy_forms.helper import FormHelper # Form helper
from crispy_forms.layout import Submit

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('text','user','path',)

# other approach not using models
class CommentForm(forms.Form):
    comment = forms.CharField(
    widget=forms.Textarea(attrs={"placeholder": "Add Comment or Your Commen or Reply"}))

    def __init__(self, data=None, files=None, **kwargs):
        super(CommentForm, self).__init__(data, files, kwargs)
        self.helper = FormHelper()
        self.helper.form_show_labels = False # hide labels on initialize
        self.helper.form_method = "POST"
        # self.helper.form_action = ""
        self.helper.add_input(Submit('submit', 'Comment' ,css_class='btn btn-primary',))
