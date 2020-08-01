import os
import pandas as pd

from django.conf import settings
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, logout
from django.core.files.storage import FileSystemStorage
from yolo_app.models import UserHistory
from yolo_app.Inference.Detector import main_detector

# variables used for getting the path of the media
current_path = os.getcwd()
path_for_image = settings.MEDIA_ROOT
# mapping dictionary used to map result of the yolo model into the string
reference_dict = {'0' : 'Corona Positive', '1' : 'Corona Negative'}

# Create your views here.
# this is the home view which contains the below logic
# logic 1: if user is not signed in sign up link is added here
# logic 2: if user is sign up he can sign in using the link added here
def index(request):
	return render(request, 'index.html')

# This view will enable users to sign up and save the result in auth
# user table
def signup_view(request):
	if request.method == 'POST':
		form = UserCreationForm(request.POST)
		if form.is_valid():
			form.save(																																																		)
			return redirect('index')
	else:
		form = UserCreationForm()	
		
	return render(request, 'signup.html', {'form': form})

# this is login view
def login_view(request):
	if request.method == 'POST':
		form = AuthenticationForm(data=request.POST)
		if form.is_valid():
			user = form.get_user()
			login(request, user)
			return redirect('yolo_app')
	else:
	    form = AuthenticationForm()
	
	return render(request, 'login.html', {'form': form})

# ===============main code and is applicable for those user who have logined in=====================
def yolo_detection_App(request):
	if request.method == 'POST':
		name_of_file = request.FILES['myfile']
		fs = FileSystemStorage()
		# save the file in the specific folder
		saved_file = fs.save(name_of_file.name, name_of_file)
		csv_file_returned = main_detector(saved_file)
		data = pd.read_csv(csv_file_returned)
		data_dict = data.to_dict()
		label = data_dict['label']
		value = list(label.values())
		value_to_string = str(value[0])
		label_predicted = reference_dict[value_to_string]
		UserHistory.objects.create(
			                   user = request.user,
					   uploaded_img_path = os.path.join(path_for_image, saved_file),
					   result = label_predicted
					  )
			
		return render(request, 'result.html', {'context': data_dict})

	return render(request, 'upload_file.html')

# Getting user details from the database based on user table
def user_details(request):
	history = UserHistory.objects.filter(
                                        user=request.user.pk
	                                    )
	return render(request, 'history.html', { 'user_history': history })

# logout page and is applicable for those users who have login successfully
def logout_user(request):
	logout(request)
	return redirect('index')
