from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, render, redirect
# from .models import related models
from .restapis import *
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from datetime import datetime
import logging
import json

# Get an instance of a logger
logger = logging.getLogger(__name__)


# Create your views here.
def base_view(request):
    return render(request, 'base.html')


# Create an `about` view to render a static about page
def about(request):
    return render(request, 'djangoapp/about.html')


# Create a `contact` view to return a static contact page
def contact(request):
    return render(request, 'djangoapp/contact.html')


# Create a `login_request` view to handle sign in request
def login_request(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('djangoapp:index')
        else:
            # Handle invalid login credentials
            return render(request, 'djangoapp/index.html', {'error': 'Invalid username or password'})
    else:
        return redirect('djangoapp:index')


# Create a `logout_request` view to handle sign out request
def logout_request(request):
    logout(request)
    return redirect('djangoapp:index')


# Create a `registration_request` view to handle sign up request
def registration_request(request):
    context = {}
    # If GET request, render the registration page
    if request.method == 'GET':
        return render(request, 'djangoapp/registration.html', context)
    # If POST request
    elif request.method == 'POST':
        # Get user information from request.POST
        username = request.POST['username']
        password = request.POST['password']
        first_name = request.POST['firstname']
        last_name = request.POST['lastname']
        user_exist = False
        try:
            # Check if user already exists
            User.objects.get(username=username)
            user_exist = True
        except:
            # If not, simply log this is a new user
            logger.debug("{} is new user".format(username))
        # If it is a new user
        if not user_exist:
            # Create user in auth_user table
            user = User.objects.create_user(username=username, first_name=first_name, last_name=last_name,
                                            password=password)
            # Login the user and redirect to course list page
            login(request, user)
            return redirect('djangoapp:index')
        else:
            return render(request, 'djangoapp/index.html', context)



# Update the `get_dealerships` view to render the index page with a list of dealerships
# def get_dealerships(request):
#     context = {}
#     if request.method == "GET":
#         return render(request, 'djangoapp/index.html', context)

def get_dealerships(request):
    if request.method == "GET":
        context = {}

        url = "https://us-south.functions.appdomain.cloud/api/v1/web/22113336-9c90-43fa-9d87-eed5f287930e/dealership-package/get-dealership"
        # Get dealers from the URL

        dealerships = get_dealers_from_cf(url)

        context = {"dealership_list" : dealerships}
        # Concat all dealer's short name
        dealer_names = ' '.join([dealer.short_name for dealer in dealerships])
        # Return a list of dealer short name
        return render(request, 'djangoapp/index.html', context)


# Create a `get_dealer_details` view to render the reviews of a dealer
def get_dealer_details(request, dealer_id):
    if request.method == "GET" and dealer_id:

        url = "https://us-south.functions.appdomain.cloud/api/v1/web/22113336-9c90-43fa-9d87-eed5f287930e/dealership-package/get-review?id="+str(dealer_id)
        # Get dealers from the URL

        review = get_dealer_reviews_from_cf(url, dealer_id)

        # Concat all dealer's review???
        # dealer_names = ' '.join([dealer.short_name for dealer in dealerships])
        # Return a list of dealer review
        return HttpResponse(review)


# Create a `add_review` view to submit a review
def add_review(request, dealer_id):
    pass

    review["time"] = datetime.utcnow().isoformat()
    review["dealership"] = 11
    review["review"] = "This is a great car dealer"
    post_request(url, json_payload, dealerId=dealer_id)