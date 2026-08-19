import pandas as pd
import joblib

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
    "CancerHistory",
]

scale_columns = [
    "Age",
    "BMI",
    "PhysicalActivity",
    "AlcoholIntake",
]


def run_prediction(form_data):
    age = float(form_data["age"])
    gender = int(form_data["gender"])
    bmi = float(form_data["bmi"])
    smoking = int(form_data["smoking"])
    genetic_risk = int(form_data["genetic_risk"])
    physical_activity = float(form_data["physical_activity"])
    alcohol_intake = float(form_data["alcohol_intake"])
    cancer_history = int(form_data["cancer_history"])

    input_df = pd.DataFrame(
        [[
            age,
            gender,
            bmi,
            smoking,
            genetic_risk,
            physical_activity,
            alcohol_intake,
            cancer_history,
        ]],
        columns=feature_names,
    )

    input_df[scale_columns] = scaler.transform(input_df[scale_columns])

    probs = model.predict_proba(input_df)[0]
    pred_index = int(probs.argmax())
    pred_label = "Cancer" if pred_index == 1 else "No Cancer"
    confidence = float(probs[pred_index])

    return {
        "prediction": pred_label,
        "diagnosis": pred_index,
        "confidence": f"{confidence:.2%}",
        "confidence_raw": confidence,
    }
