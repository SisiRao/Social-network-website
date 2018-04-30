from django import forms
from OOTD.models import *
from OOTD.choice import *

MAX_UPLOAD_SIZE = 5000000


class RegistrationForm(forms.Form):
    first_name = forms.CharField(max_length=20)

    last_name  = forms.CharField(max_length=20)
    email      = forms.CharField(max_length=50,
                                 widget = forms.EmailInput())
    username   = forms.CharField(max_length = 20)
    password1  = forms.CharField(max_length = 200, 
                                 label='Password', 
                                 widget = forms.PasswordInput())
    password2  = forms.CharField(max_length = 200, 
                                 label='Confirm password',  
                                 widget = forms.PasswordInput())
    longitude = forms.FloatField(widget=forms.HiddenInput())
    latitude = forms.FloatField(widget=forms.HiddenInput())

    # Customizes form validation for properties that apply to more
    # than one field.  Overrides the forms.Form.clean function.
    def clean(self):
        # Calls our parent (forms.Form) .clean function, gets a dictionary
        # of cleaned data as a result
        cleaned_data = super(RegistrationForm, self).clean()

        # Confirms that the two password fields match
        password1 = cleaned_data.get('password1')
        password2 = cleaned_data.get('password2')
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords do not match.")

        # We must return the cleaned data we got from our parent.
        return cleaned_data

    # Customizes form validation for the username field.
    def clean_username(self):
        # Confirms that the username is not already present in the
        # User model database.
        username = self.cleaned_data.get('username')
        email = self.cleaned_data.get('email')
        if User.objects.filter(username__exact=username):
            raise forms.ValidationError("Username is already taken.")
        if User.objects.filter(email__exact=email):
            raise forms.ValidationError("Email is already used.")
        # We must return the cleaned data we got from the cleaned_data
        # dictionary
        return username


class PasswordEditForm_forget(forms.Form):
    password = forms.CharField(max_length=200,
                               label='Password',
                               widget=forms.PasswordInput())
    confirm_pass = forms.CharField(max_length=200,
                                   label='Confirm password',
                                   widget=forms.PasswordInput())

    def clean(self):
        cleaned_data = super(PasswordEditForm_forget, self).clean()
        password = cleaned_data.get('password')
        confirm_pass = cleaned_data.get('confirm_pass')

        if password and confirm_pass and password != confirm_pass:
            raise forms.ValidationError("Passwords did not match!")
        
        return cleaned_data



class filterForm(forms.Form):
    gender = forms.ChoiceField(choices = GENDER_CHOICES, label = "Gender",required=False)
    season = forms.ChoiceField(choices = SEASON_CHOICES, label = "Season",required=False)
    # height = forms.ChoiceField(choices = HEIGHT_CHOICES, label = "Height",required=False)
    size   = forms.ChoiceField(choices = SIZE_CHOICES,   label = "Size",  required=False)
    color  = forms.ChoiceField(choices = COLOR_CHOICES,  label = "Color", required=False)
    brand  = forms.ChoiceField(choices = BRAND_CHOICES,  label = "Brand", required=False)



MAX_UPLOAD_SIZE = 2500000
class EditProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = {
            'bio',
            'picture',
            'occupation',
            'longitude',
            'latitude'
        }
        widgets = {
                'longitude': forms.HiddenInput(),
                'latitude': forms.HiddenInput()
            }

    def clean_picture(self):
        picture = self.cleaned_data['picture']
        if not picture:
            raise forms.ValidationError('You must upload a picture')
        else:
            if not picture.content_type or not picture.content_type.startswith('image'):
                raise forms.ValidationError('File type is not image')
            if picture.size > MAX_UPLOAD_SIZE:
                raise forms.ValidationError('File too big (max size is {0} bytes)'.format(MAX_UPLOAD_SIZE))
        return picture



class outfitForm(forms.ModelForm):
    class Meta:
        model = Outfit
        fields = ('picture', 'gender', 'height', 'season', 'publicity', 'description')
        widgets = {
            'description': forms.Textarea(),
        }


class clothesForm(forms.ModelForm):
    class Meta:
        model = Clothes

        fields = ('picture', 'gender', 'color', 'category', 'price', 'size', 'brand', 'url', 'description', 'detail')
        widgets = {
            'detail': forms.Textarea(),
            'description': forms.Textarea(),
        }

# class filterForm(forms.ModelForm):
#     class Mata:
#         model = Outfit
#         fields = ('gender', 'season','height','description')
#         widgets = {
#             'description': forms.Textarea(),
#         }




