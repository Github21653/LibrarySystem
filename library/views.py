from django.shortcuts import render
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.http import HttpResponseForbidden
from django.shortcuts import get_object_or_404
from django.utils import timezone
from datetime import timedelta

from library.forms import RegisterForm, LoginForm, AdminRegisterForm, RegisterBook
from library.models import Book, BookRequest
# Create your views here.

def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            messages.success(request, 'Account created successfully')
            return redirect('user_login')
    else:
        form = RegisterForm()
    return render(request, 'reader_register.html', {'form': form})


def user_login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            user =  authenticate(request, email=email, password=password)

            if user is not None:
                messages.success(request, 'Login successful')
                login(request, user)
                if user.is_admin:
                    return redirect('home')
                else:
                    return redirect('view_books')
            else:
                messages.error(request, 'Invalid email or password')
    else:
        form = LoginForm()
    return render(request, 'reader_login.html', {'form': form})

@login_required
def admin_register(request):
    print(request.user.is_superadmin)
    if not request.user.is_superadmin:
        return HttpResponseForbidden("You are not authorized to access this page.")
    
    if request.method == 'POST':
        form = AdminRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Admin account created successfully')
            return redirect('home')
    else:
        form = AdminRegisterForm()
    return render(request, 'admin_register.html', {'form': form})

def logout_user(request):
    logout(request)
    print("Logged Out")
    messages.success(request, "You have been logged out successfully.")
    return redirect('user_login')

#for testing 
#Now it is for adminHome 
@login_required
def home(request):
    books = Book.objects.all()
    return render(request, 'admin_base.html', {'books': books})


@login_required
@staff_member_required
def add_book(request):
    if request.method == 'POST':
        form = RegisterBook(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Book added successfully')
            print("Book saved")
        else:
            print("Book not saved: " + str(form.errors))
    else:
        form = RegisterBook()
    return render(request, 'add_book.html', {'form': form})

@login_required
def view_books(request):
    books = Book.objects.all()
    return render(request, 'view_books.html', {'books': books})

@login_required
def request_book(request,book_id):
    book = get_object_or_404(Book, id=book_id)

    existing_request = BookRequest.objects.filter(user=request.user, book=book, status='pending').exists()
    if existing_request:
        messages.error(request, 'You have already requested this book.')
        return redirect('view_books')
    
    BookRequest.objects.create(user=request.user, book=book, status='pending')
    messages.success(request, 'Book request submitted successfully.')
    print("Book request submitted")
    return redirect('my_requests')

@login_required
def my_requests(request):
    requests = BookRequest.objects.filter(user=request.user).order_by('-request_date')
    return render(request, 'my_requests.html', {'requests': requests})

@login_required
@staff_member_required
def manage_requests(request):
    requests = BookRequest.objects.filter(status='pending').order_by('request_date')
    return render(request, 'manage_requests.html', {'requests': requests})

@login_required
@staff_member_required
def process_request(request, request_id):
    if request.method == 'POST':
        book_request = get_object_or_404(BookRequest, id=request_id)
        action = request.POST.get('action')
        
        if action == 'approve':
            book_request.status = 'approved'
            book_request.approved_date = timezone.now()
            book_request.due_date = timezone.now() + timedelta(days=14)  # 2 weeks lending period
            messages.success(request, 'Book request approved.')
            print("Book Approved")
        elif action == 'reject':
            book_request.status = 'rejected'
            messages.success(request, 'Book request rejected.')
            print("Book Rejected")
        book_request.save()
    return redirect('manage_requests')

@login_required
@staff_member_required
def mark_returned(request, request_id):
    if request.method == 'POST':
        book_request = get_object_or_404(BookRequest, id=request_id)
        book_request.status = 'returned'
        book_request.save()
        messages.success(request, 'Book marked as returned.')
    return redirect('manage_requests')



