from django.contrib import auth
from django.shortcuts import render,redirect
from django.core.paginator import Paginator,EmptyPage

from User.models import Registration,Blog


# Create your views here.

def home(request):
    return render(request,'Admin/home.html')


def users_view(request):

    details=Registration.objects.all()

    # Instantiate the Paginator with the queryset and number of items per page
    paginator = Paginator(details, 4)
    page_number = request.GET.get('page')  # Get the page number from the request

    try:
        # Get the specific page of results
        page = paginator.get_page(page_number)
    except EmptyPage:
        # Handle the case where the page is out of range
        page = paginator.page(paginator.num_pages)

    # Pass the paginated results to the template

    return render(request,'Admin/usersview.html',{'details':details,'page': page})


def deleteuser(request, user_id):
    try:
        user = Registration.objects.get(id=user_id)
    except Registration.DoesNotExist:
        # Handle case where book does not exist
        return redirect('users_view')  # Redirect to a book list page or another page

    if request.method == 'POST':
        user.delete()  # Delete the book if the request is POST
        return redirect('users_view')  # Redirect to the home page or book list after deletion

    return render(request, 'Admin/deleteuser.html', {'user': user})  # Render the confirmation pageder(request,'delete.html', {'book':book})

def Logout(request):
   auth.logout(request)
   return redirect('Guesthome')



def blogsview(request):
    blogs = Blog.objects.all()

    return render(request, 'Admin/blogsview.html',{'blogs': blogs})




def blogdelete(request, blog_id):

    try:
        blog = Blog.objects.get(id=blog_id)
    except Blog.DoesNotExist:
        return redirect('blogsview')

    if request.method == 'POST':
        blog.delete()
        return redirect('blogsview')



    return render(request, 'Admin/blogdelete.html', {'blog': blog})