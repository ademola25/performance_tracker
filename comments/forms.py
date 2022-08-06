from django import forms
from comments.models import CommentTrail, ManagersComment
from gt_logs.models import GtLog
from numbers_of_days.models import NumbersOfDays


class ManagersCommentForm(forms.ModelForm):
    class Meta:
        model = ManagersComment
        fields =[ 'comment',]
        widgets = {
            'comment': forms.Textarea(attrs={'rows': 5,'cols':20, 'class':'form-control', 'place-holder':'type in your log here...'}),
        }

        labels = {
                # 'comment': 'Log your activities here',
                # 'saved':'Click for final submission'
        }


class ManagersCommentTrailForm(forms.ModelForm):
    class Meta:
        model = CommentTrail
        fields =[ 'comment',]
        widgets = {
            'comment': forms.Textarea(attrs={'rows': 5,'cols':20, 'class':'form-control', 'place-holder':'type in your log here...'}),
        }

        labels = {
                # 'comment': 'Log your activities here',
                # 'saved':'Click for final submission'
        }




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


class ManagerGradingForm(forms.ModelForm):
    gt_score = forms.ChoiceField(
        choices = Grade_CHOICES,
        label='Select score for trainee',
        widget=forms.Select(attrs={'class': 'form-control',}),
    )

    class Meta:
        model = ManagersComment
        fields =[ 'gt_score', 'comment',]



        widgets = {
            'comment': forms.Textarea(attrs={'rows': 5,'cols':20, 'class':'form-control', 'place-holder':'type in your log here...'}),
        }









class NumbersOfDaysForm(forms.ModelForm):

    class Meta:
        model = NumbersOfDays
        fields =[ 'managers_overall_comment',]


        widgets = {
            'managers_overall_comment': forms.Textarea(attrs={'rows': 5,'cols':20, 'class':'form-control', 'place-holder':'type in your log here...'}),
            # 'saved': forms.CheckboxInput(attrs={'class':'form-control'}),
        }

        labels = {
                'managers_overall_comment': 'Comment on Trainees performance',
                # 'saved':'Click for final submission'
        }




