from flask import Flask, render_template, request, jsonify
from drug_drug_checker import check_ddi
from drug_info import get_drug_info
from drug_food_classifier import DrugFoodClassifier
import os

app = Flask(__name__)

# Initialize FDI classifier
classifier = DrugFoodClassifier()

# ==========================================================
# 🏠 MAIN ROUTES
# ==========================================================
@app.route('/')
def home():
    return render_template('home.html')


@app.route('/checker')
def checker():
    return render_template('checker.html')


@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/contact')
def contact():
    return render_template('contact.html')


# ==========================================================
# ⚗️ FOOD–DRUG INTERACTION
# ==========================================================
@app.route('/check_interaction', methods=['POST'])
def check_interaction():
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
# 💊 DRUG–DRUG INTERACTION
# ==========================================================
@app.route('/ddi')
def ddi_page():
    return render_template('ddi.html')


@app.route('/check_ddi', methods=['POST'])
def check_ddi_route():
    try:
        data = request.get_json(force=True)
        drug1 = (data or {}).get('drug1', '').strip()
        drug2 = (data or {}).get('drug2', '').strip()

        if not drug1 or not drug2:
            return jsonify({'error': 'Please provide two drug names'}), 400

        result = check_ddi(drug1, drug2)
        return jsonify({'DDI_Result': result})

    except Exception as e:
        return jsonify({'error': f'Error analyzing DDI: {str(e)}'}), 500


# ==========================================================
# 💊 DRUG INFORMATION
# ==========================================================
@app.route('/druginfo')
def druginfo_page():
    return render_template('drug_info.html')


@app.route('/drug_info', methods=['POST'])
def drug_info_route():
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
# 🚀 PRODUCTION ENTRY POINT (Render Compatible)
# ==========================================================
if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)