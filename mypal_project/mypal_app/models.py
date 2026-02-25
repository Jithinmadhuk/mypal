from django.db import models

#SignUp table

class SignUp(models.Model):
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=30)

#home-Page table

class HomePage(models.Model):
    user = models.CharField(max_length=30)
    pal = models.CharField(max_length=30)
    streak = models.IntegerField(default=0)
    last_study_date = models.DateField(null=True, blank=True)
    xp= models.IntegerField(default=0)
    
#Task table    

class Task(models.Model):
    priority = [
        ("High","High"),
        ("Medium","Medium"), 
        ("Low","Low")
    ]
    is_done = [
        ("Completed","Completed"),
        ("Pending","Pending")
    ]
    user = models.ForeignKey(HomePage, on_delete=models.CASCADE)
    task_id=models.AutoField(primary_key=True)
    title = models.CharField(max_length=100)
    priority = models.CharField(max_length=10, choices=priority)
    description = models.TextField(max_length=500)
    is_done=models.CharField(max_length=20, choices=is_done, default="Pending")
    
#Deck

class Deck(models.Model):
    user = models.ForeignKey(HomePage, on_delete=models.CASCADE)
    subject = models.CharField(max_length=30)
    chapter = models.CharField(max_length=30)
    
#Flashcard table

class Flashcard(models.Model):
    deck = models.ForeignKey(Deck, on_delete=models.CASCADE)
    question = models.TextField()
    answer = models.TextField()

#Timer table

class Timer(models.Model):
    user = models.ForeignKey(HomePage, on_delete=models.CASCADE)
    date = models.DateField()
    minutes = models.TimeField()
    sessions = models.IntegerField(default=0)

#Calender table

class Calender(models.Model):
    type = [
        ("Event","Event"),
        ("Class","Class"),
        ("Exam","Exam"),
        ("Assignment Due","Assignment Due")
    ]
    user = models.ForeignKey(HomePage, on_delete=models.CASCADE)
    title = models.CharField(max_length=30)
    type =  models.CharField(choices=type, max_length=20)
    date = models.DateField()
    time = models.TimeField()  