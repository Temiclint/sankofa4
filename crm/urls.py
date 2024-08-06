from django.urls import path
from .views import *


urlpatterns = [
    path('', login, name='login'),
    path('logout', logout, name='logout'),
    
    
    path('dashboard', dashboard, name='dashboard'),
    path('dashbaord/contacts', dashboardContacts, name='dashboard-contacts'),
    path('dashbaord/invoices', dashboardInvoices, name='dashboard-invoices'),
    path('dashbaord/quotes', dashboardQuotes, name='dashboard-quotes'),
    path('dashbaord/statistics', dashboardStatistics, name='dashboard-statistics'),
    path('dashbaord/monthlysale', dashboardMonthlySale, name='dashboard-monthlysale'),
    
    
    path('profile', profile, name='profile'),
    
    
    path('staff', users, name='staff-users'),
    path('staff/add', addUser, name='add-staff-user'),
    path('staff/update/<int:id>', updateUser, name='update-staff-user'),
    path('staff/delete/<int:id>', deleteUser, name='delete-staff-user'),
    
    
    path('roles', roles, name='roles'),
    path('role/add', addRole, name='add-role'),
    path('role/update/<int:id>', updateRole, name='update-role'),
    path('role/delete/<int:id>', deleteRole, name='delete-role'),
    
    
    path('category/company', companyCategories, name='company-categories'),
    path('category/company/update/<int:pk>', updateCompanyCategory, name='update-company-category'),
    path('category/company/delete/<int:pk>', deleteCompanyCategory, name='delete-company-category'),
    
    
    path('category/event', eventCategories, name='event-categories'),
    path('category/event/update/<int:pk>', updateEventCategory, name='update-event-category'),
    path('category/event/delete/<int:pk>', deleteEventCategory, name='delete-event-category'),
    
    
    path('companies', companies, name='companies'),
    path('company/add', addCompany, name='add-company'),
    path('company/update/<int:pk>', updateCompany, name='update-company'),
    path('company/delete/<int:pk>', deleteCompany, name='delete-company'),
    
    
    path('contacts', contacts, name='contacts'),
    path('contact/add', addContact, name='add-contact'),
    path('contact/update/<int:pk>', updateContact, name='update-contact'),
    path('contact/delete/<int:pk>', deleteContact, name='delete-contact'),
    
    
    path('circles', circles, name='circles'),
    path('circle/update/<int:pk>', updateCircle, name='update-circle'),
    path('circle/delete/<int:pk>', deleteCircle, name='delete-circle'),
    
    
    path('events', events, name='events'),
    path('event/add', addEvent, name='add-event'),
    path('event/update/<int:pk>', updateEvent, name='update-event'),
    path('event/delete/<int:pk>', deleteEvent, name='delete-event'),
    
    
    path('inbox' , inbox, name='inbox'),
    path('messages/view' , viewMessageAjax, name='view-message'),
    path('messages/sent' , messagesSent, name='sent-messages'),
    path('messages/signatures' , messagesSignature, name='signature-messages'),
    path('messages/trash' , messagesTrash, name='trash-messages'),
    path('message/send' , sendMessage, name='send-message'),
    path('message/delete/<int:pk>' , deleteMessage, name='delete-message'),
    
    
    path('items', items, name='items'),
    path('item/add', addItem, name='add-item'),
    path('item/update/<int:pk>', updateItem, name='update-item'),
    path('item/delete/<int:pk>', deleteItem, name='delete-item'),
    
    
    path('taxes', taxes, name='taxes'),
    path('tax/add', addTax, name='add-tax'),
    path('tax/update/<int:pk>', updateTax, name='update-tax'),
    path('tax/delete/<int:pk>', deleteTax, name='delete-tax'),
    
    
    path('discounts', discounts, name='discounts'),
    path('discount/add', addDiscount, name='add-discount'),
    path('discount/update/<int:pk>', updateDiscount, name='update-discount'),
    path('discount/delete/<int:pk>', deleteDiscount, name='delete-discount'),
    
    
    path('invoice-settings', invoiceSetting, name='invoice-setting'),
    
    path('invoices', invoices, name='invoices'),
    path('invoice/add', addInvoice, name='add-invoice'),
    path('invoice/view/<str:inv_no>', viewInvoice, name='view-invoice'),
    path('invoice/delete/<int:id>', deleteInvoice, name='delete-invoice'),
    
    
    path('estimate-settings', estimateSetting, name='estimate-setting'),
    
    
    path('estimates', estimates, name='estimates'),
    path('estimate/add', addEstimate, name='add-estimate'),
    path('estimate/view/<str:est_no>', viewEstimate, name='view-estimate'),
    path('estimate/delete/<int:id>', deleteEstimate, name='delete-estimate'),
    
    
    path('templates', templates, name='templates'),
    path('template/add', addTemplate, name='add-template'),
    path('template/view/<int:pk>', viewTemplate, name='view-template'),
    path('template/update/<int:pk>', updateTemplate, name='update-template'),
    path('template/delete/<int:pk>', deleteTemplate, name='delete-template'),
    
    
    path('documents', documents, name='documents'),
    path('document/add', addDocument, name='add-document'),
    path('document/view/<int:pk>', viewDocument, name='view-document'),
    path('document/update/<int:pk>', updateDocument, name='update-document'),
    path('document/delete/<int:pk>', deleteDocument, name='delete-document'),
]
