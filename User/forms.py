from django import forms
from .models import Logintable, Registration,Blog,Comment


class RegisterForm(forms.ModelForm):

    class Meta:  # Corrected from Mate to Meta
        model = Registration  # Specify the model the form is based on
        fields = ['username','firstname','lastname','email','contact','photo']  # Corrected from Fields='__alt__' to fields='__all__'


        widgets={
            'firstname':forms.TextInput(attrs={'class':'form-control','placeholder':'Enter the book name'}),
            'lastname': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter the author name'}),
            'email': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter the author name'}),
            'number': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Enter the book price'})

        }

class BlogForm(forms.ModelForm):
        class Meta:
            model = Blog
            fields = ['title', 'description', 'blog_images']



class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['comment', 'email']