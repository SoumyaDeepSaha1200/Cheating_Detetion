from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class course(models.Model):
    name=models.CharField(max_length=122)
    location=models.TextField()
    desc=models.TextField()

    def __str__(self):
        return self.name

class teachers(models.Model):
    name=models.CharField(max_length=122)
    location=models.TextField()
    desc=models.TextField()
    def __str__(self):
        return f"Name- {self.name}"

    

class modules(models.Model):
    code=models.CharField(max_length=50)
    mod_no=models.DecimalField(max_digits=2,decimal_places=0)
    name=models.CharField(max_length=122)
    desc=models.TextField()
    data=models.TextField()
    def __str__(self):
        return f"Code-{self.code} Module-{self.mod_no}"
    


class mcq(models.Model):
    code=models.CharField(max_length=50)
    examtype=models.CharField(max_length=4)
    question=models.TextField()
    option1=models.TextField()
    option2=models.TextField()
    option3=models.TextField()
    option4=models.TextField()
    answer=models.TextField()
    diffucalty=models.DecimalField(max_digits=1,decimal_places=0,default=0)
    def __str__(self):
        return f"Code-{self.code}"
    


class course_details(models.Model):
    code=models.CharField(max_length=50)
    sub_name=models.CharField(max_length=80)
    amt=models.IntegerField()
    location=models.TextField()
    duration=models.TextField()
    def __str__(self):
        return self.sub_name



class reply(models.Model):
    name=models.CharField(max_length=100)
    reply=models.CharField(max_length=15000)
    def __str__(self):
        return self.name




class AttendanceRecord(models.Model):
    name = models.CharField(max_length=100)
    head_movement = models.CharField(max_length=100)
    left_eye = models.CharField(max_length=100)
    right_eye = models.CharField(max_length=100)
    head_position = models.CharField(max_length=100)
    date = models.DateField()
    time = models.TimeField()
    cheating_incident = models.CharField(max_length=100, blank=True, null=True)
    image_path= models.ImageField(upload_to='cheating_images/' ,default="")
    sound_detection = models.CharField(max_length=10, default="")  
    background_noise_level=models.CharField(max_length=20,default="")
    def __str__(self):
        return self.name
    




class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    age = models.IntegerField()
    dob = models.DateField()
    gender = models.CharField(max_length=10)
    image = models.ImageField(upload_to='profile_images/', null=True, blank=True)
    email = models.EmailField(default="")  # Make sure this field exists if you want to include email in Profile
    subject_code = models.CharField(max_length=100, default="")
    levelOfExam = models.CharField(max_length=100, default="")
    marks = models.CharField(max_length=100, default="")
    def __str__(self):
        return self.name
    


