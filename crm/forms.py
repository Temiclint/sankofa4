from django import forms
from django.contrib.auth.models import Group, User, Permission 
from .models import *


class TimeInput(forms.TimeInput):
    input_type = 'time'

class DateInput(forms.DateInput):
    input_type = 'date'


class RoleForm(forms.ModelForm):
    class Meta:
        model = Group
        fields = ('name',)
        
        


class ProfileForm(forms.ModelForm):

    class Meta:

        model = Profile
        fields = ('image',)


class UserCreationForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email', 'password')



class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email')
        widgets = {
            'email' : forms.EmailInput(attrs={'readonly': 'readonly'})
        }
        

class CompanyCategoryForm(forms.ModelForm):

    class Meta:

        model = CompanyCategory
        fields = ('status', 'name')
        
        
class EventCategoryForm(forms.ModelForm):

    class Meta:

        model = EventCategory
        fields = ('status', 'name')
        
        
class CompanyForm(forms.ModelForm):
    phone_number = forms.RegexField(regex=r'^\+?1?\d{9,15}$')
    
    class Meta:

        model = Company
        fields = ('name', 'logo', 'category', 'background_info', 'phone_number', 'website', 'skype', 'address', 'city', 'zip_code', 'state', 'country')


class ContactForm(forms.ModelForm):
    phone_number = forms.RegexField(regex=r'^\+?1?\d{9,15}$')

    class Meta:

        model = Contact
        fields = ('role', 'name_prefix', 'first_name', 'last_name', 'email', 'avatar', 'company', 'designation', 'background_info', 'phone_number', 'website', 'skype', 'address', 'city', 'zip_code', 'state', 'country')


class CircleForm(forms.ModelForm):

    class Meta:

        model = Circle
        fields = ('status', 'name', 'description')


class EventForm(forms.ModelForm):

    class Meta:

        model = Event
        fields = ('visibility', 'title', 'description', 'date', 'time', 'duration')
        widgets = {
            'date' : DateInput(),
            'time' : TimeInput(),
        }



class MessageForm(forms.ModelForm):

    class Meta:

        model = Message
        fields = ('subject', 'body')
        




class ItemForm(forms.ModelForm):

    class Meta:

        model = Item
        fields = '__all__'
        widgets = {
            'issue_date' : DateInput(),
        }



class TaxForm(forms.ModelForm):

    class Meta:

        model = Tax
        fields = '__all__'
        
        
        
class DiscountForm(forms.ModelForm):

    class Meta:

        model = Discount
        fields = '__all__'
        
        
        
class InvoiceSettingForm(forms.ModelForm):

    class Meta:

        model = InvoiceSetting
        fields = '__all__'
        
        

class EstimateSettingForm(forms.ModelForm):

    class Meta:

        model = EstimateSetting
        fields = '__all__'      




class EstimateUpdateForm(forms.ModelForm):

    class Meta:

        model = Estimate
        fields = ('client', 'status', 'due_date', 'title', 'internal_notes', 'terms_and_conditions', 'payment_description') 
        widgets = {
            'due_date' : DateInput(),
        }



class InvoiceUpdateForm(forms.ModelForm):

    class Meta:

        model = Invoice
        fields = ('client', 'status', 'due_date', 'title', 'internal_notes', 'terms_and_conditions', 'payment_description') 
        widgets = {
            'due_date' : DateInput(),
        }



class TemplateForm(forms.ModelForm):
    
    class Meta:

        model = Template
        fields = "__all__"





class DocumentForm(forms.ModelForm):
    
    class Meta:

        model = Document
        fields = ('title', 'document_for', 'invoice', 'estimate', 'body')
        
        
        