from django.contrib import admin
from .models import *
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User
from django.contrib.auth.models import Permission

# Register your models here.

@admin.register(Permission)
class PermissionAdmin(admin.ModelAdmin):
    list_display = ('name', 'codename', 'content_type')

class ProfileInline(admin.StackedInline):
    model = Profile
class UserAdmin(BaseUserAdmin):
    inlines = (ProfileInline, )
    
admin.site.unregister(User)
admin.site.register(User, UserAdmin)


@admin.register(CompanyCategory)
class CompanyCategoryAdmin(admin.ModelAdmin):

    list_display = ('name', 'status')
    list_filter = ('status',)
    search_fields = ('name',)


@admin.register(EventCategory)
class EventCategoryAdmin(admin.ModelAdmin):

    list_display = ('name', 'status')
    list_filter = ('status',)
    search_fields = ('name',)
    
@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    list_display = ('name',)
    
    
@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name')
    
class CircleClientInline(admin.TabularInline):
    model = CircleClient
@admin.register(Circle)
class CircleAdmin(admin.ModelAdmin):
    list_display = ('name',)
    inlines = [
        CircleClientInline,
    ]
    

@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ('title',)
    
    

class MessageRecieverInline(admin.TabularInline):
    model = MessageReciever
class MessageAttachmentInline(admin.TabularInline):
    model = MessageAttachment
@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):

    list_display = ('subject', 'sender', 'created', 'is_read', 'is_deleted')
    list_filter = ( 'is_read', 'is_deleted')
    inlines = [
        MessageRecieverInline,
        MessageAttachmentInline,
    ]
    search_fields = ('subject',)
    
    
    
    
    
    
    
@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    list_display = ('name',)
    
    
@admin.register(Tax)
class TaxAdmin(admin.ModelAdmin):
    list_display = ('name',)
    
    
@admin.register(Discount)
class DiscountAdmin(admin.ModelAdmin):
    list_display = ('name',)
    
    
    
@admin.register(InvoiceSetting)
class InvoiceSettingAdmin(admin.ModelAdmin):
    list_display = ('title',)
    
    def has_add_permission(self, request, obj=None):
        return False
    def has_delete_permission(self, request, obj=None):
        return False
    
    

class InvoiceItemInline(admin.TabularInline):
    model = InvoiceItem
class InvoiceTaxInline(admin.TabularInline):
    model = InvoiceTax
class InvoiceDiscountInline(admin.TabularInline):
    model = InvoiceDiscount
class InvoiceFileInline(admin.TabularInline):
    model = InvoiceFile
@admin.register(Invoice)
class InvoiceAdmin(admin.ModelAdmin):
    list_display = ('invoice_number',)
    inlines = [
        InvoiceItemInline,
        InvoiceTaxInline,
        InvoiceDiscountInline,
        InvoiceFileInline,
    ]
    
    
    
    
@admin.register(EstimateSetting)
class EstimateSettingAdmin(admin.ModelAdmin):
    list_display = ('title',)
    
    def has_add_permission(self, request, obj=None):
        return False
    def has_delete_permission(self, request, obj=None):
        return False
    
    

class EstimateItemInline(admin.TabularInline):
    model = EstimateItem
class EstimateTaxInline(admin.TabularInline):
    model = EstimateTax
class EstimateDiscountInline(admin.TabularInline):
    model = EstimateDiscount
class EstimateFileInline(admin.TabularInline):
    model = EstimateFile
@admin.register(Estimate)
class EstimateAdmin(admin.ModelAdmin):
    list_display = ('estimate_number',)
    inlines = [
        EstimateItemInline,
        EstimateTaxInline,
        EstimateDiscountInline,
        EstimateFileInline,
    ]