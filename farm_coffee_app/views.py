from asyncio import proactor_events
from itertools import chain
from multiprocessing import context
from pyexpat import model
from re import template
from urllib.request import ProxyDigestAuthHandler
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse
from numpy import product
from pytz import timezone
from .forms import ProductForm, SignUpForm
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm, PasswordResetForm
from django.core.mail import send_mail, BadHeaderError
from django.contrib.auth.models import User
from django.template.loader import render_to_string
from django.db.models.query_utils import Q
from django.utils.http import urlsafe_base64_encode
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_bytes
from django.views import generic
from .forms import *
from .models import Product, Profile, Review, Order, Cart
import traceback
from datetime import datetime
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
import pandas as pd
import numpy as np
from sklearn.neighbors import NearestNeighbors
import csv



# Create your views here.

# Sign-Up, Log-In, and Password-reset
# @login_required(login_url='login')
def home(request):
    products = Product.objects.filter(pub_date__lte=datetime.now()).order_by('-pub_date')[0:4]
    return render(request, 'home.html', {"products": products})

# @login_required(login_url='login')
def menu(request):
    return render(request, 'menu.html', {})

def register_request(request):
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f"New account created: {username}")
            login(request, user, backend='django.contrib.auth.backends.ModelBackend')
        else:
            messages.error(request, "Account creation failed")

        return redirect("farm_coffee_app:home")
    form = SignUpForm()
    return render(request, "register.html", {"form": form})

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
                return redirect("farm_coffee_app:home")
            else:
                messages.error(request, "Invalid username or password.")
        else:
            messages.error(request, "Invalid username or password.")
    form = AuthenticationForm()
    return render(request=request, template_name="login.html", context={"login_form":form})

def logout_request(request):
    logout(request)
    messages.info(request, "You have successfully logged out.")
    return redirect("farm_coffee_app:home")

@login_required(login_url='login')
def user_details(request, user_id):
    return HttpResponse("User details %s" % user_id)

def password_reset_request(request):
    if request.method == "POST":
        password_reset_form = PasswordResetForm(request.POST)
        if password_reset_form.is_valid():
            data = password_reset_form.cleaned_data['email']
            associated_users = User.objects.filter(Q(email=data))
            if associated_users.exists():
                for user in associated_users:
                    subject = "Password Reset Requested"
                    email_template_name = "password/password_reset_email.txt"
                    c = {
                        "email":user.email,
                        'domain':'127.0.0.1:8000',
                        'site_name': 'Farm Coffee',
                        'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                        "user": user,
                        'token': default_token_generator.make_token(user),
                        'protocol': 'http',
                    }
                    email = render_to_string(email_template_name, c)
                    try:
                        send_mail(subject, email, 'admin@fcoffee.com', [user.email], fail_silently=False)
                    except BadHeaderError:
                        return HttpResponse('Invalid header found.')
                    return redirect ("/password_reset/done/")
    password_reset_form = PasswordResetForm()
    return render(request=request, template_name="password/password_reset.html", context={"password_reset_form":password_reset_form})

#Profile CRUD
@login_required(login_url='login')
def profilepage(request):
    if request.method == 'POST':
        user_form = UserForm(request.POST, instance=request.user)
        profile_form = ProfileForm(request.POST, instance=request.user.profile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, ('Your profile was successfully updated!'))
            return redirect('farm_coffee_app:profilepage')
        else:
            messages.error(request, ('Please correct the errors below.'))
    else:
        user_form = UserForm(instance=request.user)
        profile_form = ProfileForm(instance=request.user.profile)
    return render(request, 'profile_page.html', {
        'user_form': user_form,
        'profile_form': profile_form
    })


# class create_order(generic.CreateView):
#     model = Total_Order
#     template_name = 'order/total_order_form.html'
#     form_class= TotalOrderForm

#     def form_valid(self, form):
#         print("super", super().form_valid(form),)
#         return super().form_valid(form)

# class read_order(generic.DetailView):
# class read_order_list(generic.ListView):
# class delete_order(generic.DeleteView):

#Product CRUD
class create_product(LoginRequiredMixin, generic.CreateView):
    model = Product
    template_name = 'product/product_form.html'
    form_class = ProductForm
    success_url = '/list' 

    def get_context_data(self, **kwargs):
        ctx = super(create_product, self).get_context_data(**kwargs)
        prods = Product.objects.all()
        cates = []
        for prod in prods:
            if prod.category is not None and not prod.category in cates:
                cates.append(prod.category)
        ctx["cates"] = cates
        return ctx

    def form_valid(self, form):
        
        print("super", super().form_valid(form),)
        return super().form_valid(form)

class read_product_list(LoginRequiredMixin, generic.ListView):
    template_name = 'product/read_product_list.html'
    context_object_name = 'view_product_list'

    def get_queryset(self):
        return Product.objects.filter(pub_date__lte=datetime.now()).order_by('-pub_date')
        

class read_product_detail(LoginRequiredMixin, generic.DetailView):
    model = Product
    template_name = 'product/read_product_detail.html'
    
    def get_queryset(self):
        return Product.objects.filter(pub_date__lte=datetime.now()).order_by('-pub_date')

    # def get_context_data(self):
    #     products = Product.objects.get(product_id=self.kwargs.get('pk'))

    #     reviews = Review.objects.all().filter(product_fk_product_id=self.kwargs.get('pk'))
    #     return {"products":products, "reviews":reviews}



class update_product(LoginRequiredMixin, generic.UpdateView):
    model = Product
    fields = ['name', 'price', 'image', 'availability']
    template_name= 'product/update_product.html'
    success_url = '/details/{product_id}'
    def get_object(self, queryset=None):
        id = self.kwargs.get('pk')
        return get_object_or_404(Product, product_id=id)

class delete_product(LoginRequiredMixin, generic.DeleteView):
    model = Product
    template_name = 'product/confirm_delete_product.html'
    success_url = '/list'

#Topping CRUD
# class create_topping(generic.CreateView):
# class read_topping(generic.DetailView):
# class read_topping_list(generic.ListView):
# class update_topping(generic.UpdateView):
# class delete_topping(generic.DeleteView):

#Review CRUD --- rewrite it using function based


# class create_review(generic.CreateView):
#     model = Review
#     template_name = 'review/review_form.html'
#     form_class = ReviewForm
#     success_url = '/details/5'
#     def form_valid(self, form):
#         product_fk_product_id=form.cleaned_data['product_fk_product_id']
#         rating= form.cleaned_data['rating']
#         review_description =form.cleaned_data['review_description']
#         try:
#             review = Review(
#                 users_fk_user_id=self.request.user,
#                 product_fk_product_id=Product.objects.get(product_id=product_fk_product_id),
#                 rating=rating,
#                 review_description= review_description)
#             review.save()
#             messages.success(self.request, "review has been created")
#         except:
#             messages.success(self.request, "review was not created")
       
#         return super().form_valid(form)

# Functions dealing with Reviews
@login_required(login_url='login')
def create_review(request):
    product_fk_product_id=request.POST['product_fk_product_id']
    print(request.user)
    review=Review(
        users_fk_user_id=request.user,
        product_fk_product_id=Product.objects.get(product_id=product_fk_product_id),
        rating=request.POST['rating'],
        review_description= request.POST['review_description'])
    review.save()

    messages.success(request, "review has been created")
    return HttpResponseRedirect(reverse('farm_coffee_app:read_product_list'))
     

class read_review(LoginRequiredMixin, generic.ListView):
    template_name = 'product/read_product_detail.html'
    context_object_name = 'view_reviews'

    def get_queryset(self):
        return Review.objects.all()

class update_review(LoginRequiredMixin, generic.UpdateView):
    model = Review
    fields = ['rating', 'review_description']
    template_name= 'review/update_review.html'
    success_url = '/list'
    # success_url = '/details/{product_fk_product_id}'
    # def get_object(self, queryset=None):
    #     id = self.kwargs.get('pk')
    #     return get_object_or_404(Review, product_fk_product_id=id)

class delete_review(LoginRequiredMixin, generic.DeleteView):
    model = Review
    template_name = 'review/confirm_delete_review.html'
    success_url = '/list'

# Functions dealing with the cart  
# @login_required(login_url='login')  
# def read_cart(request):
#     profile = Profile.objects.get(user=request.user)
#     items = Cart.objects.get(user=profile.user)
#     context = {'items': items, 'total_price': retrieve_total_price(request), 'cart_items': retrieve_cart_items(request)}
#     return render(request, 'cart/cart.html', context)
  

# Getting total amount of items in the cart
# @login_required(login_url='login')  
# def retrieve_cart_items(request):
#     total_items = ''
#     try:
#         user = Profile.objects.get(user=request.user)
#         cart = Cart.objects.get(user=user)
#         total_items = cart.get_total_items
#     except:
#         total_items = 0
#         messages.info(request,"The cart is empty")
    
#     return total_items

# Getting total price of items in the cart
# @login_required(login_url='login')  
# def retrieve_total_price(request):
#     total_price = 0
#     try:
#         user = Profile.objects.get(user=request.user)
#         cart = Cart.objects.get(user=user)
#         total_price = cart.get_total_price
#     except:
#         total_price = 0
#         messages.info(request,"No items")
#     return total_price

# Cart Checkout Function
# @login_required(login_url='login')  
# def cart_checkout(request):
#     user = Profile.objects.get(user=request.user)
#     context = {'cart_items': retrieve_cart_items(request), 'total_price': retrieve_total_price(request)}
    # if request.method == 'POST':
    #     form = TotalOrderForm(request.POST)
    #     if form.is_valid():
    #         order = form.save()
    #         cart = Cart.objects.filter(user=user)[0]
    #         for cart in cart:
    #             item = Item.objects.create(order=order, product=cart.product)
    #             Quantity.objects.create(item=item, quantity=cart.cart_quantity)
    #             Cart.objects.filter(user=user).delete()			
    #         return redirect('store')
    #     error = form.errors
    #     for e in error:
    #         error = e
    #     messages.warning(request,' is not valid')
    #     return redirect('cart_checkout')
    # return render(request, 'checkout/checkout.html', context)

# Add to cart function
# @login_required(login_url='login')  
# def add_to_cart(request):
#     cart = Cart.objects.get(user=Cart.user)
#     products = Product.objects.get()
#     if cart:
# 		existed_item = Cart.objects.filter(user=user, product=products)
# 		if existed_item:
# 			existed_item.update(quantity=F('quantity') + 1)
# 		else:
# 			Cart.objects.create(user=user, product=products, quantity=1).save()
# 	else:
# 		Cart.objects.create(user=user, product=products, quantity=1)	
    




# class checkout(LoginRequiredMixin, generic.ListView):
#     template_name = 'checkout/checkout.html'

def recommendations_views(request):
    reviews = pd.read_csv(r"recommendation_engine\reviews.csv", usecols=['userId', 'productId', 'rating'])
    products = pd.read_csv(r'recommendation_engine\products.csv', usecols=['productId', 'title'])
    reviews2 = pd.merge(reviews, products, how='inner', on='productId')

    current_user = request.user
    user = current_user.id(object)

    df = reviews2.pivot_table(index='title',columns='userId',values='rating').fillna(0)
    df1 = df.copy()

    num_neighbors = 10
    num_recommendation = 10
    
    number_neighbors = num_neighbors
    
    knn = NearestNeighbors(metric='cosine', algorithm='brute')
    knn.fit(df.values)
    distances, indices = knn.kneighbors(df.values, n_neighbors=number_neighbors)
    
    user_index = df.columns.tolist().index(user)
    
    for p,t in list(enumerate(df.index)):
        if df.iloc[p, user_index] == 0:
            sim_products = indices[p].tolist()
            product_distances = distances[p].tolist()
            
            if p in sim_products:
                id_product = sim_products.index(p)
                sim_products.remove(p)
                product_distances.pop(id_product)
                
            else:
                sim_products = sim_products[:num_neighbors-1]
                product_distances = product_distances[:num_neighbors-1]
                
            product_similarity = [1-x for x in product_distances]
            product_similarity_copy = product_similarity.copy()
            nominator = 0
            
            for s in range(0, len(product_similarity)):
                if df.iloc[sim_products[s], user_index] == 0:
                    if len(product_similarity_copy) == (number_neighbors - 1):
                        product_similarity_copy.pop(s)
                        
                    else:
                        product_similarity_copy.pop(s-(len(product_similarity)-len(product_similarity_copy)))
                        
                else:
                    nominator = nominator + product_similarity[s]*df.iloc[sim_products[s],user_index]
                    
            if len(product_similarity_copy) > 0:
                if sum(product_similarity_copy) > 0:
                    predicted_r = nominator/sum(product_similarity_copy)
                    
                else:
                    predicted_r = 0
                    
            else:
                predicted_r = 0
                
            df1.iloc[p,user_index] = predicted_r
    
    recommended_products = []

    for m in df[df[user] == 0].index.tolist():
        index_df = df.index.tolist().index(m)
        predicted_rating = df1.iloc[index_df, df1.columns.tolist().index(user)]
        recommended_products.append((m, predicted_rating))

    sorted_rm = sorted(recommended_products, key=lambda x:x[1], reverse=True)
     
    recommendations = sorted_rm[:num_recommendation]
    recommendations = [ x[0] for x in recommendations]

    return render(request, "recommendations/recommendation.html", {'recommendations':recommendations})