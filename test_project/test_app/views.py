import re

from django.contrib import messages
from django.contrib.auth import (authenticate, login, logout,
                                 update_session_auth_hash)
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm, UserCreationForm
from django.http import HttpRequest
from django.shortcuts import HttpResponse, redirect, render
from rest_framework import generics
from rest_framework.request import Request
from rest_framework.test import APIRequestFactory

from .forms import *
from .models import *
from .serializers import *


def product_list(request):
    # products = Product.objects.all()
    products = Product.objects.select_related('category').all()
    return render(request, 'productList.html', {'products': products})

def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = RegistrationForm()

    return render(request, 'register.html', {'form': form})

def update_profile(request):
    try:
        user_profile = request.user.userprofile
    except UserProfile.DoesNotExist:
        user_profile = UserProfile(user=request.user)

    if request.method == 'POST':
        form = CombinedForm(request.POST, instance=user_profile)
        if form.is_valid():
            user_profile = form.save(commit=False)
            user_profile.user = request.user
            user_profile.save()
            return redirect('home')
    else:
        form = CombinedForm(instance=user_profile)

    return render(request, 'updateProfile.html', {'form': form})

def isAllPresent(str):
    regex = ("^(?=.*[a-z])(?=." +
            "*[A-Z])(?=.*\\d)" )
    p = re.compile(regex)
    if ((str != None) and (re.search(p, str)) and (len(str) >=6)):
        return True
    else:
        return False

def update_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        for field in form.fields.values():
            field.help_text = None



        if form.is_valid():
            form.fields['old_password'].help_text = None
            form.fields['new_password1'].help_text = None
            form.fields['new_password2'].help_text = None
            user = form.save()
            update_session_auth_hash(request, user)
            messages.success(request, 'Your password was successfully updated!')
            return redirect('home')
        else:
            form.fields['old_password'].help_text = None
            form.fields['new_password1'].help_text = None
            form.fields['new_password2'].help_text = None
            messages.error(request, 'Please correct the error below.')
    else:
        form = PasswordChangeForm(request.user)

    return render(request, 'updatePassword.html', {'form': form})

def user_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            print("if user is not None")
            #messages.error(request, 'Invalid login credentials. Please check your username and password.')
            return redirect('home')
        else:
            if User.objects.filter(username=username).exists():
                messages.error(request, 'Incorrect password. Please try again.')
            else:
                messages.error(request, 'Invalid login credentials. Please check your username and password.')
    
    return render(request, 'registration/login.html')


class ProductListByCategory(generics.ListAPIView):
    serializer_class = ProductSerializer

    def get_queryset(self):
        category_id = self.kwargs['category_id'] 
        return Product.objects.filter(category__id=category_id)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        category_id = self.kwargs['category_id']
        category = Category.objects.get(id=category_id)
        context['category_name'] = category.name
        return context

def render_category_products(request, category_id):
    view = ProductListByCategory.as_view()

    factory = APIRequestFactory()
    drf_request = factory.get(f'/products_by_category/{category_id}/')

    try:
        products_by_category = view(drf_request, category_id=category_id)

        if products_by_category.status_code == 200:
            django_request = HttpRequest()
            django_request.method = drf_request.method
            django_request.path_info = drf_request.path
            django_request.user = drf_request.user
            products_data = products_by_category.data
            first_product = products_data[0] if products_data else None
            if first_product:
                category_name = first_product.get('name', '')
            else:
                category_name = ''

            # Fetch reviews for products in the category
            product_ids = [product.get('id') for product in products_data]
            
            return render(request, 'products_by_category.html', {
                'category_name': category_name,
                'products': products_data,

            })
        else:
            return HttpResponse("Error fetching data", status=500)
    except Exception as e:
        return HttpResponse(f"Error: {str(e)}", status=500)
    
class ProductList(generics.ListAPIView):
    serializer_class = ProductSerializer

    def get_queryset(self):
        queryset = Product.objects.all()

        category_id = self.request.query_params.get('category_id', None)
        if category_id is not None:
            queryset = queryset.filter(category__id=category_id)

        ordering = self.request.query_params.get('ordering', None)
        if ordering is not None:
            queryset = queryset.order_by(ordering)

        return queryset

def submit_review(request, product_id):
    print("product_id", product_id)
    if request.method == 'POST':
        reviews = ProductReview.objects.filter(product__id=product_id)

        # Organize reviews by product id for easy access in the template
        reviews_by_product_id = {}
        for review in reviews:
            product_id = review.product.id
            if product_id not in reviews_by_product_id:
                reviews_by_product_id[product_id] = []
            reviews_by_product_id[product_id].append(review)
        
        print("reviews_by_product_id", reviews_by_product_id)

        form = ProductReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.user = request.user
            review.product_id = product_id
            review.save()
            messages.success(request, 'Your Review is successfully submitted !!')
            return render(request, 'submitReview.html', {'form': form, 'product_id': product_id, 'reviews_by_product_id': reviews_by_product_id})
            # return redirect('home')
    else:
        form = ProductReviewForm()

    return render(request, 'submitReview.html', {'form': form, 'product_id': product_id})

# @login_required
# def update_profile(request):
#     if request.method == 'POST':
#         form = UserProfileForm(request.POST, instance=request.user.userprofile)
#         if form.is_valid():
#             form.save()
#             return redirect('profile')
#     else:
#         form = UserProfileForm(instance=request.user.userprofile)

#     return render(request, 'updateProfile.html', {'form': form})

def user_logout(request):
    logout(request)
    return redirect('user_login')  

def home(request):
    categories = Category.objects.all()
    return render(request, 'home.html', {'categories': categories})






