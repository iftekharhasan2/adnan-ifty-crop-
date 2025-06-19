import os
from flask import Flask, render_template, redirect, url_for, session
import pandas as pd
import requests
from pyngrok import ngrok
from datetime import date
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
app = Flask(__name__)
app.secret_key = os.getenv('FLASK_SECRET_KEY', os.urandom(24).hex())  # Secure fallback key

#tips:  Ctrl + Shift + P fixes idictations

# Create templates directory
os.makedirs('templates', exist_ok=True)
os.makedirs('static', exist_ok=True)

# Write the index.html template
with open('templates/base.html', 'w') as f:
    f.write('''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{% block title %}Crop Recommender App{% endblock %}</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
    <link rel="stylesheet" href="{{ url_for('static', filename='styles.css') }}">
</head>
<body>
    <nav class="navbar navbar-expand-lg navbar-dark bg-success">
        <div class="container">
            <a class="navbar-brand" href="/">🌾 Crop Recommender</a>
            <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarNav">
                <span class="navbar-toggler-icon"></span>
            </button>
            <div class="collapse navbar-collapse" id="navbarNav">
                <ul class="navbar-nav ms-auto">
                    <li class="nav-item">
                        <a class="nav-link" href="/">Home</a>
                    </li>
                    <li class="nav-item">
                        <a class="nav-link" href="/weather">Weather</a>
                    </li>
                    <li class="nav-item">
                        <a class="nav-link" href="/crop_manuals">Crop Manuals</a>
                    </li>
                    <li class="nav-item">
                        <a class="nav-link" href="/D_pred">Diseases Prediction</a>
                    </li>
                    <li class="nav-item">
                        <a class="nav-link" href="/Crop_pred">Crop Prediction</a>
                    </li>
                </ul>
            </div>
        </div>
    </nav>
    <div class="container">
        {% block content %}{% endblock %}
    </div>
    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/js/bootstrap.bundle.min.js"></script>
</body>
</html>




''')




# Write the index.html template
with open('templates/index.html', 'w') as f1:
    f1.write('''

{% extends "base.html" %}
{% block title %}Home - Crop Recommender{% endblock %}
{% block content %}
<div class="header">
    <h1>🌱 Welcome to Crop Recommender</h1>
    <p>Developed by Adnan Rahman</p>
</div>
<div class="card">
    <div class="card-body">
        <h3>🌾 Recommend Crops for Your Farm</h3>
        <p>This section is a placeholder for crop recommendation functionality. Stay tuned for updates!</p>
    </div>
</div>
{% endblock %}



''')


# Write the index.html template
with open('templates/Dpred.html', 'w') as f1:
    f1.write('''

{% extends "base.html" %}
{% block title %}Diseases Prediction - Crop Recommender{% endblock %}
{% block content %}
<div class="header">
    <h1>🌱 placeholder for Diseases Prediction</h1>
    <p>Developed by Adnan Rahman and Polash</p>
</div>
{% endblock %}



''')



# Write the index.html template
with open('templates/crop.html', 'w') as f1:
    f1.write('''

{% extends "base.html" %}
{% block title %}crop Prediction - Crop Recommender{% endblock %}
{% block content %}
<div class="header">
    <h1>🌱 placeholder for Crop Prediction</h1>
    <p>Developed by Adnan Rahman and Polash</p>
</div>
{% endblock %}



''')



# Write the index.html template
with open('templates/weather.html', 'w') as f:
    f.write('''

{% extends "base.html" %}
{% block title %}Weather - Crop Recommender{% endblock %}
{% block content %}
<div class="header">
    <h1>🌦️ Current Weather Information</h1>
</div>
<div class="card">
    <div class="card-body">
        <form method="POST">
            <div class="mb-3">
                <label for="city" class="form-label">📍 Enter your District Name:</label>
                <input type="text" class="form-control" name="city" value="Dhaka" required>
            </div>
            <button type="submit" class="btn btn-primary">Fetch Weather</button>
        </form>
        {% if error %}
        <div class="alert alert-danger mt-3">{{ error }}</div>
        {% endif %}
        {% if weather_data %}
        <div class="weather-data mt-3">
            <h3>Weather Information</h3>
            <p><strong>Temperature:</strong> {{ weather_data.Temperature }}°C</p>
            <p><strong>Humidity:</strong> {{ weather_data.Humidity }}%</p>
            <p><strong>Weather Condition:</strong> {{ weather_data.Weather }}</p>
            <p><strong>Wind Speed:</strong> {{ weather_data['Wind Speed'] }} m/s</p>
            <div class="alert alert-success">
                <a href="https://docs.google.com/document/d/1zAfRxq70L-Akjt9T9Hthoe-FQNrsUTei6KtNNkE6EIk/edit?usp=drivesdk" target="_blank" class="alert-link">
                    Click to Open the Manual
                </a>
            </div>
        </div>
        {% endif %}
    </div>
</div>
{% endblock %}



''')



# Write the index.html template
with open('templates/crop_manuals.html', 'w') as f:
    f.write('''

{% extends "base.html" %}
{% block title %}Crop Manuals - Crop Recommender{% endblock %}
{% block content %}
<div class="header">
    <h1>🌾 ফসল পরিকল্পনা সহায়ক</h1>
    <p>Developed by Adnan Rahman</p>
</div>
{% if redirect_to_manual %}
<div class="alert alert-info">
    <a href="https://docs.google.com/document/d/1Kl2pIYCwxvkz_79dfApkrB7yNdNawtPO/edit?usp=sharing&ouid=103687624693269329103&rtpof=true&sd=true" target="_blank" class="alert-link">
        Proceed to Cucumber Manual - Google Docs
    </a>
</div>
{% else %}
<div class="card">
    <div class="card-body">
        <form method="POST">
            <div class="mb-3">
                <label class="form-label">Do you want dynamic mangement for ur crop?</label>
                <div class="form-check">
                    <input class="form-check-input" type="radio" name="dynamic_choice" value="Yes" {% if dynamic_choice == "Yes" %}checked{% endif %}>
                    <label class="form-check-label">Yes</label>
                </div>
                <div class="form-check">
                    <input class="form-check-input" type="radio" name="dynamic_choice" value="No" {% if dynamic_choice == "No" %}checked{% endif %}>
                    <label class="form-check-label">No</label>
                </div>
            </div>
            <div class="mb-3">
                <label for="start_date" class="form-label">📅 When do you want to start?</label>
                <input type="date" class="form-control" name="start_date" value="{{ start_date }}" required>
            </div>
            <div class="mb-3">
                <label for="city" class="form-label">📍 What is your area?</label>
                <input type="text" class="form-control" name="city" value="{{ city }}" required>
            </div>
            <div class="mb-3">
                <label for="phase" class="form-label">📘 Phase</label>
                <select class="form-select" name="phase">
                    <option value="জমি প্রস্তুতকালীন সময়কাল" {% if phase == "জমি প্রস্তুতকালীন সময়কাল" %}selected{% endif %}>জমি প্রস্তুতকালীন সময়কাল</option>
                    <option value="সংবেদনশীল সময়কাল" {% if phase == "সংবেদনশীল সময়কাল" %}selected{% endif %}>সংবেদনশীল সময়কাল</option>
                </select>
            </div>
            <div class="mb-3">
                <label for="day" class="form-label">📅 Day</label>
                <input type="number" class="form-control" name="day" value="{{ day }}" min="1" max="30" required>
            </div>
            <div class="mb-3" {% if phase != "সংবেদনশীল সময়কাল" %}style="display:none;"{% endif %}>
                <label class="form-label">❓ চারা গজিয়েছে?</label>
                <div class="form-check">
                    <input class="form-check-input" type="radio" name="chara" value="Yes" {% if chara == "Yes" %}checked{% endif %}>
                    <label class="form-check-label">Yes</label>
                </div>
                <div class="form-check">
                    <input class="form-check-input" type="radio" name="chara" value="No" {% if chara == "No" %}checked{% endif %}>
                    <label class="form-check-label">No</label>
                </div>
            </div>
            <button type="submit" class="btn btn-primary">Submit</button>
        </form>
    </div>
</div>
{% if error %}
<div class="alert alert-danger">{{ error }}</div>
{% endif %}
{% if df_data %}
<div class="card">
    <div class="card-header">
        <h3>✅ শসা চাষের প্রস্তুতি সময়সূচি</h3>
    </div>
    <div class="card-body">
        <table class="table table-bordered">
            <thead>
                <tr>
                    <th>ধাপ (Step)</th>
                    <th>কাজের বিবরণ (Task Description)</th>
                    <th>সময়কাল (Time of Day)</th>
                    <th>সময় সীমা (Time Range)</th>
                </tr>
            </thead>
            <tbody>
                {% for row in df_data %}
                <tr>
                    <td>{{ row.Step }}</td>
                    <td>{{ row['Task Description'] }}</td>
                    <td>{{ row['Time of Day'] }}</td>
                    <td>{{ row['Time Range'] }}</td>
                </tr>
                {% endfor %}
            </tbody>
        </table>
    </div>
</div>
{% if tuple_items %}
<div class="card">
    <div class="card-header">
        <h3>📌 অতিরিক্ত নির্দেশনা</h3>
    </div>
    <div class="card-body additional-instructions">
        {% for tup in tuple_items %}
            {% for statement in tup %}
            <p>🔸 {{ statement }}</p>
            {% endfor %}
        {% endfor %}
    </div>
</div>
{% endif %}
{% if list_items %}
<div class="card mt-3">
    <div class="card-header">
        <h3>📝 তালিকা নির্দেশনা</h3>
    </div>
    <div class="card-body list-instructions">
        {% for lst in list_items %}
            {% for item in lst %}
                <p>🔹 {{ item }}</p>
            {% endfor %}
        {% endfor %}
    </div>
</div>
{% endif %}
<div class="card">
    <div class="card-header">
        <h3>🌦️ আবহাওয়া তথ্য</h3>
    </div>
    <div class="card-body">
        <p><strong>তাপমাত্রা:</strong> {{ temp }}°C</p>
        <p><strong>আর্দ্রতা:</strong> {{ humidity }}%</p>
        <p><strong>আবহাওয়া:</strong> {{ weather_desc }}</p>
        <p><strong>বাতাসের গতি:</strong> {{ wind_speed }} m/s</p>
    </div>
</div>
<div class="video-container">
    <iframe width="100%" height="315" src="https://www.youtube.com/embed/Vf_shMr3pbw" frameborder="0" allowfullscreen></iframe>
</div>
{% endif %}
{% endif %}
{% endblock %}


''')




# Write the index.html template
with open('static/styles.css', 'w') as f:
    f.write('''

/* General body styling */
body {
    background-color: #f0f4f1; /* Light green-gray for agricultural theme */
    font-family: 'Arial', sans-serif;
    color: #333;
    line-height: 1.6;
}

/* Container styling */
.container {
    max-width: 1200px;
    margin: 20px auto;
    padding: 0 15px;
}

/* Navbar styling */
.navbar {
    background-color: #2e7d32; /* Green for agricultural theme */
    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.navbar-brand {
    font-size: 1.5rem;
    font-weight: bold;
}

.nav-link {
    color: white !important;
    font-weight: 500;
    margin-left: 15px;
}

.nav-link:hover {
    color: #c8e6c9 !important;
}

/* Header styling */
.header {
    text-align: center;
    margin-bottom: 40px;
    padding: 20px;
    background-color: #4caf50;
    color: white;
    border-radius: 8px;
    box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
}

.header h1 {
    font-size: 2.5rem;
    margin-bottom: 10px;
}

.header p {
    font-size: 1.2rem;
    opacity: 0.9;
}

/* Card styling */
.card {
    background-color: #ffffff;
    border: none;
    border-radius: 10px;
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
    margin-bottom: 30px;
}

.card-header {
    background-color: #4caf50;
    color: white;
    font-weight: bold;
    border-radius: 8px 8px 0 0;
    padding: 15px;
}

.card-body {
    padding: 20px;
}

/* Form elements */
.form-label {
    font-weight: 600;
    color: #2e7d32;
    margin-bottom: 8px;
}

.form-control, .form-select {
    border: 2px solid #81c784;
    border-radius: 6px;
    padding: 10px;
    font-size: 1rem;
}

.form-control:focus, .form-select:focus {
    border-color: #2e7d32;
    box-shadow: 0 0 5px rgba(46, 125, 50, 0.3);
}

.form-check-label {
    margin-left: 8px;
    color: #444;
}

.btn-primary {
    background-color: #2e7d32;
    border-color: #2e7d32;
    padding: 10px 20px;
    font-size: 1.1rem;
    border-radius: 6px;
    transition: background-color 0.3s ease;
}

.btn-primary:hover {
    background-color: #1b5e20;
    border-color: #1b5e20;
}

/* Table styling */
.table {
    background-color: #ffffff;
    border-radius: 8px;
    overflow: hidden;
    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

.table th {
    background-color: #81c784;
    color: white;
    font-weight: 600;
    padding: 12px;
}

.table td {
    padding: 12px;
    vertical-align: middle;
    border-bottom: 1px solid #e0e0e0;
}

.table tr:last-child td {
    border-bottom: none;
}

/* Alert styling */
.alert {
    border-radius: 6px;
    padding: 15px;
    margin-bottom: 20px;
}

.alert-danger {
    background-color: #ffebee;
    color: #c62828;
}

.alert-info, .alert-success {
    background-color: #e8f5e9;
    color: #2e7d32;
}

.alert-link {
    color: #1b5e20;
    font-weight: bold;
}

/* Video container */
.video-container {
    margin-top: 30px;
    text-align: center;
}

.video-container iframe {
    border-radius: 8px;
    box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
    max-width: 100%;
}

/* Additional instructions */
.additional-instructions p {
    background-color: #e8f5e9;
    padding: 10px;
    border-left: 4px solid #2e7d32;
    border-radius: 4px;
    margin-bottom: 10px;
}

/* Responsive adjustments */
@media (max-width: 768px) {
    .header h1 {
        font-size: 2rem;
    }

    .header p {
        font-size: 1rem;
    }

    .form-control, .form-select {
        font-size: 0.9rem;
    }

    .btn-primary {
        width: 100%;
        padding: 12px;
    }

    .table th, .table td {
        font-size: 0.9rem;
        padding: 10px;
    }

    .navbar-brand {
        font-size: 1.2rem;
    }

    .nav-link {
        margin-left: 10px;
    }
}



''')
#######################################################################

# Initialize Flask app
from flask import Flask, render_template, request
import pandas as pd
import requests
from datetime import date

app = Flask(__name__)

# ------------------------ Crop manual Functions for cucumber ------------------------

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


extra_note = []

def add_note(note):
    extra_note.append(note)

def clear_note():
    extra_note.clear()

def cucumber(day, temp, humidity, weather_desc, wind_speed, phase):
    note = ""

    # Phase-based day instructions
    if phase == "জমি প্রস্তুতকালীন সময়কাল":
        if day == 1:
            note = day01()
        elif day == 2:
            note = day02()
        elif day == 3:
            note = day03()
        else:
            note = "এই দিনের জন্য কোনো নির্দেশনা পাওয়া যায়নি।"

    elif phase == "সংবেদনশীল সময়কাল":
        if day in [1, 2, 3, 4]:
            note = day_seed02()
        elif day in [5, 6]:
            note = day_seed05()
        elif day in [7, 8, 9]:
            note = day_seed07()
        elif day in [10, 11]:
            note = day_seed10()
        elif day in [12, 13, 14]:
            note = day_seed12()
        elif day in [15, 16]:
            note = day_seed15()
        elif day in [17, 18]:
            note = day_seed17()
        elif day == 19:
            note = day_seed19()
        elif day in [20, 21, 22, 23, 24]:
            note = day_seed20()
        elif day == 25:
            note = day_seed25()
        elif day in [26, 27, 28, 29]:
            note = day_seed26()
        elif day == 30:
            note = day_seed30()
        else:
            note = "এই দিনের জন্য কোনো নির্দেশনা পাওয়া যায়নি।"

    else:
        note = "এই পর্যায়ের জন্য কোনো নির্দেশনা পাওয়া যায়নি।"

    # Postpone if rain or haze
    if weather_desc in ["Rain", "Haze"]:
        add_note(note)
        sp_3 = ("আজ বৃষ্টি বা অতিরিক্ত শিশিরের কারণে নির্ধারিত কার্যক্রম স্থগিত করা হয়েছে। আবহাওয়া পরিষ্কার হলে পরবর্তী দিনে এ কার্যক্রম পুনরায় সম্পাদিত হবে।", )
        return  sp_3

    # Retrieve and clear any carried-over notes
    xtra = extra_note.copy()
    clear_note()  # <-- must call the function

    return note, xtra



# ------------------------ Weather API ------------------------

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

# ------------------------ Flask Routes ------------------------

@app.route("/Crop_pred")
def crop_p():
    return render_template("crop.html")

@app.route("/demo")
def demo():
    return render_template("demo.html")


@app.route("/")
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
    list_items = []
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
                list_items = [item for item in result if isinstance(item, list)]

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
      list_items=list_items,
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


#######################################################################


# Set ngrok authentication token
ngrok.set_auth_token("2sDzUaTZpllEMQSfJt58C2ZNhSK_4gL8tHVmirAje55ZhSgC8")

# Start ngrok tunnel to expose the Flask server
ngrok_tunnel = ngrok.connect(addr='5011', proto='http', bind_tls=True)

# Print the public URL
print(' * Tunnel URL:', ngrok_tunnel.public_url)

if __name__ == '__main__':
    app.run(port=5011)