from django.db import models
from django.contrib.auth.models import User
from ckeditor.fields import RichTextField
from django.contrib.auth.models import User

# Create your models here..
class Profile(models.Model):
    TYPE_CHOICES = (
        (1, 'Admin'),
        (2, 'User'),
    )
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    image = models.ImageField(upload_to='users')

    class Meta:
        verbose_name = 'Profile'
        verbose_name_plural = 'Profiles'

    def __str__(self):
        return self.user.first_name + ' ' + self.user.last_name




class CompanyCategory(models.Model):
    STATUS_CHOICES = (
        (1, 'Active'),
        (2, 'Inactive'),
    )
    status = models.IntegerField(choices=STATUS_CHOICES)
    name = models.CharField(max_length=200)

    class Meta:

        verbose_name = 'Company Category'
        verbose_name_plural = 'Company Categories'

    def __str__(self):
        return self.name
    
    
class EventCategory(models.Model):
    STATUS_CHOICES = (
        (1, 'Active'),
        (2, 'Inactive'),
    )
    status = models.IntegerField(choices=STATUS_CHOICES)
    name = models.CharField(max_length=200)

    class Meta:

        verbose_name = 'Event Category'
        verbose_name_plural = 'Event Categories'

    def __str__(self):
        return self.name



class Company(models.Model):
    name = models.CharField(max_length=100)
    logo = models.ImageField(upload_to="company/logo", null=True, blank=True)
    category = models.ForeignKey(CompanyCategory, on_delete=models.CASCADE)
    background_info = models.TextField()
    phone_number = models.CharField(max_length=100)
    website = models.URLField(null=True, blank=True)
    skype = models.CharField(max_length=100, null=True, blank=True)
    address = models.CharField(max_length=500)
    city = models.CharField(max_length=50)
    zip_code = models.IntegerField()
    state = models.CharField(max_length=100)
    country = models.CharField(max_length=100)
    
    class Meta:

        verbose_name = 'Company'
        verbose_name_plural = 'Companies'

    def __str__(self):
        return self.name


class Contact(models.Model):
    ROLE_CHOICES = (
        (1, 'Lead'),
        (2, 'Prospect'),
        (3, 'Client'),
    )
    NAME_PREFIX_CHOICES = (
        ('Mr.', 'Mr.'),
        ('Ms.', 'Ms.'),
        ('Mrs.', 'Mrs.'),
        ('Miss.', 'Miss.'),
        ('Mx.', 'Mx'),
        ('Dr.', 'Dr.'),
    )
    
    role = models.IntegerField(choices=ROLE_CHOICES)
    name_prefix = models.CharField(max_length=5, choices=NAME_PREFIX_CHOICES)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField()
    avatar = models.ImageField(upload_to="contacts", null=True, blank=True)
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    designation = models.CharField(max_length=200)
    background_info = models.TextField()
    phone_number = models.CharField(max_length=100)
    website = models.URLField(null=True, blank=True)
    skype = models.CharField(max_length=100, null=True, blank=True)
    address = models.CharField(max_length=500)
    city = models.CharField(max_length=50)
    zip_code = models.IntegerField()
    state = models.CharField(max_length=100)
    country = models.CharField(max_length=100)
    

    class Meta:

        verbose_name = 'Contact'
        verbose_name_plural = 'Contacts'

    def __str__(self):
        return self.first_name + ' ' + self.last_name



class Circle(models.Model):
    STATUS_CHOICES = (
        (1, 'Active'),
        (2, 'Inactive'),
    )
    status = models.IntegerField(choices=STATUS_CHOICES)
    name = models.CharField(max_length=100)
    description = models.TextField()
    color = models.CharField(max_length=100)
    

    class Meta:

        verbose_name = 'Circle'
        verbose_name_plural = 'Circles'

    def __str__(self):
        return self.name


class CircleClient(models.Model):
    circle = models.ForeignKey(Circle, on_delete=models.CASCADE, related_name='circle_contact')
    client = models.ForeignKey(Contact, on_delete=models.CASCADE)

    class Meta:

        verbose_name = 'Circle Client'
        verbose_name_plural = 'Circle Clients'

    def __str__(self):
        return self.circle.name + ' (' + self.client.first_name + ' ' + self.client.last_name + ")"
    
    

class Event(models.Model):
    VISIBILITY_CHOICES = (
        (1, 'Public'),
        (2, 'Private'),
    )
    DURATION_CHOICES = (
        ('15 minutes', '15 minutes'),
        ('30 minutes', '30 minutes'),
        ('45 minutes', '45 minutes'),
        ('1 hour', '1 hour'),
        ('1 hour 15 minutes', '1 hour 15 minutes'),
        ('1 hour 30 minutes', '1 hour 30 minutes'),
        ('1 hour 45 minutes', '1 hour 45 minutes'),
        ('2 hour', '2 hour'),
        ('2 hours 15 minutes', '2 hours 15 minutes'),
        ('2 hours 30 minutes', '2 hours 30 minutes'),
        ('2 hours 45 minutes', '2 hours 45 minutes'),
        ('3 hour', '3 hour'),
        ('3 hours 15 minutes', '3 hours 15 minutes'),
        ('3 hours 30 minutes', '3 hours 30 minutes'),
        ('3 hours 45 minutes', '3 hours 45 minutes'),
        ('4 hour', '4 hour'),
        ('4 hours 15 minutes', '4 hours 15 minutes'),
        ('4 hours 30 minutes', '4 hours 30 minutes'),
        ('4 hours 45 minutes', '4 hours 45 minutes'),
        ('5 hour', '5 hour'),
        ('5 hours 15 minutes', '5 hours 15 minutes'),
        ('5 hours 30 minutes', '5 hours 30 minutes'),
        ('5 hours 45 minutes', '5 hours 45 minutes'),
        ('6 hour', '6 hour'),
        ('6 hours 15 minutes', '6 hours 15 minutes'),
        ('6 hours 30 minutes', '6 hours 30 minutes'),
        ('6 hours 45 minutes', '6 hours 45 minutes'),
        ('7 hour', '7 hour'),
        ('7 hours 15 minutes', '7 hours 15 minutes'),
        ('7 hours 30 minutes', '7 hours 30 minutes'),
        ('7 hours 45 minutes', '7 hours 45 minutes'),
        ('8 hour', '8 hour'),
        ('8 hours 15 minutes', '8 hours 15 minutes'),
        ('8 hours 30 minutes', '8 hours 30 minutes'),
        ('8 hours 45 minutes', '8 hours 45 minutes'),
        ('9 hour', '9 hour'),
        ('9 hours 15 minutes', '9 hours 15 minutes'),
        ('9 hours 30 minutes', '9 hours 30 minutes'),
        ('9 hours 45 minutes', '9 hours 45 minutes'),
        ('10 hour', '10 hour'),
        ('10 hours 15 minutes', '10 hours 15 minutes'),
        ('10 hours 30 minutes', '10 hours 30 minutes'),
        ('10 hours 45 minutes', '10 hours 45 minutes'),
        ('11 hour', '11 hour'),
        ('11 hours 15 minutes', '11 hours 15 minutes'),
        ('11 hours 30 minutes', '11 hours 30 minutes'),
        ('11 hours 45 minutes', '11 hours 45 minutes'),
        ('12 hour', '12 hour'),
    )
    
    visibility = models.IntegerField(choices=VISIBILITY_CHOICES)
    title = models.CharField(max_length=100)
    date = models.DateField()
    time = models.TimeField()
    duration = models.CharField(max_length=100, choices=DURATION_CHOICES)
    description = models.TextField()
    
    class Meta:

        verbose_name = 'Event'
        verbose_name_plural = 'Events'

    def __str__(self):
        return self.title



class Message(models.Model):
    is_read = models.BooleanField(default=False)
    is_deleted = models.BooleanField(default=False)
    subject = models.CharField(max_length=500)
    body =  RichTextField()
    created = models.DateTimeField(auto_now_add=True)
    sender = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
    
        verbose_name = 'Message'
        verbose_name_plural = 'Messages'

    def __str__(self):
        return self.subject
    
    
class MessageReciever(models.Model):
    message = models.ForeignKey(Message, on_delete=models.CASCADE, related_name="recievers")
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:

        verbose_name = 'Message Reciever'
        verbose_name_plural = 'Message Recievers'

    def __str__(self):
        return self.message.subject


class MessageAttachment(models.Model):
    message = models.ForeignKey(Message, on_delete=models.CASCADE, related_name="attachments")
    file = models.FileField(upload_to='attachments/', null=True, blank=True)

    class Meta:

        verbose_name = 'Message Attachment'
        verbose_name_plural = 'Message Attachments'

    def __str__(self):
        return self.message.subject







class Item(models.Model):
    STATUS_CHOICES = (
        (1, 'Active'),
        (2, 'Inactive'),
    )
    status = models.IntegerField(choices=STATUS_CHOICES, default=1)
    name = models.CharField(max_length=200)
    developer = models.CharField(max_length=100)
    country = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    issue_date = models.DateField()
    verify_institute = models.CharField(max_length=100)
    link_to_verification_certificate = models.URLField()
    description = models.TextField(null=True, blank=True)
    amount = models.DecimalField(max_digits=20, decimal_places=2)

    class Meta:

        verbose_name = 'Item'
        verbose_name_plural = 'Items'

    def __str__(self):
        return self.name
    
    
    
class Tax(models.Model):
    STATUS_CHOICES = (
        (1, 'Active'),
        (2, 'Inactive'),
    )
    
    status = models.IntegerField(choices=STATUS_CHOICES, default=1)
    name = models.CharField(max_length=200)
    description = models.TextField(null=True, blank=True)
    percentage = models.IntegerField()

    class Meta:

        verbose_name = 'Tax'
        verbose_name_plural = 'Taxes'

    def __str__(self):
        return self.name
    
    
    
class Discount(models.Model):
    STATUS_CHOICES = (
        (1, 'Active'),
        (2, 'Inactive'),
    )
    RATE_TYPE_CHOICES = (
        (1, 'Percentage %'),
        (2, 'Amount #'),
    )
    
    status = models.IntegerField(choices=STATUS_CHOICES, default=1)
    name = models.CharField(max_length=200)
    description = models.TextField(null=True, blank=True)
    percentage = models.IntegerField()

    class Meta:

        verbose_name = 'Discount'
        verbose_name_plural = 'Discounts'

    def __str__(self):
        return self.name
    
    

class InvoiceSetting(models.Model):
    title = models.CharField(max_length=200)
    phone_number = models.CharField(max_length=50)
    email = models.EmailField()
    invoice_prefix = models.CharField(max_length=5)
    terms_and_conditions = models.TextField(blank=True, null=True)
    payment_description = models.TextField(blank=True, null=True)
    address = models.CharField(max_length=300)
    city = models.CharField(max_length=50)
    state = models.CharField(max_length=50)
    zip_code = models.CharField(max_length=50)
    country = models.CharField(max_length=50)
    logo = models.ImageField(upload_to='Invoice_Logos/')
    

    class Meta:

        verbose_name = 'Invoice Setting'
        verbose_name_plural = 'Invoice Settings'

    def __str__(self):
        return self.title
    
    


class Invoice(models.Model):
    STATUS_CHOICES = (
        (1, 'Pending'),
        (2, 'Paid'),
    )
    
    status = models.IntegerField(choices=STATUS_CHOICES, default=1)
    client = models.ForeignKey(Contact, on_delete=models.CASCADE, related_name='related_invoices')
    title = models.CharField(max_length=200)
    invoice_number = models.CharField(max_length=1000)
    date_added = models.DateTimeField(auto_now_add=True)
    due_date = models.DateTimeField()
    internal_notes = models.TextField(blank=True, null=True)
    terms_and_conditions = models.TextField(blank=True, null=True)
    payment_description = models.TextField(blank=True, null=True)
    sub_total = models.DecimalField(max_digits=999, decimal_places=2, null=True, blank=True)
    taxes_total = models.DecimalField(max_digits=999, decimal_places=2, null=True, blank=True)
    discounts_total = models.DecimalField(max_digits=999, decimal_places=2, null=True, blank=True)
    grand_total = models.DecimalField(max_digits=999, decimal_places=2, null=True, blank=True)

    class Meta:

        verbose_name = 'Invoice'
        verbose_name_plural = 'Invoices'

    def __str__(self):
        return str(self.invoice_number)
    
    
    
    
class InvoiceItem(models.Model):
    invoice = models.ForeignKey(Invoice, on_delete=models.CASCADE, related_name='items')
    item = models.ForeignKey(Item, on_delete=models.CASCADE)

    class Meta:

        verbose_name = 'Invoice Item'
        verbose_name_plural = 'Invoice Items'

    def __str__(self):
        return self.item.name + ' (' + self.invoice.invoice_number + ')'
    
    

class InvoiceTax(models.Model):
    invoice = models.ForeignKey(Invoice, on_delete=models.CASCADE, related_name='taxes')
    tax = models.ForeignKey(Tax, on_delete=models.CASCADE)

    class Meta:

        verbose_name = 'Invoice Tax'
        verbose_name_plural = 'Invoice Taxes'

    def __str__(self):
        return self.tax.name + ' (' + self.invoice.invoice_number + ')'



class InvoiceDiscount(models.Model):
    invoice = models.ForeignKey(Invoice, on_delete=models.CASCADE, related_name='discounts')
    discount = models.ForeignKey(Discount, on_delete=models.CASCADE)

    class Meta:

        verbose_name = 'Invoice Discount'
        verbose_name_plural = 'Invoice Discounts'

    def __str__(self):
        return self.discount.name + ' (' + self.invoice.invoice_number + ')'


class InvoiceFile(models.Model):
    invoice = models.ForeignKey(Invoice, on_delete=models.CASCADE, related_name='files')
    file = models.FileField(upload_to='invoice_files')

    class Meta:

        verbose_name = 'Invoice File'
        verbose_name_plural = 'Invoice Files'

    def __str__(self):
        return self.invoice.invoice_number 
    
    
    
    
    
    
class EstimateSetting(models.Model):
    title = models.CharField(max_length=200)
    phone_number = models.CharField(max_length=50)
    email = models.EmailField()
    estimate_prefix = models.CharField(max_length=5)
    terms_and_conditions = models.TextField(blank=True, null=True)
    payment_description = models.TextField(blank=True, null=True)
    address = models.CharField(max_length=300)
    city = models.CharField(max_length=50)
    state = models.CharField(max_length=50)
    zip_code = models.CharField(max_length=50)
    country = models.CharField(max_length=50)
    logo = models.ImageField(upload_to='Invoice_Logos/')
    

    class Meta:

        verbose_name = 'Estimate Setting'
        verbose_name_plural = 'Estimate Settings'

    def __str__(self):
        return self.title
    
    


class Estimate(models.Model):
    STATUS_CHOICES = (
        (1, 'Open'),
        (2, 'Accepted'),
        (3, 'Rejected'),
    )
    
    status = models.IntegerField(choices=STATUS_CHOICES, default=1)
    client = models.ForeignKey(Contact, on_delete=models.CASCADE, related_name='related_estimates')
    title = models.CharField(max_length=200)
    estimate_number = models.CharField(max_length=1000)
    date_added = models.DateTimeField(auto_now_add=True)
    due_date = models.DateTimeField()
    internal_notes = models.TextField(blank=True, null=True)
    terms_and_conditions = models.TextField(blank=True, null=True)
    payment_description = models.TextField(blank=True, null=True)
    sub_total = models.DecimalField(max_digits=999, decimal_places=2, null=True, blank=True)
    taxes_total = models.DecimalField(max_digits=999, decimal_places=2, null=True, blank=True)
    discounts_total = models.DecimalField(max_digits=999, decimal_places=2, null=True, blank=True)
    grand_total = models.DecimalField(max_digits=999, decimal_places=2, null=True, blank=True)

    class Meta:

        verbose_name = 'Estimate'
        verbose_name_plural = 'Estimates'

    def __str__(self):
        return str(self.estimate_number)
    
    
class EstimateItem(models.Model):
    estimate = models.ForeignKey(Estimate, on_delete=models.CASCADE, related_name='estimate_items')
    item = models.ForeignKey(Item, on_delete=models.CASCADE)

    class Meta:

        verbose_name = 'Estimate Item'
        verbose_name_plural = 'Estimate Items'

    def __str__(self):
        return self.item.name + ' (' + self.estimate.estimate_number + ')'
    
    

class EstimateTax(models.Model):
    estimate = models.ForeignKey(Estimate, on_delete=models.CASCADE, related_name='estimate_taxes')
    tax = models.ForeignKey(Tax, on_delete=models.CASCADE)

    class Meta:

        verbose_name = 'Estimate Tax'
        verbose_name_plural = 'Estimate Taxes'

    def __str__(self):
        return self.tax.name + ' (' + self.estimate.estimate_number + ')'



class EstimateDiscount(models.Model):
    estimate = models.ForeignKey(Estimate, on_delete=models.CASCADE, related_name='estimate_discounts')
    discount = models.ForeignKey(Discount, on_delete=models.CASCADE)

    class Meta:

        verbose_name = 'Estimate Discount'
        verbose_name_plural = 'Estimate Discounts'

    def __str__(self):
        return self.discount.name + ' (' + self.estimate.estimate_number + ')'


class EstimateFile(models.Model):
    estimate = models.ForeignKey(Estimate, on_delete=models.CASCADE, related_name='estimate_files')
    file = models.FileField(upload_to='estimate_files')

    class Meta:

        verbose_name = 'Estimate File'
        verbose_name_plural = 'Estimate Files'

    def __str__(self):
        return self.estimate.estimate_number 
    
    
    
    
class Template(models.Model):
    title = models.CharField(max_length=200)
    body = RichTextField()
    
    class Meta:

        verbose_name = 'Template'
        verbose_name_plural = 'Templates'

    def __str__(self):
        return self.title
    
    
    



class Document(models.Model):
    FOR_CHOICES = (
        (1, 'Invoice'),
        (2, 'Estimate'),
    )
    document_for = models.IntegerField(choices=FOR_CHOICES)
    invoice = models.ForeignKey(Invoice, on_delete=models.SET_NULL, null=True, blank=True)
    estimate = models.ForeignKey(Estimate, on_delete=models.SET_NULL, null=True, blank=True)
    title = models.CharField(max_length=150)
    body = RichTextField()

    class Meta:

        verbose_name = 'Document'
        verbose_name_plural = 'Documents'

    def __str__(self):
        return self.title
