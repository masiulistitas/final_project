from .forms import UserForm
from django.contrib import messages
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import render, redirect, get_object_or_404
from django.core.mail import send_mail, BadHeaderError
from django.http import HttpResponse
from django.contrib.auth.forms import PasswordResetForm
from django.contrib.auth.models import User
from django.template.loader import render_to_string
from django.db.models.query_utils import Q
from django.utils.http import urlsafe_base64_encode
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_bytes
from django.contrib.auth.decorators import login_required
from .models import Note, Category
from .forms import NotesForm, CategoryForm


# Create your views here.

def index(request):
    return render(request, 'index.html')


@login_required
def search(request):
    query = request.GET.get('query')
    search_results = Note.objects.filter(Q(title__icontains=query), user=request.user)
    return render(request, 'search.html', {'search_results': search_results, 'query': query})


@login_required
def filter(request, id):
    categories = Category.objects.filter(user=request.user)
    obj = get_object_or_404(Category, id=id)
    context = {
        'obj': obj,
        'categories': categories,
    }
    return render(request, 'filter.html', context=context)


@login_required
def add_note(request):
    notes = Note.objects.filter(user=request.user)
    categories = Category.objects.filter(user=request.user)
    form = NotesForm(user=request.user)

    if request.method == 'POST':
        form = NotesForm(request.POST, request.FILES, user=request.user)
        if form.is_valid():
            form_data = form.save(commit=False)
            form_data.user = request.user
            form_data.save()
            messages.info(request, f"You have created a note.")
            return redirect('notes')

    context = {
        'form': form,
        "notes": notes,
        "categories": categories,

    }
    return render(request, "notes.html", context=context)


@login_required
def edit_note(request, id):
    categories = Category.objects.filter(user=request.user)
    notes = Note.objects.get(id=id)
    form = NotesForm(instance=notes, user=request.user)
    if request.method == 'POST':
        form = NotesForm(request.POST, request.FILES, user=request.user, instance=notes)
        if form.is_valid():
            form.save()
            messages.info(request, f"You have updated a note.")
            return redirect('notes')

    context = {
        'form': form,
        "notes": notes,
        'categories': categories,
    }
    return render(request, "edit_note.html", context=context)


@login_required
def update_category(request, id):
    categories = Category.objects.filter(user=request.user)
    update = Category.objects.get(id=id)
    form = CategoryForm(instance=update)

    if request.method == 'POST':
        form = CategoryForm(request.POST, instance=update)
        if form.is_valid():
            form.save()
            messages.info(request, f"You have updated a category.")
            return redirect('category')

    context = {
        'update': update,
        'form': form,
        'categories': categories,
    }
    return render(request, 'update_category.html', context=context)


@login_required
def add_category(request):
    categories = Category.objects.filter(user=request.user)
    form = CategoryForm()
    if request.method == 'POST':
        form = CategoryForm(request.POST, request.FILES)
        if form.is_valid():
            form_data = form.save(commit=False)
            form_data.user = request.user
            form_data.save()
            messages.info(request, f"You have created a category.")
            return redirect('category')

    context = {
        'form': form,
        'categories': categories,
    }
    return render(request, "add_category.html", context=context)


@login_required
def delete_note(request, id):
    notes = Note.objects.get(id=id)

    if request.method == 'POST':
        notes.delete()
        messages.info(request, f"You have deleted a note.")
        return redirect('notes')

    context = {
        'notes': notes,
    }
    return render(request, 'delete_note.html', context)


@login_required
def delete_category(request, id):
    category = Category.objects.get(id=id)

    if request.method == 'POST':
        category.delete()
        messages.info(request, f"You have deleted a category.")
        return redirect('category')

    context = {
        'category': category,
    }
    return render(request, 'delete_category.html', context)


def register_request(request):
    if request.method == "POST":
        form = UserForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Registration successful.")
            return redirect("notes")
        messages.error(request, "Unsuccessful registration. Invalid information.")
    form = UserForm()
    return render(request=request, template_name="register.html", context={"register_form": form})


def login_request(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.info(request, f"You are now logged in as {username}.")
                return redirect("notes")
            else:
                messages.error(request, "Invalid username or password.")
        else:
            messages.error(request, "Invalid username or password.")
    form = AuthenticationForm()
    return render(request=request, template_name="login.html", context={"login_form": form})


def logout_request(request):
    logout(request)
    messages.info(request, "You have successfully logged out.")
    return redirect("index")


def password_reset_request(request):
    if request.method == "POST":
        password_reset_form = PasswordResetForm(request.POST)
        if password_reset_form.is_valid():
            data = password_reset_form.cleaned_data['email']
            associated_users = User.objects.filter(Q(email=data))
            if associated_users.exists():
                for user in associated_users:
                    subject = "Password Reset Requested"
                    email_template_name = "password_reset_email.txt"
                    c = {"email": user.email, 'domain': '127.0.0.1:8000', 'site_name': 'Website',
                         "uid": urlsafe_base64_encode(force_bytes(user.pk)), "user": user,
                         'token': default_token_generator.make_token(user), 'protocol': 'http', }
                    email = render_to_string(email_template_name, c)
                    try:
                        send_mail(subject, email, 'admin@example.com', [user.email], fail_silently=False)
                    except BadHeaderError:
                        return HttpResponse('Invalid header found.')
                    return redirect("password_reset_done")
    password_reset_form = PasswordResetForm()
    return render(request=request, template_name="password_reset.html",
                  context={"password_reset_form": password_reset_form})
