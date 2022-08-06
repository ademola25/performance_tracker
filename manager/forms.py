from django import forms
from comments.models import ManagersComment
from gt_logs.models import GtLog


class TraineeLogForm(forms.ModelForm):

    class Meta:
        model = GtLog
        fields =[ 'log', 'saved']


        widgets = {
            'log': forms.Textarea(attrs={'rows': 5,'cols':20, 'class':'form-control', 'place-holder':'type in your log here...'}),
            'saved': forms.CheckboxInput(attrs={'class':'form-control'}),
        }

        labels = {
                'log': 'Log your activities here',
                'saved':'Click for final submission'
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
        fields =[ 'gt_score',]


