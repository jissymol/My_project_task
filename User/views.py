from django.contrib.auth.decorators import login_required
from django.shortcuts import render
import re
from .forms import BlogForm,RegisterForm,CommentForm
from .models import Registration,Logintable,Blog,Comment
from django.contrib import messages,auth
from django.shortcuts import render, redirect, get_object_or_404

# Create your views here.


def user_registration(request):
    login_table = Logintable()
    userprofile = Registration()

    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        contact = request.POST['number']
        password1 = request.POST['password1']
        password2 = request.POST['password2']

        # Check if the username or email already exists
        if Registration.objects.filter(username=username).exists():
            messages.error(request, 'Username already exists. Please choose a different username.')
            return render(request, 'User/userregister.html')

        if Registration.objects.filter(email=email).exists():
            messages.error(request, 'Email is already registered. Please use a different email.')
            return render(request, 'User/userregister.html')

        # Check if the contact number is valid and unique
        if not re.match(r'^\d{10}$', contact):
            messages.error(request, 'Please enter a valid 10-digit contact number.')
            return render(request, 'User/userregister.html')

        if Registration.objects.filter(contact=contact).exists():
            messages.error(request, 'This contact number is already registered.')
            return render(request, 'User/userregister.html')

        # Populate user profile data
        userprofile.username = username
        userprofile.firstname = request.POST['firstname']
        userprofile.lastname = request.POST['lastname']
        userprofile.email = email
        userprofile.contact = contact

        # Check if 'photo' exists in request.FILES
        if 'photo' in request.FILES:
            userprofile.photo = request.FILES['photo']
        else:
            messages.error(request, 'Please upload a photo.')
            return render(request, 'User/userregister.html')

        userprofile.password1 = password1
        userprofile.password2 = password2

        login_table.username = username
        login_table.password1 = password1
        login_table.password2 = password2
        login_table.type = 'user'

        # Validate passwords match
        if password1 == password2:
            userprofile.save()
            login_table.save()

            messages.success(request, 'Registration successful')
            return redirect('login')
        else:
            messages.error(request, 'Passwords do not match.')
            return render(request, 'User/userregister.html')

    return render(request, 'User/userregister.html')
def loginpage(request):
    if request.method == 'POST':
        username = request.POST.get('username')  # Safely get the username
        password = request.POST.get('password1')  # Safely get the password


        user = Logintable.objects.filter(username=username, password1=password, type='user').exists()
        try:
            if user is not None:
                user_details = Logintable.objects.get(username=username, password1=password)
                user_name = user_details.username
                user_type = user_details.type

                if user_type == 'user':
                    request.session['username'] = user_name
                    return redirect('userhome')

                elif user_type == 'admin':
                    request.session['username'] = user_name
                    return redirect('/Admin/home')

            else:
                messages.error(request, 'Invalid username or password.')

        except:
                messages.error(request, 'An error occurred: ')

    else:
            messages.error(request, 'Username and password are required.')

    return render(request, 'User/login.html')
@login_required(login_url='login')  # Ensures only authenticated users access this page
def user_view(request):

    if 'username' not in request.session:
        return redirect('login')

    username = request.session['username']

    user = get_object_or_404(Registration, username=username)

    return render(request, 'User/user_view.html', {'user': user})

def Logout(request):
   auth.logout(request)
   return redirect('Guesthome')


#def update_profile(request, user_id):
 # details=Registration.objects.get(id=user_id)
  #if request.method=='POST':
   #   form=RegisterForm(request.POST,request.FILES,instance=details)

    #  if form.is_valid():
     #     form.save()

      #    return redirect('listbook')


  #else:

   #   form = RegisterForm(instance=Boodetailsk)

  #return render(request, 'User/updateprofile.html', {'form': form})  # Pass3

def Guesthome(request):
    return render(request, 'User/main.html')





def uploadblogs(request):
    if 'username' not in request.session:
        messages.error(request, "Please log in first.")
        return redirect('login')

    user = get_object_or_404(Registration, username=request.session['username'])
    form = BlogForm()

    if request.method == 'POST':
        form = BlogForm(request.POST, request.FILES)
        if form.is_valid():
            blog = form.save(commit=False)
            blog.userid = user
            blog.save()
            messages.success(request, 'Blog uploaded successfully!')
            return redirect('uploadblogs')  # Redirect to a blog list or dashboard page
        else:
            messages.error(request, 'Please correct the errors below.')

    return render(request, 'User/uploadblogs.html', {'form': form, 'user': user})


def photo(request):
    if 'username' not in request.session:
        return redirect('login')


    username = request.session['username']


    user = get_object_or_404(Registration, username=username)


    blogs = Blog.objects.filter(userid=user)

    for blog in blogs:
        print(blog.title, blog.description, blog.blog_images, blog.Date)

    return render(request, 'User/photos.html', {'blogs': blogs,'user':user})



def userhome(request):

    if 'username' not in request.session:
        return redirect('login')

    username = request.session['username']

    user = get_object_or_404(Registration, username=username)

    return render(request, 'User/userhome.html', {'user': user})



def blogs(request):
    if 'username' not in request.session:
        return redirect('login')

    username = request.session['username']
    blogs = Blog.objects.select_related('userid').all()

    user = get_object_or_404(Registration, username=username)
    return render(request, 'User/blogs.html',{'user': user,'blogs': blogs})



def profile(request):

    if 'username' not in request.session:
        return redirect('login')

    username = request.session['username']

    user = get_object_or_404(Registration, username=username)

    blogs = Blog.objects.filter(userid=user)

    for blog in blogs:
        print(blog.title, blog.description, blog.blog_images, blog.Date)

    return render(request, 'User/profile.html', {'blogs': blogs, 'user': user})



def updateprofile(request):
    if 'username' not in request.session:
        return redirect('login')

    username = request.session['username']
    user = get_object_or_404(Registration, username=username)

    if request.method == 'POST':
        form = RegisterForm(request.POST, request.FILES, instance=user)

        if form.is_valid():
            form.save()
            return redirect('updateprofile')
        else:
            return render(request, 'User/updateprofile.html', {'form': form, 'user': user})
    else:

        form = RegisterForm(instance=user)

    return render(request, 'User/updateprofile.html', {'form': form, 'user': user})

def deleteblog(request, blog_id):
    if 'username' not in request.session:
        return redirect('login')

    username = request.session['username']
    user = get_object_or_404(Registration, username=username)
    try:
        blog = Blog.objects.get(id=blog_id)
    except Blog.DoesNotExist:
        return redirect('profile')

    if request.method == 'POST':
        blog.delete()
        return redirect('profile')



    return render(request, 'User/deleteblog.html', {'blog': blog,'user':user})


def comment(request):
    if 'username' not in request.session:
        messages.error(request, "Please log in first.")
        return redirect('login')

    user = get_object_or_404(Registration, username=request.session['username'])

    if request.method == 'POST':
        blog_id = request.POST.get('blogid')  # Get the blogid from the form
        print(f"Received blog ID: {blog_id}")  # Debugging

        if not blog_id:
            messages.error(request, "Blog ID is missing or invalid.")
            return redirect('blogs')

        try:
            blog = Blog.objects.get(id=blog_id)  # Attempt to retrieve the blog by ID
        except Blog.DoesNotExist:
            messages.error(request, "The blog does not exist.")
            return redirect('blogs')  # Redirect to blogs page if the blog doesn't exist

        form = CommentForm(request.POST, request.FILES)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.blogid = blog  # Set the blogid field to the retrieved blog
            comment.userid = user
            comment.save()
            messages.success(request, "Comment posted successfully!")
            return redirect('blogs')  # Redirect after successful comment
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = CommentForm()

    return render(request, 'User/comments.html', {'form': form, 'user': user})

def updateblog(request, blog_id):
    if 'username' not in request.session:
        return redirect('login')

    username = request.session['username']
    user = get_object_or_404(Registration, username=username)
    blog = get_object_or_404(Blog, id=blog_id)

    if request.method == 'POST':
        form = BlogForm(request.POST, request.FILES, instance=blog)
        if form.is_valid():
            form.save()
            return redirect('profile')
        else:

            print(form.errors)

    else:
        form = BlogForm(instance=blog)

    return render(request, 'User/updateblog.html', {'form': form, 'user': user})



def view_comments(request, blog_id):
    if 'username' not in request.session:
        messages.error(request, "Please log in first.")
        return redirect('login')


    blog = get_object_or_404(Blog, id=blog_id)
    comments = Comment.objects.filter(blogid=blog)  # Fetch comments for this blog

    print("Comments:", comments)  # Deb Fetch comments for this blog

    return render(request, 'User/view_comments.html', {'blog': blog, 'comments': comments})