
from .forms import *
from .models import *
from .decorators import *
from datetime import datetime
from multiprocessing import context
from django.db.models import Sum, Avg
from django.contrib.auth.hashers import make_password
from django.contrib import messages
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.models import User, Group, Permission
from django.shortcuts import render, redirect, get_object_or_404  
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib.auth.decorators import login_required, permission_required


# Create your views here.

@unauthenticated_user
def login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user is not None:
            auth_login(request, user)
            
            messages.success(request, 'Welcome on the board..!!!') 
            if 'next' in request.POST:
                return redirect(request.POST['next'])
            else:
                return redirect('crm:dashboard')
        else:
            messages.warning(request, 'Invalid credentials')
            
    return render(request, 'login.html')


def logout(request):
    auth_logout(request)
    messages.success(request, 'Logged out successfully')
    return redirect('crm:login')


@login_required(login_url='crm:login')
def dashboard(request):
    
    context = {}
    return render(request, 'dashboard.html')


# DASHBOARD ROUTES
@login_required(login_url='crm:login')
def dashboardContacts(request):
    contacts = Contact.objects.all().order_by('-id')[:10]
    context = {
        'contacts' : contacts
    }
    return render(request, 'snippets/contacts.html', context)


@login_required(login_url='crm:login')
def dashboardInvoices(request):
    invoices = Invoice.objects.all().order_by('-id')[:10]
    context = {
        'invoices' : invoices
    }
    return render(request, 'snippets/invoices.html', context)


@login_required(login_url='crm:login')
def dashboardQuotes(request):
    quotes = Estimate.objects.all().order_by('-id')[:10]
    context = {
        'quotes' : quotes
    }
    return render(request, 'snippets/quotes.html', context)


@login_required(login_url='crm:login')
def dashboardStatistics(request):
    current_year = datetime.now().year
    years = [current_year - i for i in range(5)]
    totals = []
    for i in years:
        total = Invoice.objects.filter(due_date__year=i, status=2).aggregate(Sum('grand_total'))['grand_total__sum']
        if total:
            totals.append(total)
        else:
            totals.append(0)
        
    data = {
        'years' : years,
        'totals' : totals
    }
    return JsonResponse(data)


@login_required(login_url='crm:login')
def dashboardMonthlySale(request):
    current_year = datetime.now().year
    totals = []
    for i in range(1, 13):
        total = Invoice.objects.filter(due_date__year=current_year, due_date__month=i, status=2).aggregate(Sum('grand_total'))['grand_total__sum']
        if total:
            totals.append(total)
        else:
            totals.append(0)
    
    data = {
        'totals' : totals
    }
    return JsonResponse(data)



#PROFILE VIEW
@login_required
def profile(request):
    password_form = PasswordChangeForm(request.user)
    user_form = UserUpdateForm(instance=request.user)
    profile_form = ProfileForm(instance=request.user.profile)

    if request.method == "POST":
        if "updateProfile" in request.POST:
            user_form = UserUpdateForm(request.POST, instance=request.user)
            profile_form = ProfileForm(request.POST, request.FILES, instance=request.user.profile)

            if user_form.is_valid():
                user = user_form.save(commit=False)
                user.save()

            if profile_form.is_valid():
                profile_form.save()
                user.save()

            messages.success(request,"Profile successfully updated")
            return redirect("crm:profile")

        if "updatePassword" in request.POST:
            password_form = PasswordChangeForm(request.user, request.POST)
            if password_form.is_valid():
                user = password_form.save()
                update_session_auth_hash(request, user)
                messages.success(request, "Password updated successfully")
                return redirect("main:profile")

    context = {
        "user_form": user_form,
        "password_form": password_form,
        "profile_form": profile_form,
    }
    return render(request, "profile.html", context)



# USERS AND PERMISSIONS VIEWS
@login_required
@permission_required("auth.view_user", raise_exception=True)
def users(request):
    users = User.objects.all()
    
    context = {
        'users' : users,
    }
    return render(request, 'users/users.html', context)

@login_required
@permission_required('auth.add_user', raise_exception=True)
def addUser(request):
    groups = Group.objects.all()
    user_form = UserCreationForm()
    
    if request.method == 'POST':
        user_form = UserCreationForm(request.POST)
        
        if User.objects.filter(username = request.POST.get('email')).exists():
            messages.warning(request, 'This email is already registered with the system. Please select some other email')
        else:
            if user_form.is_valid:
                user = user_form.save(commit=False)
                user.username = user_form.cleaned_data['email']
                user.password = make_password(request.POST.get('password'))
                user.is_staff = True
                user.save()
                
                groups = request.POST.getlist('group')
                
                if groups:
                    for i in groups:
                        group = get_object_or_404(Group, id=i)
                        group.user_set.add(user)
                
                messages.success(request, 'Staff user added successfully')
                return redirect('crm:staff-users')
    
    context = {
        'user_form' : user_form,
        'roles' : groups,
    }
    return render(request, 'users/add-user.html', context)


@login_required
@permission_required('auth.change_user', raise_exception=True)
def updateUser(request, id):
    instance = User.objects.get(id=id)
    user_form = UserUpdateForm(instance=instance)
    groups = Group.objects.all()
    
    if request.method == 'POST':
        user_form = UserUpdateForm(request.POST, instance=instance)

        if user_form.is_valid:
            user = user_form.save()
            instance.groups.clear()
            groups = request.POST.getlist('group')
                
            if groups:
                for i in groups:
                    group = get_object_or_404(Group, id=i)
                    group.user_set.add(instance)
                    
        if request.POST.get('password'):
            user.password = make_password(request.POST.get('password'))
            user.save()
            
        messages.success(request, 'Staff user updated successfully')
        return redirect('crm:staff-users')
    
    context = {
        'roles' : groups,
        'instance' : instance,
        'user_form' : user_form,
    }
    return render(request, 'users/update-user.html', context)

@login_required
@permission_required('auth.delete_user', raise_exception=True)
def deleteUser(request, id):
    instance = get_object_or_404(User, id=id)
    instance.delete()
    messages.info(request, 'User deleted successfully.')
    return redirect('crm:staff-users')



# ROLES VIEWS
@login_required
@permission_required('auth.view_group', raise_exception=True)
def roles(request):
    roles = Group.objects.all().order_by('name')
    
    context = {
        'roles' : roles,
    }
    return render(request, 'roles/roles.html', context)


@login_required
@permission_required('auth.add_group', raise_exception=True)
def addRole(request):
    form = RoleForm()
    permissions = Permission.objects.all()
    
    if request.method == 'POST':
        access = request.POST.getlist('permissions')
        form = RoleForm(request.POST)
        if form.is_valid():
            role = form.save()
            
            for i in access:
                role.permissions.add(get_object_or_404(Permission, id=i))
                
            messages.success(request, 'Role added successfully')
            return redirect('crm:roles')
    
    context = {
        'form' : form,
        'permissions' : permissions,
    }
    return render(request, 'roles/add-role.html', context)


@login_required
@permission_required('auth.change_group', raise_exception=True)
def updateRole(request, id):
    instance = get_object_or_404(Group, id=id)
    form = RoleForm(instance=instance)
    permissions = Permission.objects.all()
    
    if request.method == "POST":
        access = request.POST.getlist('permissions')
        form = RoleForm(request.POST, instance=instance)
        if form.is_valid():
            form.save()
            instance.permissions.clear()
            for i in access:
                instance.permissions.add(get_object_or_404(Permission, id=i))
                
            messages.success(request, 'Role updated successfully')
            return redirect('crm:roles')
    
    context = {
        'instance' : instance,
        'form' : form,
        'permissions' : permissions,
    }
    return render(request, 'roles/update-role.html', context)


@login_required
@permission_required('auth.delete_group', raise_exception=True)
def deleteRole(request, id):
    instance = get_object_or_404(Group, id=id)
    instance.delete()
    messages.info(request, 'Role deleted successfully')
    return redirect('crm:roles')







# Settings Views 
@login_required(login_url='crm:login')
@permission_required("crm.view_companycategory", raise_exception=True)
def companyCategories(request):
    categories = CompanyCategory.objects.all().order_by('name')
    form = CompanyCategoryForm()
    
    if request.method == 'POST':
        form = CompanyCategoryForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Company category is added successfully')
            return redirect ('crm:company-categories')
    
    context = {
        'form' : form,
        'categories' : categories,
    }
    return render(request, 'settings/company-categories.html', context)


@login_required(login_url='crm:login')
@permission_required("crm.change_companycategory", raise_exception=True)
def updateCompanyCategory(request, pk):
    category = CompanyCategory.objects.get(id=pk)
    form = CompanyCategoryForm(instance=category)
    
    if request.method == 'POST':
        form = CompanyCategoryForm(request.POST, instance=category)
        if form.is_valid():
            form.save()
            messages.success(request, 'Company category is updated successfully')
            return redirect('crm:company-categories')
    
    context = {
        'category' : category,
        'form' : form,
    }
    return render(request, 'settings/update-company-category.html', context)


@login_required(login_url='crm:login')
@permission_required("crm.delete_companycategory", raise_exception=True)
def deleteCompanyCategory(request, pk):
    category = CompanyCategory.objects.get(id=pk)
    category.delete()
    messages.success(request, 'Company category deleted successfully')
    return redirect('crm:company-categories')


@login_required(login_url='crm:login')
@permission_required("crm.view_eventcategory", raise_exception=True)
def eventCategories(request):
    categories = EventCategory.objects.all().order_by('name')
    form = EventCategoryForm()
    
    if request.method == 'POST':
        form = EventCategoryForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Event category is added successfully')
            return redirect ('crm:event-categories')
    
    context = {
        'form' : form,
        'categories' : categories,
    }
    return render(request, 'settings/event-categories.html', context)


@login_required(login_url='crm:login')
@permission_required("crm.change_eventcategory", raise_exception=True)
def updateEventCategory(request, pk):
    category = EventCategory.objects.get(id=pk)
    form = EventCategoryForm(instance=category)
    
    if request.method == 'POST':
        form = EventCategoryForm(request.POST, instance=category)
        if form.is_valid():
            form.save()
            messages.success(request, 'Event category is updated successfully')
            return redirect('crm:event-categories')
    
    context = {
        'category' : category,
        'form' : form,
    }
    return render(request, 'settings/update-event-category.html', context)


@login_required(login_url='crm:login')
@permission_required("crm.delete_eventcategory", raise_exception=True)
def deleteEventCategory(request, pk):
    category = EventCategory.objects.get(id=pk)
    category.delete()
    messages.success(request, 'Event category deleted successfully')
    return redirect('crm:event-categories')






# Comapny views
@login_required(login_url='crm:login')
@permission_required("crm.view_company", raise_exception=True)
def companies(request):
    companies = Company.objects.all().order_by('-id')
    
    context = {
        'companies' : companies,
    }
    return render(request, 'company/companies.html', context)


@login_required(login_url='crm:login')
@permission_required("crm.add_company", raise_exception=True)
def addCompany(request):
    form = CompanyForm()
    
    if request.method == 'POST':
        form = CompanyForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Company added successfully')
            return redirect('crm:companies')
    
    context = {
        'form' : form,
    }
    return render(request, 'company/add-company.html', context)


@login_required(login_url='crm:login')
@permission_required("crm.change_company", raise_exception=True)
def updateCompany(request, pk):
    company = Company.objects.get(id=pk)
    form = CompanyForm(instance=company)
    
    if request.method == 'POST':
        form = CompanyForm(request.POST, request.FILES, instance=company)
        
        if form.is_valid():
            form.save()
            messages.success(request, 'Company updated successfully')
            return redirect('crm:companies')
    
    context = {
        'company' : company,
        'form' : form,
    }
    return render(request, 'company/update-company.html', context)


@login_required(login_url='crm:login')
@permission_required("crm.delete_company", raise_exception=True)
def deleteCompany(request, pk):
    company  = Company.objects.get(id=pk)
    company.delete()
    messages.success(request, 'Company deleted successfully')
    return redirect('crm:companies')



# Contact views
@login_required(login_url='crm:login')
@permission_required("crm.view_contact", raise_exception=True)
def contacts(request):
    contacts = Contact.objects.all().order_by('-id')
    
    context = {
        'contacts' : contacts,
    }
    return render(request, 'contacts/contacts.html', context)


@login_required(login_url='crm:login')
@permission_required("crm.add_contact", raise_exception=True)
def addContact(request):
    form = ContactForm()
    
    if request.method == 'POST':
        form = ContactForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Conatct added successfully')
            return redirect('crm:contacts')
    
    context = {
        'form' : form,
    }
    return render(request, 'contacts/add-contact.html', context)


@login_required(login_url='crm:login')
@permission_required("crm.change_contact", raise_exception=True)
def updateContact(request, pk):
    contact = Contact.objects.get(id=pk)
    form = ContactForm(instance=contact)
    
    if request.method == 'POST':
        form = ContactForm(request.POST, request.FILES, instance=contact)
        
        if form.is_valid():
            form.save()
            messages.success(request, 'Contact updated successfully')
            return redirect('crm:contacts')
    
    context = {
        'contact' : contact,
        'form' : form,
    }
    return render(request, 'contacts/update-contact.html', context)


@login_required(login_url='crm:login')
@permission_required("crm.delete_contact", raise_exception=True)
def deleteContact(request, pk):
    contact  = Contact.objects.get(id=pk)
    contact.delete()
    messages.success(request, 'Contact deleted successfully')
    return redirect('crm:contacts')



# Circle views
@login_required(login_url='crm:login')
@permission_required("crm.view_circle", raise_exception=True)
def circles(request):
    circles = Circle.objects.all().order_by('-id')
    contacts = Contact.objects.filter(role=3).order_by('first_name')
    form = CircleForm()
    
    if request.method == 'POST':
        form = CircleForm(request.POST)
        contact_list = request.POST.getlist('contact')
        
        if form.is_valid():
            circle = form.save(commit=False)
            circle.color = request.POST.get('color_code')
            circle.save()
            
            for i in contact_list:
                contact = Contact.objects.get(id=i)
                CircleClient.objects.create(circle=circle, client=contact)
            
            messages.success(request, 'Circle added successfully.')
            return redirect('crm:circles')
            
    
    context = {
        'circles' : circles,
        'contacts' : contacts,
        'form' : form,
    }
    return render(request, 'circles/circles.html', context)


@login_required(login_url='crm:login')
@permission_required("crm.change_circle", raise_exception=True)
def updateCircle(request, pk):
    circle = Circle.objects.get(id=pk)
    form = CircleForm(instance=circle)
    contacts = Contact.objects.filter(role=3).order_by('first_name')
    circle_contacts = circle.circle_contact.all()
    
    
    if request.method == 'POST':
        form = CircleForm(request.POST, instance=circle)
        contact_list = request.POST.getlist('contact')
        
        if form.is_valid():
            circle = form.save()
            circle.color = request.POST.get('color_code')
            circle.save()
            
            for i in circle_contacts:
                instance = CircleClient.objects.get(id=i.id)
                instance.delete()
            
            for j in contact_list:
                contact = Contact.objects.get(id=j)
                CircleClient.objects.create(circle=circle, client=contact)
                
            
            messages.success(request, 'Circle updated successfully')
            return redirect('crm:circles')
    
    context = {
        'circle' : circle,
        'form' : form,
        'contacts' : contacts,
        'circle_contacts' : circle_contacts,
    }
    return render(request, 'circles/update-circle.html', context)


@login_required(login_url='crm:login')
@permission_required("crm.delete_circle", raise_exception=True)
def deleteCircle(request, pk):
    circle  = Circle.objects.get(id=pk)
    circle.delete()
    messages.success(request, 'Circle deleted successfully')
    return redirect('crm:circles')




# Event views
@login_required(login_url='crm:login')
@permission_required("crm.view_event", raise_exception=True)
def events(request):
    events = Event.objects.all().order_by('-id')
    
    context = {
        'events' : events,
    }
    return render(request, 'events/events.html', context)


@login_required(login_url='crm:login')
@permission_required("crm.add_event", raise_exception=True)
def addEvent(request):
    form = EventForm()
    
    if request.method == 'POST':
        form = EventForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Event added successfully')
            return redirect('crm:events')
    
    context = {
        'form' : form,
    }
    return render(request, 'events/add-event.html', context)


@login_required(login_url='crm:login')
@permission_required("crm.change_event", raise_exception=True)
def updateEvent(request, pk):
    event = Event.objects.get(id=pk)
    form = EventForm(instance=event)
    
    if request.method == 'POST':
        form = EventForm(request.POST, instance=event)
        
        if form.is_valid():
            form.save()
            messages.success(request, 'Event updated successfully')
            return redirect('crm:events')
    
    context = {
        'event' : event,
        'form' : form,
    }
    return render(request, 'events/update-event.html', context)


@login_required(login_url='crm:login')
@permission_required("crm.delete_event", raise_exception=True)
def deleteEvent(request, pk):
    event  = Event.objects.get(id=pk)
    event.delete()
    messages.success(request, 'Event deleted successfully')
    return redirect('crm:events')




# Messages View
@login_required(login_url='crm:login')
def inbox(request):
    msgs = Message.objects.filter(recievers__user=request.user, is_deleted=False).order_by('-id')
    users = User.objects.all()
    form = MessageForm()
    
    context = {
        'users' : users,
        'form' : form,
        'msgs' : msgs,
    }
    return render(request, 'messaging/inbox.html', context)


@login_required(login_url='crm:login')
def messagesSent(request):
    msgs = Message.objects.filter(sender=request.user).order_by('-id')
    users = User.objects.all()
    form = MessageForm()
    
    context = {
        'msgs' : msgs,
        'users' : users,
        'form' : form,
    }
    return render(request, 'messaging/sent.html', context)


@login_required(login_url='crm:login')
def messagesTrash(request):
    msgs = Message.objects.filter(recievers__user=request.user, is_deleted=True).order_by('-id')
    users = User.objects.all()
    form = MessageForm()
    
    context = {
        'msgs' : msgs,
        'users' : users,
        'form' : form,
    }   
    return render(request, 'messaging/trash.html', context)


@login_required(login_url='crm:login')
def messagesSignature(request):
    users = User.objects.all()
    form = MessageForm()
    
    context = {
        'users' : users,
        'form' : form,
    }    
    return render(request, 'messaging/signature.html', context)


@login_required(login_url='crm:login')
def viewMessageAjax(request):
    msg = get_object_or_404(Message, id=request.GET.get('id'))
    recepients = msg.recievers.all()
    
    link = request.META.get('HTTP_REFERER')
    
    if 'inbox' in link:
        msg.is_read = True
        msg.save()
    
    context = {
        'link' : link,
        'msg' : msg,
        'recepients' : recepients,
    }
    return render(request, 'messaging/snippets/mail.html', context)



@login_required(login_url='crm:login')
def sendMessage(request):
    if request.method == 'POST':
        form = MessageForm(request.POST)
        recievers = request.POST.getlist('recievers')
        files = request.FILES.getlist('files')
        
        if form.is_valid():
            msg = form.save(commit=False)
            msg.sender = request.user
            msg.save()
        
        for i in recievers:
            MessageReciever.objects.create(message=msg, user=User.objects.get(id=i))
        
        for j in files:
            MessageAttachment.objects.create(message=msg, file=j)
    
    messages.success(request, 'Message sent successsfully')
    return redirect('crm:inbox')


@login_required(login_url='crm:login')
def deleteMessage(request, pk):
    msg = get_object_or_404(Message, id=pk)
    msg.is_deleted = True
    msg.save()
    messages.info(request, 'Message sent to trash')
    return redirect('crm:inbox')





# Items Views
@login_required(login_url='crm:login')
@permission_required("crm.view_item", raise_exception=True)
def items(request):
    items = Item.objects.all().order_by('-id')
    
    context = {
        'items' : items,
    }
    return render(request, 'items/items.html', context)

@login_required(login_url='crm:login')
@permission_required("crm.add_item", raise_exception=True)
def addItem(request):
    form = ItemForm()
    
    if request.method == 'POST':
        form = ItemForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Item added successfully')
            return redirect('crm:items')
    
    context = {
        'form' : form,
    }
    return render(request, 'items/add-item.html', context)

@login_required(login_url='crm:login')
@permission_required("crm.change_item", raise_exception=True)
def updateItem(request, pk):
    item = get_object_or_404(Item, id=pk)
    
    form = ItemForm(instance=item)
    
    if request.method == 'POST':
        form = ItemForm(request.POST, instance=item)
        if form.is_valid():
            form.save()
            messages.success(request, 'Item updated successfully')
            return redirect('crm:items')
    
    context = {
        'form' : form,
    }
    return render(request, 'items/update-item.html', context)

@login_required(login_url='crm:login')
@permission_required("crm.delete_item", raise_exception=True)
def deleteItem(request, pk):
    item = get_object_or_404(Item, id=pk)
    item.delete()
    messages.info(request, 'Item deleted successfully')
    return redirect('crm:items')



# Taxes views
@login_required(login_url='crm:login')
@permission_required("crm.view_tax", raise_exception=True)
def taxes(request):
    taxes = Tax.objects.all().order_by('-id')
    
    context = {
        'taxes' : taxes,
    }
    return render(request, 'taxes/taxes.html', context)

@login_required(login_url='crm:login')
@permission_required("crm.add_tax", raise_exception=True)
def addTax(request):
    form = TaxForm()
    
    if request.method == 'POST':
        form = TaxForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Tax added successfully')
            return redirect('crm:taxes')
    
    context = {
        'form' : form,
    }
    return render(request, 'taxes/add-tax.html', context)

@login_required(login_url='crm:login')
@permission_required("crm.change_tax", raise_exception=True)
def updateTax(request, pk):
    tax = get_object_or_404(Tax, id=pk)
    
    form = TaxForm(instance=tax)
    
    if request.method == 'POST':
        form = TaxForm(request.POST, instance=tax)
        if form.is_valid():
            form.save()
            messages.success(request, 'Tax updated successfully')
            return redirect('crm:taxes')
    
    context = {
        'form' : form,
    }
    return render(request, 'taxes/update-tax.html', context)

@login_required(login_url='crm:login')
@permission_required("crm.delete_tax", raise_exception=True)
def deleteTax(request, pk):
    tax = get_object_or_404(Tax, id=pk)
    tax.delete()
    messages.info(request, 'Tax deleted successfully')
    return redirect('crm:taxes')


# Discount Views
@login_required(login_url='crm:login')
@permission_required("crm.view_discount", raise_exception=True)
def discounts(request):
    discounts = Discount.objects.all().order_by('-id')
    
    context = {
        'discounts' : discounts,
    }
    return render(request, 'discounts/discounts.html', context)

@login_required(login_url='crm:login')
@permission_required("crm.add_discount", raise_exception=True)
def addDiscount(request):
    form = DiscountForm()
    
    if request.method == 'POST':
        form = DiscountForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Discount added successfully')
            return redirect('crm:discounts')
    
    context = {
        'form' : form,
    }
    return render(request, 'discounts/add-discount.html', context)

@login_required(login_url='crm:login')
@permission_required("crm.change_discount", raise_exception=True)
def updateDiscount(request, pk):
    discount = get_object_or_404(Discount, id=pk)
    
    form = DiscountForm(instance=discount)
    
    if request.method == 'POST':
        form = DiscountForm(request.POST, instance=discount)
        if form.is_valid():
            form.save()
            messages.success(request, 'Discount updated successfully')
            return redirect('crm:discounts')
    
    context = {
        'form' : form,
    }
    return render(request, 'discounts/update-discount.html', context)

@login_required(login_url='crm:login')
@permission_required("crm.delete_discount", raise_exception=True)
def deleteDiscount(request, pk):
    discount = get_object_or_404(Discount, id=pk)
    discount.delete()
    messages.info(request, 'Discount deleted successfully')
    return redirect('crm:discounts')




#Invoice views
@login_required(login_url='crm:login')
@permission_required("crm.view_invoicesetting", raise_exception=True)
def invoiceSetting(request):
    instance = InvoiceSetting.objects.first()
    
    form = InvoiceSettingForm(instance=instance)
    
    if request.method == 'POST':
        form = InvoiceSettingForm(request.POST, request.FILES, instance=instance)
        
        if form.is_valid():
            form.save()
            messages.success(request, 'Invoice settings updated successfully')
            return redirect('crm:invoice-setting')
    
    context = {
        'instance': instance,
        'form' : form,
    }
    return render(request, 'invoices/invoice-setting.html', context)




@login_required(login_url='crm:login')
@permission_required("crm.view_invoice", raise_exception=True)
def invoices(request):
    invoices = Invoice.objects.all().order_by('-id')
    
    context = {
        'invoices': invoices
    }
    return render(request, 'invoices/invoices.html', context)



@login_required(login_url='crm:login')
@permission_required("crm.add_invoice", raise_exception=True)
def addInvoice(request):
    cp = InvoiceSetting.objects.first()
    settings = InvoiceSetting.objects.first()
    clients = Contact.objects.filter(role=3)
    items = Item.objects.all()
    discounts = Discount.objects.all()
    taxes = Tax.objects.all()
    
    
    if request.method == 'POST':
        client = get_object_or_404(Contact, id=request.POST.get('client')) 
        title = request.POST.get('title')
        due_date = request.POST.get('due_date')
        internal_notes = request.POST.get('internal_notes')
        items_list = request.POST.getlist('items')
        discounts_list = request.POST.getlist('discounts')
        taxes_list = request.POST.getlist('taxes')
        
        sub_total = request.POST.get('sub_total')
        discounts_total = request.POST.get('discounts_total')
        taxes_total = request.POST.get('taxes_total')
        grand_total = request.POST.get('grand_total')
        
        terms_and_conditions = request.POST.get('terms_and_conditions')
        payment_description = request.POST.get('payment_description')
        file = request.FILES.get('file')
        
        
        invoice = Invoice.objects.create(
            title = title,
            client = client,
            invoice_number = f'{cp.invoice_prefix}{datetime.now().strftime("%Y%m%d%H%M%S")}',
            due_date = due_date,
            internal_notes = internal_notes,
            terms_and_conditions = terms_and_conditions,
            payment_description = payment_description,
            sub_total = sub_total,
            taxes_total = taxes_total,
            discounts_total = discounts_total,
            grand_total = grand_total
        )
            
        for i in items_list:
            InvoiceItem.objects.create(
                invoice = invoice,
                item = get_object_or_404(Item, id=i)
            )
            
        for i in discounts_list:
            InvoiceDiscount.objects.create(
                invoice = invoice,
                discount = get_object_or_404(Discount, id=i)
            )
            
        for i in taxes_list:
            InvoiceTax.objects.create(
                invoice = invoice,
                tax = get_object_or_404(Tax, id=i)
            )
            
        if file:
            InvoiceFile.objects.create(
                Invoice = invoice, 
                file = file           
            )
        
        
        messages.success(request, 'Invoice generated successfully')
        return redirect('crm:view-invoice', invoice.invoice_number)
        
        
    
    context = {
        'settings' : settings,
        'clients' : clients,
        'items' : items,
        'discounts' : discounts,
        'taxes' : taxes,
    }
    return render(request, 'invoices/add-invoice.html', context)




@login_required(login_url='crm:login')
@permission_required("crm.view_invoice", raise_exception=True)
def viewInvoice(request, inv_no):
    cp = InvoiceSetting.objects.first()
    invoice = get_object_or_404(Invoice, invoice_number=inv_no)
    form = InvoiceUpdateForm(instance=invoice)

    if request.method == "POST":
        if 'update' in request.POST:
            form = InvoiceUpdateForm(request.POST, instance=invoice)
            if form.is_valid():
                form.save()
                messages.success(request, 'Invoice updated successfully')
                return HttpResponseRedirect(request.path_info)
    
    context = {
        'invoice' : invoice,
        'cp' : cp,
        'form' : form
    }
    return render(request, 'invoices/view-invoice.html', context)


@login_required(login_url='crm:login')
@permission_required("crm.delete_invoice", raise_exception=True)
def deleteInvoice(request, id):
    instance = get_object_or_404(Invoice, id=id)
    instance.delete()
    messages.info(request, 'Invoice deleted successfully')
    return redirect('crm:invoices')





@login_required(login_url='crm:login')
@permission_required("crm.view_estimatesetting", raise_exception=True)
def estimateSetting(request):
    instance = EstimateSetting.objects.first()
    
    form = EstimateSettingForm(instance=instance)
    
    if request.method == 'POST':
        form = EstimateSettingForm(request.POST, request.FILES, instance=instance)
        
        if form.is_valid():
            form.save()
            messages.success(request, 'Estimate settings updated successfully')
            return redirect('crm:estimate-setting')
    
    context = {
        'instance': instance,
        'form' : form,
    }
    return render(request, 'estimates/estimate-settings.html', context)



@login_required(login_url='crm:login')
@permission_required("crm.view_estimate", raise_exception=True)
def estimates(request):
    estimates = Estimate.objects.all().order_by('-id')
    
    context = {
        'estimates': estimates
    }
    return render(request, 'estimates/estimates.html', context)




@login_required(login_url='crm:login')
@permission_required("crm.add_estimatesetting", raise_exception=True)
def addEstimate(request):
    cp = EstimateSetting.objects.first()
    settings = EstimateSetting.objects.first()
    clients = Contact.objects.filter(role=3)
    items = Item.objects.all()
    discounts = Discount.objects.all()
    taxes = Tax.objects.all()
    
    
    if request.method == 'POST':
        client = get_object_or_404(Contact ,id=request.POST.get('client')) 
        title = request.POST.get('title')
        due_date = request.POST.get('due_date')
        internal_notes = request.POST.get('internal_notes')
        items_list = request.POST.getlist('items')
        discounts_list = request.POST.getlist('discounts')
        taxes_list = request.POST.getlist('taxes')
        
        sub_total = request.POST.get('sub_total')
        discounts_total = request.POST.get('discounts_total')
        taxes_total = request.POST.get('taxes_total')
        grand_total = request.POST.get('grand_total')
        
        terms_and_conditions = request.POST.get('terms_and_conditions')
        payment_description = request.POST.get('payment_description')
        file = request.FILES.get('file')
        
        
        estimate = Estimate.objects.create(
            title = title,
            client = client,
            estimate_number = f'{cp.estimate_prefix}{datetime.now().strftime("%Y%m%d%H%M%S")}',
            due_date = due_date,
            internal_notes = internal_notes,
            terms_and_conditions = terms_and_conditions,
            payment_description = payment_description,
            sub_total = sub_total,
            taxes_total = taxes_total,
            discounts_total = discounts_total,
            grand_total = grand_total
        )
        
        for i in items_list:
            EstimateItem.objects.create(
                estimate = estimate,
                item = get_object_or_404(Item, id=i)
            )
            
        for i in discounts_list:
            EstimateDiscount.objects.create(
                estimate = estimate,
                discount = get_object_or_404(Discount, id=i)
            )
            
        for i in taxes_list:
            EstimateTax.objects.create(
                estimate = estimate,
                tax = get_object_or_404(Tax, id=i)
            )
            
        if file:
            EstimateFile.objects.create(
                estimate = estimate, 
                file = file           
            )
        
        
        messages.success(request, 'Estimate generated successfully')
        return redirect('crm:view-estimate', estimate.estimate_number)
        
        
    
    context = {
        'settings' : settings,
        'clients' : clients,
        'items' : items,
        'discounts' : discounts,
        'taxes' : taxes,
    }
    return render(request, 'estimates/add-estimate.html', context)





@login_required(login_url='crm:login')
@permission_required("crm.view_estimate", raise_exception=True)
def viewEstimate(request, est_no):
    cp = EstimateSetting.objects.first()
    estimate = get_object_or_404(Estimate, estimate_number=est_no)
    form = EstimateUpdateForm(instance=estimate)
    
    if request.method == "POST":
        if 'update' in request.POST:
            form = EstimateUpdateForm(request.POST, instance=estimate)
            if form.is_valid():
                form.save()
                messages.success(request, 'Estimate updated successfully')
                return HttpResponseRedirect(request.path_info)
    
    context = {
        'estimate' : estimate,
        'cp' : cp,
        'form' : form
    }
    return render(request, 'estimates/view-estimate.html', context)


@login_required(login_url='crm:login')
@permission_required("crm.delete_estimate", raise_exception=True)
def deleteEstimate(request, id):
    instance = get_object_or_404(Estimate, id=id)
    instance.delete()
    messages.info(request, 'Quote deleted successfully')
    return redirect('crm:estimates')



@login_required(login_url='crm:login')
@permission_required("crm.view_template", raise_exception=True)
def templates(request):
    templates = Template.objects.all()
    
    context = {
        'templates': templates
    }
    return render(request, 'documents/templates.html', context)

@login_required(login_url='crm:login')
@permission_required("crm.view_template", raise_exception=True)
def viewTemplate(request, pk):
    instance = get_object_or_404(Template, id=pk)
    
    context = {
        'instance': instance,
    }
    return render(request, 'documents/view-template.html', context)

@login_required(login_url='crm:login')
@permission_required("crm.add_template", raise_exception=True)
def addTemplate(request):
    form = TemplateForm()
    
    if request.method == 'POST':
        form = TemplateForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            
            messages.success(request, 'Template added successsfully')
            return redirect('crm:templates')
        
    context = {
        'form' : form,
    }
    return render(request, 'documents/add-template.html', context)

@login_required(login_url='crm:login')
@permission_required("crm.change_template", raise_exception=True)
def updateTemplate(request, pk):
    instance = get_object_or_404(Template, id=pk)
    
    form = TemplateForm(instance=instance)
    
    if request.method == 'POST':
        form = TemplateForm(request.POST, request.FILES, instance=instance)
        if form.is_valid():
            form.save()
            
            messages.success(request, 'Template updated successsfully')
            return redirect('crm:templates')
    
    context = {
        'form' : form,
        'instance' : instance,
    }
    return render(request, 'documents/update-template.html', context)

@login_required(login_url='crm:login')
@permission_required("crm.delete_template", raise_exception=True)
def deleteTemplate(request, pk):
    instance = get_object_or_404(Template, id=pk)
    instance.delete()
    messages.info(request, 'Template deleted successfully')
    return redirect('crm:templates')




@login_required(login_url='crm:login')
@permission_required("crm.view_document", raise_exception=True)
def documents(request):
    documents = Document.objects.all()
    
    context = {
        'documents': documents
    }
    return render(request, 'documents/documents.html', context)



@login_required(login_url='crm:login')
@permission_required("crm.view_document", raise_exception=True)
def viewDocument(request, pk):
    instance = get_object_or_404(Document, id=pk)
    
    context = {
        'instance': instance,
    }
    return render(request, 'documents/view-document.html', context)



@login_required(login_url='crm:login')
@permission_required("crm.add_document", raise_exception=True)
def addDocument(request):
    templates = Template.objects.all()
    form = DocumentForm()
    
    if request.method == 'POST':
        form = DocumentForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            
            messages.success(request, 'Document added successsfully')
            return redirect('crm:documents')
        
    context = {
        'form' : form,
        'templates' : templates,
    }
    return render(request, 'documents/add-document.html', context)



@login_required(login_url='crm:login')
@permission_required("crm.change_document", raise_exception=True)
def updateDocument(request, pk):
    instance = get_object_or_404(Document, id=pk)
    
    templates = Template.objects.all()
    
    form = DocumentForm(instance=instance)
    
    if request.method == 'POST':
        form = DocumentForm(request.POST, request.FILES, instance=instance)
        if form.is_valid():
            form.save()
            
            messages.success(request, 'Document updated successsfully')
            return redirect('crm:documents')
    
    context = {
        'form' : form,
        'instance' : instance,
        'templates' : templates,
    }
    return render(request, 'documents/update-document.html', context)




@login_required(login_url='crm:login')
@permission_required("crm.delete_document", raise_exception=True)
def deleteDocument(request, pk):
    instance = get_object_or_404(Document, id=pk)
    instance.delete()
    messages.info(request, 'Document deleted successfully')
    return redirect('crm:documents')



