from django import forms
from .models import Airport, AirportRoute


class AirportRouteForm(forms.ModelForm):
    """
    Form to add an Airport Route with fields:
    - Parent Airport Node
    - Child Airport Node
    - Position (Left / Right)
    - Duration (Time taken to reach this airport)
    """
    
    class Meta:
        model = AirportRoute
        fields = ['parent', 'child', 'position', 'duration']
        widgets = {
            'parent': forms.Select(attrs={
                'class': 'form-control',
                'required': True
            }),
            'child': forms.Select(attrs={
                'class': 'form-control',
                'required': True
            }),
            'position': forms.Select(attrs={
                'class': 'form-control',
                'required': True
            }),
            'duration': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': 1,
                'required': True,
                'placeholder': 'Duration in minutes'
            })
        }
        labels = {
            'parent': 'Parent Airport Node',
            'child': 'Child Airport Node',
            'position': 'Position',
            'duration': 'Duration (minutes)'
        }
        help_texts = {
            'parent': 'Select the starting airport',
            'child': 'Select the destination airport',
            'position': 'Choose Left or Right direction',
            'duration': 'Time taken to reach this airport'
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Order airports alphabetically for better UX
        self.fields['parent'].queryset = Airport.objects.all().order_by('name')
        self.fields['child'].queryset = Airport.objects.all().order_by('name')

    def clean(self):
        cleaned_data = super().clean()
        parent = cleaned_data.get('parent')
        child = cleaned_data.get('child')
        position = cleaned_data.get('position')

        # Prevent self-referencing routes
        if parent and child and parent == child:
            raise forms.ValidationError(
                "Parent and Child airports cannot be the same."
            )

        # Check if this position already exists for the parent
        if parent and position:
            existing_route = AirportRoute.objects.filter(
                parent=parent,
                position=position
            )
            # Exclude current instance if updating
            if self.instance.pk:
                existing_route = existing_route.exclude(pk=self.instance.pk)
            
            if existing_route.exists():
                raise forms.ValidationError(
                    f"A route already exists for {parent.name} in the {self.instance.get_position_display() if self.instance.pk else position} direction."
                )

        return cleaned_data


class SearchForm(forms.Form):
    """
    Search form for Task 1: Find the Last Reachable Airport Node
    Allows user to select a starting airport and direction (Left or Right)
    """
    airport = forms.ModelChoiceField(
        queryset=Airport.objects.all().order_by('name'),
        label='Starting Airport Node',
        widget=forms.Select(attrs={
            'class': 'form-control',
            'required': True
        }),
        help_text='Select the airport to start traversal from'
    )
    
    direction = forms.ChoiceField(
        choices=AirportRoute.POSITION_CHOICES,
        label='Direction',
        widget=forms.Select(attrs={
            'class': 'form-control',
            'required': True
        }),
        help_text='Choose Left or Right direction to traverse'
    )
