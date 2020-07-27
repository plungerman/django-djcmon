from django import forms

from djtools.fields import TODAY

CLASS = [(x, x) for x in reversed(range(1926, TODAY.year + 4))]
CLASS.insert(0, ('','-----'))
RELATION_CHOICES = (
    ('', '--Select--'),
    ('Alumni', 'Alumni'),
    ('Community member', 'Community member'),
    ('Faculty member', 'Faculty member'),
    ('Friend of the college', 'Friend of the College'),
    ('Parent', 'Parent'),
    ('Staff member', 'Staff member'),
    ('Student', 'Student'),
)


class ManagerForm(forms.Form):
    first_name = forms.CharField(max_length=128)
    last_name = forms.CharField(max_length=128)
    email = forms.EmailField(label="Email")
    relation = forms.ChoiceField(
        label="Are you a ...",
        choices=RELATION_CHOICES,
    )
    address = forms.CharField(
        widget=forms.Textarea,
        required=False,
        max_length=255,
    )
    class_of = forms.ChoiceField(
        label="Class of", required=False, choices=CLASS,
    )
