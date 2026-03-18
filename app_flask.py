from flask import Flask, render_template, request, jsonify, session, redirect, url_for
from drug_drug_checker import check_ddi
from drug_info import get_drug_info
from drug_food_classifier import DrugFoodClassifier
from ddi_classifier import DDIClassifier
from pymongo import MongoClient
from dotenv import load_dotenv
import os

load_dotenv()

app = Flask(__name__)

# 🔐 Secret key
app.secret_key = os.environ.get("SECRET_KEY", "fallback_secret")

# =========================
# 🟢 MongoDB Connection
# =========================
client = MongoClient(os.environ.get("MONGO_URI"))
db = client["drugsafe"]
users_collection = db["users"]

# =========================
# 🧠 Initialize Models
# =========================
classifier = DrugFoodClassifier()
ddi_classifier = DDIClassifier()


# ==========================================================
# 🔐 LOGIN SYSTEM
# ==========================================================
@app.route('/login', methods=['GET', 'POST'])
def login():

    if 'user' in session:
        return redirect(url_for('home'))

    if request.method == 'POST':

        username = request.form.get('username').strip().lower()
        password = request.form.get('password').strip()

        user = users_collection.find_one({"username": username})

        if user and user["password"] == password:
            session['user'] = username
            return redirect(url_for('home'))

        return render_template("login.html", error="Invalid username or password")

    return render_template('login.html')


# ==========================================================
# 🆕 REGISTER SYSTEM
# ==========================================================
@app.route('/register', methods=['GET', 'POST'])
def register():

    if request.method == 'POST':

        username = request.form.get('username').strip().lower()
        password = request.form.get('password').strip()

        if not username or not password:
            return render_template("register.html", error="All fields required")

        existing_user = users_collection.find_one({"username": username})

        if existing_user:
            return render_template("register.html", error="User already exists")

        users_collection.insert_one({
            "username": username,
            "password": password
        })

        return redirect(url_for('login'))

    return render_template('register.html')


# ==========================================================
# 🔓 LOGOUT
# ==========================================================
@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))


# ==========================================================
# 🔒 LOGIN REQUIRED HELPER
# ==========================================================
def login_required():
    if 'user' not in session:
        return redirect(url_for('login'))
    return None


# ==========================================================
# 🏠 MAIN ROUTES
# ==========================================================
@app.route('/')
def home():
    check = login_required()
    if check:
        return check
    return render_template('home.html')


@app.route('/checker')
def checker():
    check = login_required()
    if check:
        return check
    return render_template('checker.html')


@app.route('/about')
def about():
    check = login_required()
    if check:
        return check
    return render_template('about.html')


@app.route('/contact')
def contact():
    check = login_required()
    if check:
        return check
    return render_template('contact.html')


# ==========================================================
# ⚗️ FOOD–DRUG INTERACTION
# ==========================================================
@app.route('/check_interaction', methods=['POST'])
def check_interaction():

    if 'user' not in session:
        return jsonify({'error': 'Login required'}), 401

    try:
        data = request.get_json(force=True)
        drug = data.get('drug', '').strip()
        food = data.get('food', '').strip()

        if not drug or not food:
            return jsonify({'error': 'Please provide both drug and food names'}), 400

        result = classifier.predict_interaction(drug, food)
        return jsonify(result)

    except Exception as e:
        return jsonify({'error': f'Error checking interaction: {str(e)}'}), 500


# ==========================================================
# 💊 DRUG–DRUG INTERACTION (🔥 UPGRADED)
# ==========================================================
@app.route('/ddi')
def ddi_page():
    check = login_required()
    if check:
        return check
    return render_template('ddi.html')


@app.route('/check_ddi', methods=['POST'])
def check_ddi_route():

    if 'user' not in session:
        return jsonify({'error': 'Login required'}), 401

    try:
        data = request.get_json(force=True)
        drug1 = (data or {}).get('drug1', '').strip()
        drug2 = (data or {}).get('drug2', '').strip()

        if not drug1 or not drug2:
            return jsonify({'error': 'Please provide two drug names'}), 400

        # ==================================================
        # 🔥 TRY GROQ FIRST
        # ==================================================
        try:
            result = check_ddi(drug1, drug2)

            # If API failed or weak response
            if not result or result.get("provider") in ["None", "Unknown"]:
                raise Exception("Groq failed")

        except Exception as e:
            print("⚠️ Groq failed → Using Classifier:", e)

            # ==================================================
            # 🔁 FALLBACK TO CLASSIFIER
            # ==================================================
            result = ddi_classifier.predict_interaction(drug1, drug2)
        result.pop("probider",None)
        return jsonify({'DDI_Result': result})

    except Exception as e:
        return jsonify({'error': f'Error analyzing DDI: {str(e)}'}), 500


# ==========================================================
# 💊 DRUG INFORMATION
# ==========================================================
@app.route('/druginfo')
def druginfo_page():
    check = login_required()
    if check:
        return check
    return render_template('drug_info.html')


@app.route('/drug_info', methods=['POST'])
def drug_info_route():

    if 'user' not in session:
        return jsonify({'error': 'Login required'}), 401

    try:
        data = request.get_json(force=True)
        drug = (data or {}).get('drug', '').strip()

        if not drug:
            return jsonify({'Drug_Info': {'error': 'Drug name required'}})

        info = get_drug_info(drug)

        return jsonify({"Drug_Info": info})

    except Exception as e:
        return jsonify({"Drug_Info": {"error": str(e)}})


# ==========================================================
# 🚀 PRODUCTION ENTRY POINT
# ==========================================================
if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)