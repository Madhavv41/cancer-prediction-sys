# Cancer Prediction System

A Machine Learning based web application that predicts cancer risk using patient health information.

## Project Overview

This project uses a Random Forest Classifier to predict whether a patient is at risk of cancer based on factors such as:

- Age
- Gender
- BMI
- Smoking Habits
- Genetic Risk
- Physical Activity
- Alcohol Intake
- Cancer History

The model is integrated with a Flask web application that allows users to enter patient details and receive instant predictions.

---

## Technologies Used

### Machine Learning
- Python
- Pandas
- NumPy
- Scikit-Learn

### Data Visualization
- Matplotlib

### Web Development
- Flask
- HTML
- CSS

### Version Control
- Git
- GitHub

---

## Dataset Features

| Feature | Description |
|----------|-------------|
| Age | Patient Age |
| Gender | Male/Female |
| BMI | Body Mass Index |
| Smoking | Smoking Status |
| GeneticRisk | Family Genetic Risk |
| PhysicalActivity | Activity Level |
| AlcoholIntake | Alcohol Consumption |
| CancerHistory | Previous Cancer History |
| Diagnosis | Target Variable |

---

## Data Preprocessing

The following preprocessing steps were performed:

- Missing value checking
- Duplicate removal
- Column name cleaning
- Data type verification
- Exploratory Data Analysis (EDA)
- Feature selection

---

## Model Used

### Random Forest Classifier

Reasons for choosing Random Forest:

- Handles tabular data effectively
- Reduces overfitting
- Provides feature importance
- Good classification performance

---

## Performance Metrics

The model was evaluated using:

- Accuracy
- Precision
- Recall
- F1 Score
- Confusion Matrix

Example:

```python
Accuracy : XX%
Precision: XX%
Recall   : XX%
F1 Score : XX%
```

Replace with your actual results.

---

## Project Structure

```text
cancer_prediction_app/
│
├── app.py
├── predict.py
├── db.py
├── requirements.txt
├── rf_model.pkl
├── scaler.pkl
│
├── templates/
│   ├── index.html
│   ├── home.html
│   ├── login.html
│   ├── register.html
│   ├── history.html
│   └── predict.html
│
├── static/
│   ├── style.css
│   └── main.js
│
└── data/
    └── cancer_app.db
```

---

## Installation

Clone the repository:

```bash
git clone https://github.com/Madhavv41/cancer-prediction-sys.git
```

Move into project folder:

```bash
cd cancer_prediction_app
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Run the Flask application:

```bash
python app.py
```

Open browser:

```text
http://127.0.0.1:5000
```

---

## Future Enhancements

- Deep Learning Models
- Real-time Risk Dashboard
- PDF Report Generation
- Cloud Deployment
- User Authentication Improvements

---

## Author

**Madhav V**

B.Tech CSE (Data Science)

GitHub:
https://github.com/Madhavv41

---

## License

This project is created for educational and learning purposes.
