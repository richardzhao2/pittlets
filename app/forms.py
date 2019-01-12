from django import forms
from .models import Listing, Image
from django.contrib.auth.forms import UserCreationForm
from django.forms import formset_factory

class ListingForm(forms.ModelForm, forms.Form):
    typeChoice = [('Sublet', 'Sublet'), ('Pass on Lease', 'Pass on Lease')]
    type = forms.ChoiceField(choices = typeChoice, widget = forms.RadioSelect())
    amenities = forms.MultipleChoiceField(
        choices=[('AC','Air-Conditioning'), ('Doorman','Doorman'), ('Furnished', 'Furnished'),
                 ('Utilities', 'Utilities Included'), ('Wifi', 'Wifi'), ('Laundry', 'Washer/Dryer'), ('Pets', 'Pets Allowed'), ('Gym', 'Gym')],  # this is optional
        widget=forms.CheckboxSelectMultiple(attrs={'class': 'new_form'}),
    )
    # need to integrate amenities with the new model
    class Meta:
        model = Listing
        widgets = {
            'description': forms.Textarea(
                attrs={'placeholder': 'Enter your description here'}),
        }
        fields = [
            'title',
            'description',
            'size',
            'address',
            'price',
            'prorated',
        ]

class SignUpForm(UserCreationForm):
    email = forms.EmailField(max_length=254, help_text='Required. Inform a valid email address.')
    username = forms.CharField(max_length=20)


    # First checks validity of super user, then checks if the email supplied is a valid .edu address
    def is_valid(self):
        valid = super(UserCreationForm, self).is_valid()

        if not valid:
            return valid

        if '.edu' not in self.data['email']:
            return False

        return True


class ImageForm(forms.ModelForm):
    image = forms.ImageField(label = 'image')
    class Meta:
        model = Image
        fields = ('image', )

class filterForm(forms.Form):
    typeChoice = [('Sublet', 'Sublet'), ('Pass on Lease', 'Pass on Lease')]
    type = forms.ChoiceField(choices=typeChoice, widget=forms.RadioSelect())
    amenities = forms.MultipleChoiceField(
        choices=[('AC', 'Air-Conditioning'), ('Doorman', 'Doorman'), ('Furnished', 'Furnished'),
                 ('Utilities', 'Utilities Included'), ('Wifi', 'Wifi'), ('Laundry', 'Washer/Dryer'),
                 ('Pets', 'Pets Allowed'), ('Gym', 'Gym')],  # this is optional
        widget=forms.CheckboxSelectMultiple(attrs={'class': 'new_form'}),
    )