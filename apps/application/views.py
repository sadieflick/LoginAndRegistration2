from django.shortcuts import render, HttpResponse, redirect
from django.contrib import messages
from .models import *
import bcrypt


def index(request):

    return render(request, "application/index.html")

def success(request):

    if "first_name" not in request.session:
        messages.error(request, "You must be logged in to enter site.")
        return redirect('/')

    return render(request, "application/success.html")


def submit(request):
    if request.method == "POST":

        print("entering the submit function")
        print(request.POST)
        print (id)

        #save post info so the user doesn't have to re-type it if they have an error
        request.session["first_name"] = request.POST["first_name"]
        request.session["lastname"] = request.POST["last_name"]
        request.session["email"] = request.POST["email"]

        #get validation manager
        errors = User.objects.basic_validator(request.POST, True)
        #if there are any errors
        if len(errors):
            print("entering errors list")
            # if the errors object contains anything, loop through each key-value pair and make a flash message
            for key, value in errors.items():
                messages.error(request, value)
            # redirect the user back to the form to fix the errors
            return redirect('/')

        #use bcrypt to hash password
        hash1 = bcrypt.hashpw(request.POST['password'].encode(), bcrypt.gensalt())

        # update from form first_name, last_name, email in db, save id in a variable
        #create user
        new_user = User.objects.create(email =request.POST["email"], first_name =request.POST["first_name"], last_name =request.POST["last_name"], password=hash1)
        new_user.save()

        messages.success(request, "Successfully registered!")

        return redirect('/success')

def login(request):

    if request.method == "POST":
        
        errors = User.objects.basic_validator(request.POST, False)
        #if there are any errors
        if len(errors):
            # if the errors object contains anything, loop through each key-value pair and make a flash message
            for key, value in errors.items():
                messages.error(request,value)
            # redirect the user back to the form to fix the errors
            return redirect('/')

        else:
            user = User.objects.get(email = request.POST["email"])
            messages.success(request, "Successfully logged in!")
            request.session["id"] = user.id
            request.session["first_name"] = user.first_name
            return redirect('/success')
        

        return redirect('/success')

def logout(request):
    request.session.clear()
    return redirect('/')
    
