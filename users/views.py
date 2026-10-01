def udashboard(request):
    return render(request, 'udashboard.html')


def prediction(request):
    return render(request, 'prediction.html')


from django.shortcuts import render, redirect
from django.contrib import messages
from .models import User  # Assuming this is a custom user model; change if using Django's built-in User
from django.core.files.storage import FileSystemStorage


def register(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        mobile = request.POST.get('mobile')
        email = request.POST.get('email')
        password = request.POST.get('password') 
        age = request.POST.get('age')
        address = request.POST.get('address')

        profile_picture = request.FILES.get('profile_picture')  # Handle file upload

        if User.objects.filter(email=email).exists():
            messages.error(request, 'Email already registered')
            return redirect('userregister')

        user = User(name=name, mobile=mobile, email=email, password=password, age=age, address=address)

        if profile_picture:
            fs = FileSystemStorage()
            filename = fs.save(profile_picture.name, profile_picture)
            user.profile_picture = filename

        user.save()

        messages.success(request, 'Registration successful! Please login.')
        return redirect('userlogin')

    return render(request, 'register.html')



def userlogin(request):
    if request.method == 'POST':
        email = request.POST.get('email')  # Get the username or email
        password = request.POST.get('password')  # Get the password

        # Check if the user exists and the password is correct
        try:
            user = User.objects.get(email=email)
            if user.password == password:  # Be cautious about plain text password comparison
                # Log the user in (you may want to set a session or token here)
                request.session['user_id'] = user.id  # Store user ID in session
                messages.success(request, 'Login successful!')
                return redirect('udashboard')  # Redirect to the index page or desired page
            else:
                messages.error(request, 'Invalid email or password. Please try again.')
        except User.DoesNotExist:
            messages.error(request, 'Invalid email or password. Please try again.')

    return render(request, 'userlogin.html')
def profile(req):
    user_id = req.session.get("user_id")  # Use 'get' to avoid a crash if session is not set
    user = User.objects.get(id=user_id)  # Fetch the user by their id
    
    if req.method == 'POST':
        user_name = req.POST.get('userName')
        user_age = req.POST.get('userAge')
        user_phone = req.POST.get('userPhNum')
        user_email = req.POST.get('userEmail')
        user_address = req.POST.get("userAddress")

        # Update user details
        user.name = user_name
        user.age = user_age
        user.address = user_address
        user.mobile = user_phone
        user.email = user_email

        # Handle profile picture update
        if len(req.FILES) != 0:
            image = req.FILES['profilepic']
            user.profile_picture = image  # Save the new profile image

        user.save()  # Save the user details after updating all fields
        messages.success(req, 'Profile updated successfully!')

    context = {"i": user}  # 'i' contains user details to be used in the template
    return render(req, 'profile.html', context)

# # Create your views here.import os  # Make sure this is at the top
# import os
# import numpy as np
# from django.shortcuts import render
# from django.core.files.storage import FileSystemStorage
# from tensorflow.keras.models import load_model
# from tensorflow.keras.preprocessing import image

# # Load the model at the start
# MODEL_PATH = 'D:/radio_therophy/radiotherapy/radiotherapy_model.h5'

# # Attempt to load the model and handle any errors
# try:
#     print(f"Loading model from: {MODEL_PATH}")
#     model = load_model(MODEL_PATH)  # Load the model
#     print("Model loaded successfully.")
# except Exception as e:
#     print(f"Error loading model: {e}")
#     model = None  # Set model to None if loading fails

# def predict_radiotherapy(request):
#     prediction = None  # Initialize prediction variable
    
#     # Check if a POST request has been made and an image has been uploaded
#     if request.method == 'POST' and request.FILES.get('image'):
#         uploaded_file = request.FILES['image']
        
#         try:
#             # Save the uploaded image temporarily
#             fs = FileSystemStorage()
#             file_path = fs.save(uploaded_file.name, uploaded_file)
#             img_path = fs.url(file_path)
#             print(f"Image uploaded to: {file_path}")
            
#             # Preprocess the image for prediction
#             img = image.load_img(os.path.join(fs.location, file_path), target_size=(150, 150))  # Adjust size to (150, 150)
#             img_array = image.img_to_array(img)
#             img_array = np.expand_dims(img_array, axis=0)  # Add batch dimension
#             img_array /= 255.0  # Normalize pixel values
#             print(f"Image preprocessed successfully. Image shape: {img_array.shape}")

#             # Check if the model is loaded before making predictions
#             if model is not None:
#                 print("Model is loaded, starting prediction...")

#                 # Confirm model input shape
#                 print(f"Model input shape: {model.input_shape}")
#                 print(f"Image array shape: {img_array.shape}")

#                 # Predict using the CNN model
#                 prediction_probabilities = model.predict(img_array)
#                 predicted_class = np.argmax(prediction_probabilities[0])
#                 print(f"Prediction probabilities: {prediction_probabilities}, Predicted class: {predicted_class}")

#                 # Define output classes based on predicted class
#                 if predicted_class == 0:
#                     prediction = "Radiotherapy is necessary"
#                 else:
#                     prediction = "Radiotherapy is not necessary"

#                 print(f"Prediction result: {prediction}")

#             else:
#                 print("Model not loaded!")
#                 prediction = "Model not loaded. Please try again later."
#                 return render(request, 'prediction.html', {'prediction': prediction})

#             # Optionally delete the uploaded image after prediction
#             fs.delete(file_path)
#             return render(request, 'prediction.html', {'prediction': prediction})

#         except Exception as e:
#             print(f"Error processing image or making prediction: {e}")
#             prediction = f"Error occurred while processing the image: {e}"
#             return render(request, 'prediction.html', {'prediction': prediction})

#     # Render the prediction result (whether success or failure)
#     return render(request, 'prediction.html', {'prediction': prediction})

import os
import numpy as np
from django.shortcuts import render
from django.core.files.storage import FileSystemStorage
import tensorflow as tf
from tensorflow.keras.preprocessing.image import load_img, img_to_array

# ===============================
# Load Model Once (Fast & Safe)
# ===============================

MODEL_PATH = "cancer_radiotherapy_model.keras"

try:
    model = tf.keras.models.load_model(MODEL_PATH)
    print("✅ Model loaded successfully")
except Exception as e:
    print(f"❌ Model loading failed: {e}")
    model = None

# ===============================
# Class Mapping
# ===============================

CLASS_NAMES = {
    0: "Glioma (Cancer)",
    1: "Meningioma (Cancer)",
    2: "No Tumor (No Cancer)",
    3: "Pituitary (Cancer)"
}

IMG_SIZE = 224

# ===============================
# Django View
# ===============================

def predict_radiotherapy(request):
    result = None

    if request.method == "POST" and request.FILES.get("image"):

        uploaded_file = request.FILES["image"]
        fs = FileSystemStorage()

        file_name = fs.save(uploaded_file.name, uploaded_file)
        file_path = os.path.join(fs.location, file_name)

        try:
            # ------------------------
            # Preprocess Image
            # ------------------------

            img = load_img(file_path, target_size=(IMG_SIZE, IMG_SIZE))
            img_array = img_to_array(img) / 255.0
            img_array = np.expand_dims(img_array, axis=0)

            # ------------------------
            # Predict
            # ------------------------

            if model is None:
                return render(request, "prediction.html", {
                    "prediction": "❌ Model not loaded"
                })

            predictions = model.predict(img_array)
            predicted_class = int(np.argmax(predictions))
            confidence = round(float(np.max(predictions)) * 100, 2)

            diagnosis = CLASS_NAMES[predicted_class]

            # ------------------------
            # Radiotherapy Logic
            # ------------------------

            if predicted_class == 2:
                radiotherapy = "❌ Radiotherapy Not Required"
            else:
                radiotherapy = "✅ Radiotherapy Required"

            result = {
                "diagnosis": diagnosis,
                "radiotherapy": radiotherapy,
                "confidence": confidence
            }
            print(f"✅ Prediction: {result}")

        except Exception as e:
            result = {"error": str(e)}
            print(f"Error during prediction: {e}")

        # Cleanup uploaded image
        fs.delete(file_name)

        return render(request, "prediction.html", {"result": result})

    return render(request, "prediction.html")
