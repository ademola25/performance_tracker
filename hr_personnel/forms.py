from django import forms
from accounts.models import User

from department.models import Department
from hod.models import Hod
from manager.models import Manager
from .models import Batch
from gt_hr import settings
from hr_personnel.utils import validate_file_extension
from accounts.models import User


class BatchForm(forms.ModelForm):

    csv_file = forms.FileField(
        label='Upload csv file',
        widget=forms.FileInput(attrs={
                               'class': 'form-control', 'accept': '.csv'}),
        validators=[validate_file_extension],
    )
    batch_name = forms.CharField(
        label='Fill in a name for batch',
        widget=forms.TextInput(attrs={'class': 'form-control', }),
    )

    month_year = forms.DateField(
        
        label='Batch Month and Year',
        widget=forms.DateInput(
            format="%d/%m/%Y",
            attrs={'class': 'form-control','placeholder': 'Select a date','type': 'date'}),
    )
    class Meta:
        model = Batch
        fields = ['batch_name', 'csv_file', 'month_year', ]

    def clean_csv_file(self):
        uploaded_csv_file = self.cleaned_data['csv_file']

        if uploaded_csv_file:
            filename = uploaded_csv_file.name
            if filename.endswith(settings.FILE_UPLOAD_TYPE):
                if uploaded_csv_file.size < int(settings.MAX_UPLOAD_SIZE):
                    return uploaded_csv_file   # Here
                else:
                    raise forms.ValidationError(
                        "File size must not exceed 5 MB")
            else:
                raise forms.ValidationError("Please upload .csv extension files only")

        return uploaded_csv_file


class createDepartmentForm(forms.ModelForm):

    department_name = forms.CharField(
        label='Fill in a name for department',
        widget=forms.TextInput(attrs={'class': 'form-control', }),
    )
    key_objective = forms.CharField(
        label='Fill in Key objectsives',
        widget=forms.Textarea(attrs={'rows': 5,'cols':20, 'class':'form-control', 'place-holder':'type in your log here...'}),
    )

    class Meta:
        model = Department
        fields = ['department_name',
                  'key_objective']


class createHodForm(forms.ModelForm):

    name = forms.CharField(
        label='Fill in a name for hod',
        widget=forms.TextInput(attrs={'class': 'form-control', }),
    )
    email = forms.EmailField(
        label='Fill in an email for hod',
        widget=forms.EmailInput(attrs={'class': 'form-control', }),
    )

    staff_id = forms.CharField(
        label='Enter staff Id',
        widget=forms.TextInput(attrs={'class': 'form-control', }),
    )
    department = forms.ModelChoiceField(
        queryset=Department.objects.filter(department_departmenthod__isnull=True),
        label='Select Department',
        widget=forms.Select(attrs={'class': 'form-control',}),
    )


    class Meta:
        model = User
        fields = ['name',
                  'email',
                  'staff_id',
                  
                  ]


class createManagerForm(forms.ModelForm):
    staff_id = forms.CharField(
        label='Staff Id',
        widget=forms.TextInput(attrs={'class': 'form-control', }),
    )
    
    name = forms.CharField(
        label='Manager name',
        widget=forms.TextInput(attrs={'class': 'form-control', }),
    )
    email = forms.EmailField(
        label='Manager email',
        widget=forms.TextInput(attrs={'class': 'form-control', }),
    )

    
    department = forms.ModelChoiceField(
        queryset=Department.objects.filter(department_departmentmanagers__isnull=True),
        label='Select Department',
        widget=forms.Select(attrs={'class': 'form-control',}),
    )




    class Meta:
        model = User
        fields = ['staff_id','name', 'email', 'department']




class DepartmentEditForm(forms.ModelForm):
    

    department_name = forms.CharField(
       label='Fill in a name for department',
       widget=forms.TextInput(attrs={'class': 'form-control',}),
    )

    key_objective = forms.CharField(
        label='Fill in Key objectsives',
        widget=forms.Textarea(attrs={'rows': 5,'cols':20, 'class':'form-control', 'place-holder':'type in your log here...'}),
    )


    class Meta:
        model = Department
        fields =[ 'department_name', 'key_objective'
          ]




class UserEditForm(forms.ModelForm):
    name = forms.CharField(
       label='Edit name of user',
       widget=forms.TextInput(attrs={'class': 'form-control py-10',}),
    )

    email = forms.EmailField(
        label='Edit email',
        widget=forms.EmailInput(attrs={'class': 'form-control',}),
    )
    class Meta:
        model = User
        fields =[ 'name', 'email' ]






