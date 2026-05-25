import csv
import os
from django import forms
from django.conf import settings
from django.http import StreamingHttpResponse
from .camera import VideoCamera
from django.shortcuts import render, redirect
from django.contrib import messages
from streamapp.models import *  # Class names should be capitalized as per Python convention
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.models import User
from django.core.files.images import get_image_dimensions



# Instantiate the VideoCamera class
video_camera = VideoCamera()


def index(request):
    return render(request, 'streamapp/index.html')


def signin(request):
    if request.method == 'POST':
        username=request.POST.get('username')
        password=request.POST.get('password')
        user=authenticate(username=username,password=password)
        if user is not None:
            login(request,user)
            messages.success(request, "Login Successful")
            return redirect('/mainpage') 
        else:
            #  messages.warning(request, "Invalid Login Credentials")
            messages.error(request, "Invalid login")
    if not request.user.is_anonymous:
        return redirect('/mainpage')
    else:
        return render(request, 'streamapp/login.html')

class RegistrationForm(forms.Form):
    name = forms.CharField(max_length=100)
    username = forms.CharField(max_length=100)
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)
    repassword = forms.CharField(widget=forms.PasswordInput)
    age = forms.IntegerField()
    dob = forms.DateField()
    gender = forms.ChoiceField(choices=(('male', 'Male'), ('female', 'Female'), ('other', 'Other')))
    image = forms.ImageField()

    def clean_image(self):
        image = self.cleaned_data.get('image')
        if image:
            w, h = get_image_dimensions(image)
            # Validate dimensions or file size if necessary
        return image

def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST, request.FILES)
        if form.is_valid():
            cleaned_data = form.cleaned_data
            username = cleaned_data['username']
            email = cleaned_data['email']
            password = cleaned_data['password']
            name = cleaned_data['name']
            age = cleaned_data['age']
            dob = cleaned_data['dob']
            gender = cleaned_data['gender']
            image = request.FILES.get('image', None)

            if User.objects.filter(email=email).exists():
                messages.warning(request, "An account already exists with this Email ID.")
            else:
                try:
                    user = User.objects.create_user(username=username, email=email, password=password)
                    user.save()

                    # Create profile
                    profile = Profile(user=user, email=email, name=name, age=age, dob=dob, gender=gender, image=image)
                    profile.save()

                    # CSV file path
                    csv_file_path = 'user_data.csv'
                    # Check if the file exists already
                    file_exists = os.path.isfile(csv_file_path)

                    # Save user data to CSV file
                    with open(csv_file_path, mode='a', newline='') as file:
                        fieldnames = ['Username', 'Email', 'Name', 'Age', 'Date of Birth', 'Gender']
                        writer = csv.DictWriter(file, fieldnames=fieldnames)

                        # Write header only if the file did not exist prior to this opening
                        if not file_exists:
                            writer.writeheader()

                        writer.writerow({
                            'Username': username,
                            'Email': email,
                            'Name': name,
                            'Age': age,
                            'Date of Birth': dob,
                            'Gender': gender
                        })

                    messages.success(request, "Account created successfully. You can now login.")
                    return redirect('/login')
                except Exception as e:
                    messages.error(request, f"Registration failed: {str(e)}")
        else:
            messages.error(request, "Please correct the errors in the form.")
    else:
        form = RegistrationForm()

    if not request.user.is_anonymous:
        return redirect('/mainpage')
    else:
        return render(request, 'streamapp/register.html', {'form': form})

    
def signout(request):
    logout(request)
    return redirect("/")
    

def mainpage(request):
    if request.user.is_anonymous:
        return redirect('/login')
    else:
        return render(request, 'streamapp/mainpage.html', {'course':course.objects.all(), 'teachers':teachers.objects.all(),'subjects':course_details.objects.all()})


def coursess(request):
    if request.user.is_anonymous:
        return redirect('/login')
    else:
        if(request.GET.get('sub')):
            subject=request.GET.get('sub')
            data_subject=course_details.objects.get(code=subject)
            data_modules=modules.objects.filter(code=subject)
        return render(request, 'streamapp/subject.html', {'subject':data_subject, 'modules': data_modules , 'subjects':course_details.objects.all()})


def about(request):
    if request.user.is_anonymous:
        return redirect('/login')
    else:
        return render(request, 'streamapp/about.html',{'subjects':course_details.objects.all()})

def courses(request):
    if request.user.is_anonymous:
        return redirect('/login')
    else:
        return render(request, 'streamapp/course.html',{'subjects':course_details.objects.all(), 'course_details':course_details.objects.all()})

def contact(request):
    if request.user.is_anonymous:
        return redirect('/login')
    else:
        return render(request, 'streamapp/contact.html',{'subjects':course_details.objects.all()})

def choose_sub(request):
    if request.user.is_anonymous:
        return redirect('/login')
    else:
        return render(request, 'streamapp/choose_sub.html',{'course_details':course_details.objects.all(), 'subjects':course_details.objects.all()})


def profile(request):
    if request.user.is_anonymous:
        return redirect('/login')
    else:
        return render(request, 'streamapp/profile.html',{'course_details':course_details.objects.all(), 'subjects':course_details.objects.all()})

def level(request):
    if request.user.is_anonymous:
        return redirect('/login')
    else:
        subject=request.GET.get('sub')
        t=request.GET.get('type')
        return render(request, 'streamapp/level.html',{'type':t, 'subject':subject})





# main exam page
def exampage(request):
    if request.user.is_anonymous:
        return redirect('/login')
    else:
        if(request.GET.get('sub') and request.GET.get('type')):
            subject=request.GET.get('sub')
            t=request.GET.get('type')
        return render(request, 'streamapp/exam-page.html',{'question':mcq.objects.filter(code=subject,examtype='mock')})



# instruction page
def test(request):
    if request.user.is_anonymous:
        return redirect('/login')
    else:
        if(request.GET.get('sub') and request.GET.get('type')):
            subject=request.GET.get('sub')
            t=request.GET.get('type')
        return render(request, 'streamapp/test.html', {'subject':subject, 'type': t})




def startmock(request):
    if request.user.is_anonymous:
        return redirect('/login')
    else:
        if(request.GET.get('sub')):
            subject=request.GET.get('sub')
            t=request.GET.get('type')
            diffucalty=request.GET.get('diffucalty')
        return render(request, 'streamapp/js_mcq.html',{'question':mcq.objects.filter(code=subject,examtype=t,diffucalty=diffucalty)})
    










# def js_mcq(request):
#     return render(request, 'streamapp/js_mcq.html')

def gen(camera):
    while True:
        frame = camera.face_cheating_detection()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')

def video_feed(request):
    return StreamingHttpResponse(gen(video_camera), content_type='multipart/x-mixed-replace; boundary=frame')
