from django.db import models
import bcrypt
import re


# Create your models here.
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

class UserManager(models.Manager):
    def basic_validator(self, postData, isNew):
        errors = {}

        #if it's a registration
        if isNew == True:

            #check if any fields are blank
            if len(postData['first_name']) < 2:
                errors["first_name_blank"] = "First must be at least 2 characters."
            if len(postData['last_name']) < 2:
                errors["last_name_blank"] = "Last must be at least 2 characters."
            if len(postData['email']) < 1:
                errors["email_blank"] = "Email cannot be blank."
            if len(postData['password']) < 1:
                errors["pw_blank"] = "Password cannot be blank."
            if not re.search('\d.*[A-Z]|[A-Z].*\d', postData['password']):
                errors['pw_format'] = "Password must contain at least 1 uppercase letter and 1 number."

            #check if email is valid address
            elif not EMAIL_REGEX.match(postData['email']):
                errors["format_invalid"] = "Please enter a valid email address."


        #check if email already in the database/if is a new user.
            user = User.objects.filter(email = postData['email'])
            if len(user):
                errors['exists'] = "User account already exists."
            if postData["password"] != postData["password2"]:
                errors['mismatch_pw'] = "Passwords must match."

        if isNew == False:
            if not EMAIL_REGEX.match(postData['email']):
                errors["format_invalid"] = "Please enter a valid email address."
            
            user = User.objects.filter(email=postData["email"])
            if len(user) == 0:
                errors["no_user"] = "Log in failed."

            user = User.objects.get(email=postData['email'])
            encoded_pw = user.password.encode()

            #if email in the database, check if passwords match, decrypting password first.
            if user:
                print("password = ", postData["password"])

                if bcrypt.hashpw(postData["password"].encode(), user.password.encode()) != encoded_pw:
                    errors["password_fail"] = "Incorrect password"


        return errors

# Create your models here.
class User(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = UserManager()

    def __repr__(self):
        return "<User object: {} {} {} {}>".format(self.first_name, self.last_name, self.email, self.password)
