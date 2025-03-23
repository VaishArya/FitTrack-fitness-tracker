# FitTrack Fitness Tracker 🏋️‍♂️📊

## 📌 Project Overview
FitTrack is a fitness tracking application that utilizes **Fitbit dataset** to analyze user activity, heart rate, and other health parameters. Built using **Python** and various data analysis libraries, this project provides insights into user fitness levels.

## 🚀 Features
- 📈 **Track fitness activities** from Fitbit dataset.
- 📊 **Analyze health metrics** like heart rate, steps, and calories burned.
- 🎯 **User-friendly interface** for data visualization.

## 🛠️ Tech Stack
- **Programming Language:** Python
- **Libraries Used:** Pandas, NumPy, Matplotlib, Seaborn
- **Virtual Environment:** `venv`
- **Dataset Source:** Fitbit

## 📂 Project Structure
```bash
📁 FitTrack-fitness-tracker
│-- 📂 app/           # Main application files
│-- 📂 analysis/      # Data processing & analysis scripts
│-- 📂 screenshots/   # Project screenshots
│-- 📂 data/          # Fitbit dataset
│-- 📜 requirements.txt  # Dependencies
│-- 📜 .gitignore     # Ignored files
│-- 📜 README.md      # Project documentation
```

## 📖 Usage Instructions

### 1️⃣ Clone the Repository
```bash
git clone https://github.com/VaishArya/FitTrack-fitness-tracker.git
cd FitTrack-fitness-tracker
```

### 2️⃣ Create a Virtual Environment
```bash
python3 -m venv venv
```

### 3️⃣ Activate the Virtual Environment
**On macOS/Linux:**
```bash
source venv/bin/activate
```
**On Windows:**
```bash
venv\Scripts\activate
```
### 4️⃣ Install Dependencies
```bash
pip install -r requirements.txt
```

### 4️⃣ Run the Streamlit App
```bash
cd app
python3 -m streamlit run app.py
```

### ⚠️ Note: Code Compatibility  
This project was developed and tested on **Streamlit v1.43.2**.  
Using a different Streamlit version **may cause unexpected issues**.  

#### 🛠️ Check Your Current Streamlit Version  
```bash
streamlit --version

