from django import forms
from comments.models import HodsComment
from gt_logs.models import GtLog



Grade_CHOICES =(
    ("1", "1"),
    ("2", "2"),
    ("3", "3"),
    ("4", "4"),
    ("5", "5"),
    ("6", "6"),
    ("7", "7"),
    ("8", "8"),
    ("9", "9"),
    ("10", "10"),
)


class HodCommentForm(forms.ModelForm):

    # hod_gt_score = forms.ChoiceField(
    #     choices = Grade_CHOICES,
    #     label='Select score for trainee',
    #     widget=forms.Select(attrs={'class': 'form-control',}),
    # )

    class Meta:
        model = HodsComment
        fields =[ 'comment', ]

#         comment
# hod
# managers_comment


        widgets = {
            'comment': forms.Textarea(attrs={'rows': 5,'cols':20, 'class':'form-control', 'place-holder':'type in your comment here...'}),
        }

        labels = {
                'comment': 'Give remarks on Trainee',

        }