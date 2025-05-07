from flask import Flask, render_template, request, redirect, url_for, session, flash
import os
from scripts.detect_ingredients import predict_ingredient
from werkzeug.utils import secure_filename
from auth import login_user, signup_user
import tensorflow as tf

app = Flask(__name__)
app.secret_key = 'supersecretkey'

# Model Preloading - Load model globally to avoid loading it on each request
MODEL_PATH = "C:/NITHU STUDIES/mealmatch/ingredient-finder/models/ingredient_recognition_model.h5"
model = tf.keras.models.load_model(MODEL_PATH)

# Directory paths
UPLOAD_FOLDER = 'static/uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Class Labels (Ensure your training directory is correct)
train_dir = r"C:\\NITHU STUDIES\\mealmatch\\ingredient-finder\\data\\train"
class_labels = sorted(os.listdir(train_dir))

@app.route('/')
def index():
    return render_template('login.html')  # Main page showing ingredient finder and other options

@app.route('/predict', methods=['POST'])
def predict():
    # Ensure the user is logged in before allowing access to this route
    if 'username' not in session:
        flash("You must be logged in to access this page.")
        return redirect(url_for('login'))  # Redirect to login if not logged in

    if 'image' not in request.files:
        flash("No image uploaded.")
        return redirect(request.url)  # Redirect back if no image is uploaded
    
    file = request.files['image']
    
    # If no file is selected
    if file.filename == '':
        flash("No file selected.")
        return redirect(request.url)  # Redirect back if no file is selected
    
    if file:
        try:
            # Securely save the file with a safe filename
            filename = secure_filename(file.filename)
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(filepath)

            # Call the ingredient prediction function
            prediction = predict_ingredient(filepath, model, class_labels)  # Pass model and class labels

            # Return the result and the image path to the template
            return render_template('ingredient_finder.html', prediction=prediction, image_path=filepath)
        
        except Exception as e:
            print(f"Error during prediction: {e}")
            flash("Error processing the image. Please try again.")
            return redirect(request.url)  # Redirect back on error

    flash("Invalid image file.")
    return redirect(request.url)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        success, result = login_user(email, password)
        if success:
            session['username'] = result  # Store username in session
            return redirect(url_for('dashboard'))
        else:
            # If login fails, inform the user that they don't have an account
            if result == "Invalid credentials" or result == "User not found":
                return render_template('login.html', error="You don't have an account. Please sign up first.")
            return render_template('login.html', error=result)
    return render_template('login.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['name']
        email = request.form['email']
        password = request.form['password']
        success, message = signup_user(username, email, password)
        if success:
            return redirect(url_for('login'))
        return render_template('signup.html', error=message)
    return render_template('signup.html')

@app.route('/dashboard')
def dashboard():
    # Protect this route by ensuring the user is logged in
    if 'username' not in session:
        return redirect(url_for('login'))  # Redirect to login if not logged in
    return render_template('dashboard.html', username=session['username'])

@app.route('/logout')
def logout():
    session.pop('username', None)  # Remove the username from session (log the user out)
    return redirect(url_for('login'))

@app.route('/ingredient-finder', methods=['GET', 'POST'])
def ingredient_finder():
    # Ensure the user is logged in before allowing access to this route
    if 'username' not in session:
        return redirect(url_for('login'))  # Redirect to login if not logged in

    if request.method == 'POST':
        if 'image' not in request.files:
            flash("No image uploaded.")
            return redirect(request.url)
        
        file = request.files['image']
        
        # If no file is selected
        if file.filename == '':
            flash("No file selected.")
            return redirect(request.url)
        
        if file:
            try:
                # Securely save the file with a safe filename
                filename = secure_filename(file.filename)
                filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                file.save(filepath)

                # Call the ingredient prediction function
                prediction = predict_ingredient(filepath, model, class_labels)  # Pass model and class labels

                # Return the result and the image path to the template
                return render_template('ingredient_finder.html', prediction=prediction, image_path=filepath)

            except Exception as e:
                print(f"Error during prediction: {e}")
                flash("Error processing the image. Please try again.")
                return redirect(request.url)

    return render_template('ingredient_finder.html')  # Render the page if it's GET or no image uploaded

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/chatbot')
def chatbot():
    return render_template('chatbot.html')  # Assuming your chatbot HTML is named chatbot.html


@app.route('/submit-feedback', methods=['POST'])
def submit_feedback():
    name = request.form['name']
    feedback = request.form['feedback']

    # Save feedback to a file (you can change to database later)
    with open('feedback.txt', 'a') as f:
        f.write(f"{name}: {feedback}\n")

    flash('Thank you for your feedback!')
    return redirect('/feedback')

@app.route('/feedback', methods=['GET', 'POST'])
def feedback():
    if request.method == 'POST':
        # You can process/store feedback here if needed
        flash('Thank you for your feedback!', 'success')
        return redirect(url_for('feedback'))
    return render_template('feedback.html')

@app.route('/recipes')
def recipes():
    return render_template('recipes.html')  # Recipe page route

# Helper function to predict the ingredient (from scripts/detect_ingredients.py)
def predict_ingredient(img_path, model, class_labels):
    from tensorflow.keras.preprocessing import image
    import numpy as np

    try:
        img = image.load_img(img_path, target_size=(150, 150))
        img_array = image.img_to_array(img) / 255.0
        img_array = np.expand_dims(img_array, axis=0)

        predictions = model.predict(img_array)
        predicted_class = class_labels[np.argmax(predictions)]

        return predicted_class
    except Exception as e:
        print(f"Error in prediction: {e}")
        return "Error during prediction"

if __name__ == '__main__':
    app.run(debug=True)
