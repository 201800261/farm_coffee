from dataclasses import field
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User, Group
from django.dispatch import receiver
from django.db.models.signals import post_save
from .models import Order, Product, Profile, Review


# Forms creation

class EmployeeForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2')

    def save(self, commit=True):
        user = super(EmployeeForm, self).save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
            group = Group.objects.get(name='Employee')
            user.groups.add(group)
        return user


class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email')

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ("__all__")
        exclude = ('user',)



# Product Form
class ProductForm(forms.ModelForm):
    # user = forms.ChoiceField(widget=forms.HiddenInput(), initial=User.id)
    
    class Meta:
        model = Product
        fields = ("__all__")

# Total Order Form
class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ("__all__")

# Review Form
class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ('users_fk_user_id', 'product_fk_product_id', 'rating', 'review_description')




