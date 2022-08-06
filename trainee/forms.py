from django import forms
from department.models import Department, DepartmentTrainee
from gt_logs.models import GtLog
from numbers_of_days.models import NumbersOfDays

 
class TraineeLogForm(forms.ModelForm):
    class Meta:
        model = GtLog
        fields =[ 'log', ]
        widgets = {
            'log': forms.Textarea(attrs={'rows': 5,'cols':20, 'class':'form-control', 'place-holder':'type in your log here...'}),
            # 'saved': forms.CheckboxInput(attrs={'class':'form-control'}),
        }
        labels = {
                'log': 'Log your activities here',
                # 'saved':'Click for final submission'
        }

# class Kpifor
    


class TraineeLogUpdateForm(forms.ModelForm):
    # create meta class
    class Meta:
        # specify model to be used
        model = GtLog
        # specify fields to be used
        fields =[ 'log',]

        widgets = {
            'log': forms.Textarea(attrs={'rows': 5,'cols':20, 'class':'form-control', 'place-holder':'type in your log here...'}),
        }
        labels = {
                'log': 'Edit your Log',
                # 'saved':'Click for final submission'
        }



class LogPastDaysCalenderForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user')
        super(LogPastDaysCalenderForm, self).__init__(*args, **kwargs)
        self.fields['departments'].queryset =Department.objects.filter(trainees=user).values_list('department_name', flat=True)


    # create meta class
    departments = forms.ModelChoiceField(
        queryset=None,
        label='Select Department',
        widget=forms.Select(attrs={'class': 'form-control',}),
    )

    class Meta:
        model = GtLog
        fields =['log']


        widgets = {
            'departments': forms.Textarea(attrs={'rows': 5,'cols':20, 'class':'form-control', 'place-holder':'type in your log here...'}),
            'log': forms.Textarea(attrs={'rows': 5,'cols':20, 'class':'form-control', 'place-holder':'type in your log here...'}),
            # 'saved': forms.CheckboxInput(attrs={'class':'form-control'}),
        }
        labels = {
                'log': 'Log your activities here',
                # 'saved':'Click for final submission'
        }







class LogPastDaysForm(forms.ModelForm):

    # def __init__(self, *args, **kwargs):
    #     user = kwargs.pop('user')
    #     super(LogPastDaysForm, self).__init__(*args, **kwargs)
    #     self.fields['departments'].queryset =Department.objects.filter(department_departmenttrainees__trainee = user)

    # create meta class
    # departments = forms.ModelChoiceField(
    #     queryset=None,
    #     label='Select Department',
    #     widget=forms.Select(attrs={'class': 'form-control',}),
    # )
    class Meta:
        model = GtLog
        fields =['log']


        widgets = {
            'departments': forms.Textarea(attrs={'rows': 5,'cols':20, 'class':'form-control', 'place-holder':'type in your log here...'}),
            'log': forms.Textarea(attrs={'rows': 5,'cols':20, 'class':'form-control', 'place-holder':'type in your log here...'}),
            # 'saved': forms.CheckboxInput(attrs={'class':'form-control'}),
        }
        labels = {
                'log': 'Log your activities here',
                # 'saved':'Click for final submission'
        }



