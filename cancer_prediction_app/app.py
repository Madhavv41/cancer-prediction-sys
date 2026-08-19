from flask import Flask, render_template, request, redirect, url_for, session
from werkzeug.security import generate_password_hash, check_password_hash
from functools import wraps
import pandas as pd
import joblib

import db
from predict import run_prediction

app = Flask(__name__)
app.secret_key = "cancer-care-ai-secret-key-change-in-production"

db.init_db()

# Load trained model and scaler (kept for legacy route)
model = joblib.load("rf_model.pkl")
scaler = joblib.load("scaler.pkl")

feature_names = [
    "Age",
    "Gender",
    "BMI",
    "Smoking",
    "GeneticRisk",
    "PhysicalActivity",
    "AlcoholIntake",
    "CancerHistory"
]

scale_columns = [
    "Age",
    "BMI",
    "PhysicalActivity",
    "AlcoholIntake"
]


def login_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if not session.get("user_id"):
            return redirect(url_for("login"))
        return f(*args, **kwargs)
    return decorated


# ===== NEW ROUTES =====

@app.route("/")
def home():
    return render_template("home.html")


@app.route("/predict", methods=["GET", "POST"])
def predict_route():
    if request.method == "GET":
        return render_template("predict.html")

    try:
        result = run_prediction(request.form)

        if session.get("user_id"):
            db.save_prediction(session["user_id"], request.form, result)

        return render_template("predict.html", **result)

    except Exception as e:
        return render_template("predict.html", error=f"Error: {str(e)}")


@app.route("/register", methods=["GET", "POST"])
def register():
    if session.get("user_id"):
        return redirect(url_for("home"))

    if request.method == "GET":
        return render_template("register.html")

    username = request.form.get("username", "").strip()
    email = request.form.get("email", "").strip()
    password = request.form.get("password", "")
    confirm = request.form.get("confirm_password", "")

    if len(username) < 3:
        return render_template("register.html", error="Username must be at least 3 characters.")
    if len(password) < 6:
        return render_template("register.html", error="Password must be at least 6 characters.")
    if password != confirm:
        return render_template("register.html", error="Passwords do not match.")
    if db.get_user_by_username(username):
        return render_template("register.html", error="Username already taken.")
    if db.get_user_by_email(email):
        return render_template("register.html", error="Email already registered.")

    password_hash = generate_password_hash(password)
    db.create_user(username, email, password_hash)

    return redirect(url_for("login", registered=1))


@app.route("/login", methods=["GET", "POST"])
def login():
    if session.get("user_id"):
        return redirect(url_for("home"))

    if request.method == "GET":
        success = "Account created successfully! Please sign in." if request.args.get("registered") else None
        return render_template("login.html", success=success)

    username = request.form.get("username", "").strip()
    password = request.form.get("password", "")

    user = db.get_user_by_username(username)
    if not user or not check_password_hash(user["password_hash"], password):
        return render_template("login.html", error="Invalid username or password.")

    session["user_id"] = user["id"]
    session["username"] = user["username"]
    return redirect(url_for("home"))


@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("home"))


@app.route("/history")
@login_required
def history():
    predictions = db.get_predictions_for_user(session["user_id"])
    cancer_count = sum(1 for p in predictions if p["prediction_label"] == "Cancer")
    no_cancer_count = len(predictions) - cancer_count
    return render_template(
        "history.html",
        predictions=predictions,
        cancer_count=cancer_count,
        no_cancer_count=no_cancer_count,
    )


# ===== LEGACY ROUTES (original code preserved) =====

@app.route("/legacy")
def legacy_home():
    return render_template("index.html")


@app.route("/legacy/predict", methods=["POST"])
def legacy_predict():
    try:
        age = float(request.form["age"])
        gender = int(request.form["gender"])
        bmi = float(request.form["bmi"])
        smoking = int(request.form["smoking"])
        genetic_risk = int(request.form["genetic_risk"])
        physical_activity = float(request.form["physical_activity"])
        alcohol_intake = float(request.form["alcohol_intake"])
        cancer_history = int(request.form["cancer_history"])

        input_df = pd.DataFrame(
            [[
                age,
                gender,
                bmi,
                smoking,
                genetic_risk,
                physical_activity,
                alcohol_intake,
                cancer_history
            ]],
            columns=feature_names
        )

        input_df[scale_columns] = scaler.transform(
            input_df[scale_columns]
        )

        probs = model.predict_proba(input_df)[0]
        pred_index = int(probs.argmax())

        if pred_index == 1:
            pred_label = "Cancer"
        else:
            pred_label = "No Cancer"

        confidence = float(probs[pred_index])

        return render_template(
            "index.html",
            prediction=pred_label,
            diagnosis=pred_index,
            confidence=f"{confidence:.2%}"
        )

    except Exception as e:
        return render_template(
            "index.html",
            error=f"Error: {str(e)}"
        )


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
