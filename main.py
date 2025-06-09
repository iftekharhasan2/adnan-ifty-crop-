from flask import Flask, request, jsonify, render_template
import numpy as np
import io
from PIL import Image
from tensorflow import keras
import pandas as pd
import requests
from flask_pymongo import PyMongo
import bcrypt
import jwt
import datetime
from flask_cors import CORS 
from datetime import date
from functools import wraps



app = Flask(__name__)
CORS(app)

app.config['MONGO_URI'] = 'mongodb+srv://ifty:nxzhhhlWutt7PcMh@cluster0.bd9ywas.mongodb.net/mydatabase?retryWrites=true&w=majority&appName=Cluster0'
app.config['SECRET_KEY'] = 'your_secret_key'

mongo = PyMongo(app)







def get_weather_data(city):
    api_key = "1bd0be556664fb2dcaa474e56927746d"
    base_url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"
    response = requests.get(base_url)
    if response.status_code == 200:
        return response.json()
    return None

def day01():
    a1 = "সূর্যের আলোয় ৪ ঘণ্টা বীজ শুকিয়ে নিন।"
    a2 = "সকাল"
    a3 = "৭টা – ১২টা"
    b1 = "স্বাভাবিক তাপমাত্রায় বীজকে ঠান্ডা করে নিন।"
    b2 = "দুপুর"
    b3 = "১২টা – ৪টা"
    c1 = "পানিতে ৬ ঘণ্টা ভিজিয়ে রাখুন।"
    c2 = "বিকাল – রাত"
    c3 = "৪টা – ১০টা"
    return a1, a2, a3, b1, b2, b3, c1, c2, c3

def day02():
    a1 = "প্রতি কেজি বীজের সাথে ১০ গ্রাম ট্রাইকোডার্মা মিশিয়ে নিন।"
    a2 = "সকাল"
    a3 = "৬টা – ৭টা"
    b1 = "বীজকে শুকিয়ে নিন (সরাসরি সূর্যের তাপ দেয়া যাবেনা)"
    b2 = "সকাল"
    b3 = "৭টা – ১০টা"
    c1 = "বীজকে ২গ্রাম/লিটার জিবেরেলিক এসিড (GA3 10%) মিশ্রনে ১০ মিনিট ডুবিয়ে রেখে বাতাসে শুকিয়ে নিন।"
    c2 = "সকাল"
    c3 = "১০টা – ১১টা"
    d1 = "একটি হালকা আর্দ্র কাপড়ে বীজ বেঁধে পুত্তলি বানিয়ে ২১ ঘণ্টা শুষ্ক জায়গায় রাখুন।"
    d2 = "সকাল"
    d3 = "১১টা – ৮টা"
    return a1, a2, a3, b1, b2, b3, c1, c2, c3, d1, d2, d3

def day03():
    a1 = "বীজ বপন করুন এবং ছায়াযুক্ত স্থানে রাখুন।"
    a2 = "সকাল"
    a3 = "৬টা – ৮টা"
    b1 = "বীজ বপনের সময় অঙ্কুরোদ্গম না"
    b2 = "সকাল"
    b3 = "৬টা – ৮টা"
    sp_statement01 = (
        "বীজ বপন পদ্ধতিঃ "
        "বীজকে প্রথমে অঙ্কুরোদ্গম করে নিতে হবে। "
        "শীতকালে খুব ঠাণ্ডা থাকলে বীজ ১২ ঘন্টা পানিতে ভিজিয়ে রেখে গোবরের মাদার ভেতরে কিংবা মাটির পাত্রে রক্ষিত বালির ভেতরে রেখে দিলে ২-৩ দিনের মধ্যে বীজ অঙ্কুরিত হয়। "
        "জমি থেকে এক মুষ্ঠি পরিমান মাটি তুলে এক মুষ্ঠি পরিমান ট্রাইকোডার্মা মিশ্রিত জৈব সার মিশিয়ে নিতে হবে। "
        "বীজকে ২ সেমি (আঙ্গুলের ২ করা) গভীরে বপন করতে হবে, জৈব সার মিশ্রিত মাটি আলতো করে দিয়ে দিতে হবে। "
        "চারা গজিয়ে গেলে প্রতিদিন সকালে ঝাঝরি দিয়ে চারার গোড়ার অঞ্চল হালকা করে ভিজিয়ে দিতে হবে (শীতকালে এবং জমি আর্দ্র থাকলে দরকার নেই)।"
    )
    sp_statement02 = (
        "সতর্কীকরণঃ "
        "চারার সুস্থ বৃদ্ধির জন্য শিডিউল স্প্রে জাতীয় পুষ্টি উপাদান স্প্রে করে দিতে হবে। "
        "চারা গজানোর পর জমিতে বেডের উচ্চতার ৩ ভাগের একভাগ পানি দিতে হবে, তবে খেয়াল রাখতে যেন চারার গোড়ায় পানি না জমে থাকে। "
        "বৃষ্টির সময় অথবা শীতকালে জমি আর্দ্র থাকলে সেচের দরকার নেই। "
        "শীতকালে বেড আর্দ্র থাকলে ৩ ভাগের একভাগ পানি দেয়ার দরকার নেই, তবে গ্রীষ্মকালে ১৫ দিন পর পর সেচ দিতে হবে এবং বেডের ৩ ভাগের এক ভাগ পানি নিশ্চিত করতে হবে। "
        "চারার বয়স ১০-১৫ দিন হয়ে গেলে তখন থেকে ঢালাও ভাবে সেচ দিতে হবে, তবে শীতকালে দেয়ার প্রয়োজন নেই।"
    )
    return a1, a2, a3, b1, b2, b3, (sp_statement01, sp_statement02)

def day_seed02():
    a1 = "দমন ব্যবস্থাপনা ---> কল্যাণ ৩ গ্রাম/লিটার + নেয়ামত ০.৫গ্রাম/লিটার"
    a2 = "সকাল"
    a3 = "৭-৮টা"
    b1 = "পরিচর্যা ---> কোন চারা রোগাক্রান্ত হলে তা দ্রুত তুলে ফেলুন। জমিতে রসের অভাব দেখা দিলে সেচ দিন।"
    b2 = "সকাল"
    b3 = "৯-১১টা"
    sp_statement01 = "if u already done it, then u dont have to do anything"
    return a1, a2, a3, b1, b2, b3, (sp_statement01,)

def day_seed05():
    a1 = "দমন ব্যবস্থাপনা ---> ক্রপ মাস্টার ৫ গ্রাম/লিটার + ম্যাট্রিক্সিন ১ মিলি/লিটার"
    a2 = "সকাল"
    a3 = "৭-৮টা"
    b1 = "পরিচর্যা ---> কোন চারা রোগাক্রান্ত হলে তা দ্রুত তুলে ফেলুন। জমিতে রসের অভাব দেখা দিলে সেচ দিন।"
    b2 = "সকাল"
    b3 = "৯-১১টা"
    return a1, a2, a3, b1, b2, b3

def day_seed07():
    a1 = "পরিচর্যা ---> কোন চারা রোগাক্রান্ত হলে তা দ্রুত তুলে ফেলুন। জমিতে রসের অভাব দেখা দিলে সেচ দিন। এর জায়গা হাল্কা ফাকা করে আগাছা তুলে ফেলতে হবে যেন গাছের গোড়ার ক্ষতি না হয়। "
    a2 = "সকাল"
    a3 = "৯-১১টা"
    return a1, a2, a3

def day_seed10():
    a1 = "দমন ব্যবস্থাপনা ---> কল্যান ৩ গ্রাম/লিটার + প্রোফাইটা ১ মিলি/লিটার + ইয়োকা ১ মিলি/লিটার"
    a2 = "সকাল"
    a3 = "৭-৮টা"
    b1 = "পরিচর্যা ---> কোন চারা রোগাক্রান্ত হলে তা দ্রুত তুলে ফেলুন। জমিতে রসের অভাব দেখা দিলে সেচ দিন।"
    b2 = "সকাল"
    b3 = "৯-১১টা"
    return a1, a2, a3, b1, b2, b3

def day_seed12():
    a1 = "পরিচর্যা ---> কোন চারা রোগাক্রান্ত হলে তা দ্রুত তুলে ফেলুন। জমিতে রসের অভাব দেখা দিলে সেচ দিন। চারার গোড়ার আগাছা তোলাঃ চারার গোড়ার এক হাত সমপরিমানে চতুর্দিক থেকে আগাছা তুলে ফেলুন। মালচিং এর জায়গা হাল্কা ফাকা করে আগাছা তুলে ফেলতে হবে যেন গাছের গোড়ার ক্ষতি না হয়। ড্রেনের আগাছা তোলাঃ এক্ষেত্রে ড্রেন থেকে মূলসহ আগাছা উপড়ে ফেলতে হবে।"
    a2 = "সকাল"
    a3 = "৯-১১টা"
    return a1, a2, a3

def day_seed15():
    a1 = "দমন ব্যবস্থাপনা ---> গ্রিন প্লাস ১মিলি/লিটার + চিলেটেট জিঙ্ক ০.৫ গ্রাম/লিটার"
    a2 = "সকাল"
    a3 = "৭-৮টা"
    b1 = "পরিচর্যা ---> কোন চারা রোগাক্রান্ত হলে তা দ্রুত তুলে ফেলুন। জমিতে রসের অভাব দেখা দিলে সেচ দিন"
    b2 = "সকাল"
    b3 = "৯-১১টা"
    return a1, a2, a3, b1, b2, b3

def day_seed17():
    a1 = "উপরি সার প্রয়োগ ----> ১ম কিস্তি উপরি সার প্রয়োগঃ DAP – ২০০ গ্রাম/শতক + TSP – ১৫০গ্রাম/শতক"
    a2 = "সকাল"
    a3 = "৮-৯.৩০টা"
    b1 = "পরিচর্যা ---> কোন চারা রোগাক্রান্ত হলে তা দ্রুত তুলে ফেলুন। জমিতে রসের অভাব দেখা দিলে সেচ দিন"
    b2 = "সকাল"
    b3 = "৯-১১টা"
    return a1, a2, a3, b1, b2, b3

def day_seed19():
    a1 = "পরিচর্যা ---> কোন চারা রোগাক্রান্ত হলে তা দ্রুত তুলে ফেলুন। জমিতে রসের অভাব দেখা দিলে সেচ দিন। চারার গোড়ার আগাছা তোলাঃ চারার গোড়ার এক হাত সমপরিমানে চতুর্দিক থেকে আগাছা তুলে ফেলুন। মালচিং এর জায়গা হাল্কা ফাকা করে আগাছা তুলে ফেলতে হবে যেন গাছের গোড়ার ক্ষতি না হয়। ড্রেনের আগাছা তোলাঃ এক্ষেত্রে ড্রেন থেকে মূলসহ আগাছা উপড়ে ফেলতে হবে।"
    a2 = "সকাল"
    a3 = "৯-১১টা"
    return a1, a2, a3

def day_seed20():
    a1 = "দমন ব্যবস্থাপনা ---> কপাল ২ গ্রাম/লিটার + নেয়ামত ০.৫ গ্রাম/লিটার"
    a2 = "সকাল"
    a3 = "৭-৮টা"
    b1 = "পরিচর্যা ---> কোন চারা রোগাক্রান্ত হলে তা দ্রুত তুলে ফেলুন। জমিতে রসের অভাব দেখা দিলে সেচ দিন"
    b2 = "সকাল"
    b3 = "৯-১১টা"
    return a1, a2, a3, b1, b2, b3

def day_seed25():
    a1 = "দমন ব্যবস্থাপনা ---> গ্রিন প্লাস ১মিলি/লিটার + চিলেটেট জিঙ্ক ০.৫ গ্রাম/লিটার"
    a2 = "সকাল"
    a3 = "৭-৮টা"
    b1 = "পরিচর্যা ---> কোন চারা রোগাক্রান্ত হলে তা দ্রুত তুলে ফেলুন। জমিতে রসের অভাব দেখা দিলে সেচ দিন"
    b2 = "সকাল"
    b3 = "৯-১১টা"
    return a1, a2, a3, b1, b2, b3

def day_seed26():
    a1 = "পরিচর্যা ---> কোন চারা রোগাক্রান্ত হলে তা দ্রুত তুলে ফেলুন। জমিতে রসের অভাব দেখা দিলে সেচ দিন। চারার গোড়ার আগাছা তোলাঃ চারার গোড়ার এক হাত সমপরিমানে চতুর্দিক থেকে আগাছা তুলে ফেলুন। মালচিং এর জায়গা হাল্কা ফাকা করে আগাছা তুলে ফেলতে হবে যেন গাছের গোড়ার ক্ষতি না হয়। ড্রেনের আগাছা তোলাঃ এক্ষেত্রে ড্রেন থেকে মূলসহ আগাছা উপড়ে ফেলতে হবে।"
    a2 = "সকাল"
    a3 = "৯-১১টা"
    return a1, a2, a3

def day_seed30():
    a1 = "দমন ব্যবস্থাপনা ---> সম্পদ ১.৫ গ্রাম/লিটার + ইয়োকো ১ মিলি/লিটার + স্টারথেন ১ গ্রাম/লিটার"
    a2 = "সকাল"
    a3 = "৭-৮টা"
    b1 = "পরিচর্যা ---> কোন চারা রোগাক্রান্ত হলে তা দ্রুত তুলে ফেলুন। জমিতে রসের অভাব দেখা দিলে সেচ দিন"
    b2 = "সকাল"
    b3 = "৯-১১টা"
    return a1, a2, a3, b1, b2, b3

# ------------------------ Weather-based dynamic manual ------------------------


def weather_report(city):
    api_key = "1bd0be556664fb2dcaa474e56927746d"
    base_url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"
    try:
        response = requests.get(base_url)
        response.raise_for_status()
        data = response.json()
        return (
            data["main"]["temp"],
            data["main"]["humidity"],
            data["weather"][0]["main"],
            data["wind"]["speed"]
        )
    except requests.RequestException:
        return None, None, "Unknown", None

# ------------------------ Central control Logic ------------------------

def center(day, crop="cucumber", city="Dhaka", phase="জমি প্রস্তুতকালীন সময়কাল"):
    temp, humidity, weather_desc, wind_speed = weather_report(city)
    if temp is None:
        return "Weather data unavailable. Try again later.", None, None, None, None
    if crop.lower() == "cucumber":
        return cucumber(day, temp, humidity, weather_desc, wind_speed, phase), temp, humidity, weather_desc, wind_speed
    return f"No logic defined for crop: {crop}", None, None, None, None




def cucumber(day, temp, humidity, weather_desc, wind_speed, phase):
    if weather_desc:
        if phase == "জমি প্রস্তুতকালীন সময়কাল":
            if day == 1:
                return day01()
            elif day == 2:
                return day02()
            elif day == 3:
                return day03()
            else:
                return "এই দিনের জন্য কোনো নির্দেশনা পাওয়া যায়নি।"
        elif phase == "সংবেদনশীল সময়কাল":
            if day in [1, 2, 3, 4]:
                return day_seed02()
            elif day in [5, 6]:
                return day_seed05()
            elif day in [7, 8, 9]:
                return day_seed07()
            elif day in [10, 11]:
                return day_seed10()
            elif day in [12, 13, 14]:
                return day_seed12()
            elif day in [15, 16]:
                return day_seed15()
            elif day in [17, 18]:
                return day_seed17()
            elif day == 19:
                return day_seed19()
            elif day in [20, 21, 22, 23, 24]:
                return day_seed20()
            elif day == 25:
                return day_seed25()
            elif day in [26, 27, 28, 29]:
                return day_seed26()
            elif day == 30:
                return day_seed30()
            else:
                return "এই দিনের জন্য কোনো নির্দেশনা পাওয়া যায়নি।"
        else:
            return "পর্যায়ের তথ্য সঠিক নয়।"
    return "এই আবহাওয়ায় চাষের জন্য উপযুক্ত পরিকল্পনা পাওয়া যায়নি।"





# Load the model
model = keras.models.load_model('model/tomato_disease.h5')

# Class labels
class_labels = [
    'Tomato_Bacterial_spot',
    'Tomato_Early_blight',
    'Tomato_Late_blight',
    'Tomato_Leaf_Mold',
    'Tomato_Septoria_leaf_spot',
    'Tomato_Spider_mites_Two_spotted_spider_mite',
    'Tomato__Target_Spot',
    'Tomato__Tomato_YellowLeaf__Curl_Virus',
    'Tomato__Tomato_mosaic_virus',
    'Tomato_healthy'
]

# Disease prevention dictionary
disease_prevention = {
    "Tomato_Bacterial_spot": [
        "Prevent bacterial spot by using disease-free seeds.",
        "Implement crop rotation to reduce the disease's prevalence.",
        "Apply copper-based fungicides to control the disease."
    ],
    "Tomato_Early_blight": [
        "Prevent early blight by practicing good garden hygiene.",
        "Ensure proper watering to avoid splashing soil onto the leaves.",
        "Apply fungicides as needed to control the disease."
    ],
    "Tomato_Late_blight": [
        "Prevent late blight by providing good air circulation in your garden or greenhouse.",
        "Avoid overhead watering, as wet leaves can encourage the disease.",
        "Apply fungicides when necessary to manage the disease."
    ],
    "Tomato_Leaf_Mold": [
        "Prevent leaf mold by ensuring good air circulation and spacing between plants.",
        "Avoid wetting the leaves when watering, and water the soil instead.",
        "Apply fungicides if the disease is present and worsening."
    ],
    "Tomato_Septoria_leaf_spot": [
        "Prevent Septoria leaf spot by maintaining good garden hygiene.",
        "Avoid overhead watering to keep the leaves dry.",
        "Apply fungicides if the disease becomes a problem."
    ],
    "Tomato_Spider_mites_Two_spotted_spider_mite": [
        "Prevent spider mite infestations by regularly inspecting your plants for signs of infestation.",
        "Increase humidity in the growing area to discourage mites.",
        "Use insecticidal soap or neem oil to control mites if necessary."
    ],
    "Tomato__Target_Spot": [
        "Prevent target spot by ensuring good air circulation and avoiding overcrowding of plants.",
        "Water at the base of the plants, keeping the leaves dry.",
        "Apply fungicides as needed to control the disease."
    ],
    "Tomato__Tomato_YellowLeaf__Curl_Virus": [
        "Prevent Tomato Yellow Leaf Curl Virus by using virus-free tomato plants.",
        "Control whiteflies, which transmit the virus, with insecticides.",
        "Remove and destroy infected plants to prevent the spread of the disease."
    ],
    "Tomato__Tomato_mosaic_virus": [
        "Prevent tomato mosaic virus by using virus-free seeds and disease-resistant tomato varieties.",
        "Control aphids, which transmit the virus, with insecticides.",
        "Remove and destroy infected plants to prevent further spread."
    ],
    "Tomato_healthy": [
        "If your tomato plant is healthy, continue to monitor for pests and diseases regularly.",
        "Follow good gardening practices, including proper watering, fertilization, and maintenance."
    ]
}

def read_image(image_bytes):
    img = Image.open(io.BytesIO(image_bytes)).resize((256, 256))
    img = np.array(img)
    return img




# ------------------------------------routing start--------------------++++++++++-------------






@app.route('/signup', methods=['POST'])
def signup():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')
    
    

    if mongo.db.users.find_one({'email': email}):
        return jsonify({'message': 'User already exists'}), 409

    hashed_pw = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    mongo.db.users.insert_one({
        'email': email,
        'password': hashed_pw,
        'first_name': data.get('firstName'),
        'last_name': data.get('lastName'),
        'phone': data.get('phone'),
        "department": data.get('department'),
        "gender": data.get('gender'),
        'created_at': datetime.datetime.utcnow()
    })

    return jsonify({'message': 'Signup successful'}), 201

@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')

    if not email or not password:
        return jsonify({'message': 'Email and password are required.'}), 400

    user = mongo.db.users.find_one({'email': email})
    if not user:
        return jsonify({'message': 'Invalid credentials'}), 401

    stored_password = user.get('password')
    if isinstance(stored_password, str):
        stored_password = stored_password.encode('utf-8')

    if bcrypt.checkpw(password.encode('utf-8'), stored_password):
        token = jwt.encode(
            {'email': email, 'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=1)},
            app.config['SECRET_KEY'],
            algorithm='HS256'
        )
        # If jwt.encode() returns bytes, decode to string
        if isinstance(token, bytes):
            token = token.decode('utf-8')
        return jsonify({'token': token})
    else:
        return jsonify({'message': 'Invalid credentials'}), 401

@app.route('/profile', methods=['GET'])
def profile():
    token = request.headers.get('Authorization')
    if not token:
        return jsonify({'message': 'Missing token'}), 403

    try:
        decoded = jwt.decode(token, app.config['SECRET_KEY'], algorithms=['HS256'])
        return jsonify({'message': f"Welcome {decoded['email']}!"})
    except jwt.ExpiredSignatureError:
        return jsonify({'message': 'Token expired'}), 401
    except jwt.InvalidTokenError:
        return jsonify({'message': 'Invalid token'}), 401
    
@app.route('/logout', methods=['POST'])
def logout():
    # In a stateless JWT setup, you might not need to handle logout on the server.
    # However, you can implement token blacklisting here if desired.
    return jsonify({'message': 'Logged out successfully'}), 200



@app.route('/image')
def home():
    return render_template('image.html')

@app.route('/detect', methods=['POST'])
def detect():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400

    try:
        image = read_image(file.read())
        image = np.expand_dims(image, axis=0)
        prediction = model.predict(image)
        pred_index = np.argmax(prediction)
        confidence = float(np.max(prediction[0]))
        predicted_class = class_labels[pred_index]
        prevention = disease_prevention.get(predicted_class, ['Prevention info not available.'])

        return jsonify({
            'prediction': predicted_class,
            'confidence': confidence,
            'prevention_measures': prevention
        })

    except Exception as e:
        return jsonify({'error': str(e)}), 500
    
    
    

# ------------------------ Crop manual Functions for cucumber ------------------------



# ------------------------ Weather API ------------------------


# ------------------------ Flask Routes ------------------------


@app.route("/register")
def register():
    return render_template("singup.html")

@app.route("/")
def loginpage():
    return render_template("login.html")

@app.route("/Crop_pred")
def crop_p():
    return render_template("crop.html")


@app.route("/home")
def index():
    return render_template("index.html")


@app.route("/D_pred")
def D_pred():
    return render_template("Dpred.html")

@app.route("/weather", methods=["GET", "POST"])
def weather():
    weather_data = None
    error = None
    if request.method == "POST":
        city = request.form.get("city", "Dhaka")
        temp, humidity, weather_desc, wind_speed = weather_report(city)
        if temp is None:
            error = "Could not fetch weather. Check your city name."
        else:
            weather_data = {
                "Temperature": temp,
                "Humidity": humidity,
                "Weather": weather_desc,
                "Wind Speed": wind_speed
            }
    return render_template("weather.html", weather_data=weather_data, error=error)







@app.route("/crop_manuals", methods=["GET", "POST"])
def crop_manuals():
    error = None
    result = None
    temp = None
    humidity = None
    weather_desc = None
    wind_speed = None
    df_data = None
    tuple_items = []
    start_date = date.today().strftime("%Y-%m-%d")
    city = "Dhaka"
    phase = "জমি প্রস্তুতকালীন সময়কাল"
    day = 1
    chara = "No"
    dynamic_choice = "Yes"

    if request.method == "POST":
        dynamic_choice = request.form.get("dynamic_choice", "Yes")
        if dynamic_choice == "No":
            return render_template("crop_manuals.html", redirect_to_manual=True)

        start_date = request.form.get("start_date", date.today().strftime("%Y-%m-%d"))
        city = request.form.get("city", "Dhaka")
        phase = request.form.get("phase", "জমি প্রস্তুতকালীন সময়কাল")
        day = int(request.form.get("day", 1))
        chara = request.form.get("chara", "No")

        if phase == "সংবেদনশীল সময়কাল" and chara == "No":
            error = "চারা গজানোর জন্য অপেক্ষা করুন।"
        else:
            result, temp, humidity, weather_desc, wind_speed = center(day, "cucumber", city, phase)
            if isinstance(result, str):
                error = result
            else:
                step_items = [item for item in result if isinstance(item, str)]
                tuple_items = [item for item in result if isinstance(item, tuple)]
                steps = len(step_items) // 3
                step_numbers = [str(i + 1) for i in range(steps)]
                descriptions = [step_items[i * 3] for i in range(steps)]
                times_of_day = [step_items[i * 3 + 1] for i in range(steps)]
                time_ranges = [step_items[i * 3 + 2] for i in range(steps)]
                df_data = [
                    {"Step": num, "Task Description": desc, "Time of Day": tod, "Time Range": tr}
                    for num, desc, tod, tr in zip(step_numbers, descriptions, times_of_day, time_ranges)
                ]

    return render_template(
        "crop_manuals.html",
        error=error,
        df_data=df_data,
        tuple_items=tuple_items,
        temp=temp,
        humidity=humidity,
        weather_desc=weather_desc,
        wind_speed=wind_speed,
        start_date=start_date,
        city=city,
        phase=phase,
        day=day,
        chara=chara,
        dynamic_choice=dynamic_choice,
        redirect_to_manual=False
    )





if __name__ == '__main__':
    app.run(debug=True)
