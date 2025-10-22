from django import forms
from .models import Employee


class EmployeeForm(forms.ModelForm):
    first_name = forms.CharField(max_length=100)
    last_name = forms.CharField(max_length=100)
    email = forms.EmailField()
    
    class Meta:
        model = Employee
        fields = [
             'first_name', 'last_name', 'email', 'phone',
            'department', 'position', 'join_date', 'status',
            'address', 'profile_picture'
        ]

        widgets = {
            'phone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter phone number'}),
            'status': forms.Select(attrs={'class': 'form-control'}),
            'join_date': forms.DateInput(attrs={'type': 'date'}),
            'address': forms.Textarea(attrs={'rows': 3}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance and self.instance.pk:
            self.fields['first_name'].initial = self.instance.user.first_name
            self.fields['last_name'].initial = self.instance.user.last_name
            self.fields['email'].initial = self.instance.user.email
    
    def save(self, commit=True):
        employee = super().save(commit=False)
        
        # Update user fields
        if not employee.pk:
            # Creating a new employee
            from authentication.models import User
            username = self.cleaned_data['email'].split('@')[0]
            user = User.objects.create_user(
                username=username,
                email=self.cleaned_data['email'],
                password='temp123',
                first_name=self.cleaned_data['first_name'],
                last_name=self.cleaned_data['last_name'],
                user_type='employee'
            )
            employee.user = user
        else:
            # Updating an existing employee
            employee.user.first_name = self.cleaned_data['first_name']
            employee.user.last_name = self.cleaned_data['last_name']
            employee.user.email = self.cleaned_data['email']
            employee.user.save()
        
        if commit:
            employee.save()
        return employee