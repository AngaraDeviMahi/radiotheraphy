from django.shortcuts import render, redirect

def index(request):
    return render(request, 'index.html')

def about(req):
    return render(req, 'about.html')

def adminlogin(req):
    return render(req, 'adminlogin.html')

def contact(req):
    return render(req, 'contact.html')

def feature(req):
    return render(req, 'feature.html')

def service(req):
    return render(req, 'service.html')

def register(req):
    return render(req, 'register.html')

def userlogin(req):
    return render(req, 'userlogin.html')

def dashboard(request):
    return render(request, 'admins/dashboard.html')

def upload(request):
    return render(request, 'admins/upload.html')







import os
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report
from django.shortcuts import render
from tensorflow.keras.preprocessing.image import ImageDataGenerator



import os
import tensorflow as tf
from tensorflow.keras import layers, models
from tensorflow.keras.optimizers import Adam
from django.shortcuts import render
import numpy as np

def build_cnn_model(input_shape):
    model = models.Sequential()
    model.add(layers.Conv2D(32, (3, 3), activation='relu', padding='same', input_shape=input_shape))
    model.add(layers.BatchNormalization())
    model.add(layers.MaxPooling2D((2, 2)))
    model.add(layers.Conv2D(64, (3, 3), activation='relu', padding='same'))
    model.add(layers.BatchNormalization())
    model.add(layers.MaxPooling2D((2, 2)))
    model.add(layers.Conv2D(128, (3, 3), activation='relu', padding='same'))
    model.add(layers.BatchNormalization())
    model.add(layers.MaxPooling2D((2, 2)))
    model.add(layers.Flatten())
    model.add(layers.Dense(128, activation='relu'))
    model.add(layers.Dense(1, activation='sigmoid'))  # For binary classification
    model.compile(optimizer=Adam(learning_rate=0.001), loss='binary_crossentropy', metrics=['accuracy'])
    return model

def cnn(request):
    if request.method == 'POST':
        dataset_path = 'D:/radio_therophy/radiotherapy/dataset'  # Update this path

        if not os.path.exists(dataset_path):
            return render(request, 'admins/cnn.html', {'error': 'Dataset path does not exist.'})

        image_size = (150, 150)
        batch_size = 32

        train_datagen = tf.keras.preprocessing.image.ImageDataGenerator(rescale=1./255, validation_split=0.2)
        train_generator = train_datagen.flow_from_directory(
            dataset_path,
            target_size=image_size,
            batch_size=batch_size,
            class_mode='binary',
            subset='training'
        )
        validation_generator = train_datagen.flow_from_directory(
            dataset_path,
            target_size=image_size,
            batch_size=batch_size,
            class_mode='binary',
            subset='validation'
        )

        input_shape = (150, 150, 3)
        model = build_cnn_model(input_shape)

        # Train the model
        history = model.fit(
            train_generator,
            epochs=2,
            validation_data=validation_generator
        )

        # Extract final training metrics (accuracy, loss)
        final_accuracy = history.history['accuracy'][-1]
        final_val_accuracy = history.history['val_accuracy'][-1]
        final_loss = history.history['loss'][-1]
        final_val_loss = history.history['val_loss'][-1]

        context = {
            'final_accuracy': final_accuracy,
            'final_val_accuracy': final_val_accuracy,
            'final_loss': final_loss,
            'final_val_loss': final_val_loss,
        }

        return render(request, 'admins/cnn.html', context)

    return render(request, 'admins/cnn.html')



from django.contrib import messages
from django.core.files.storage import FileSystemStorage

from django.shortcuts import render,redirect
from django.contrib import messages
import urllib.request
import urllib.parse

from django.conf import settings
from django.contrib.auth import authenticate, login

def adminlogin(req):
    if req.method == 'POST':
        username = req.POST.get('username')
        password = req.POST.get('password')
        print("hello")
        print(username,password)
        # Check if the provided credentials match
        if username == 'admin' and password   == 'admin':
            messages.success(req, 'You are logged in.')
            return redirect('dashboard')  # Redirect to the admin dashboard page
        else:
             messages.error(req, 'You are trying to log in with wrong details.')
             return redirect('dashboard')  # Redirect to the login page (named 'admin' here)

    # Render the login page if the request method is GET
    return render(req, 'adminlogin.html')

def adminlogout(req):
    messages.info(req,'You are logged out...!')
    return redirect('adminlogin')

