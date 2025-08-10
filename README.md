# 🖋️ Keystroke Biometrics Authentication using DTW

[![Python](https://img.shields.io/badge/Python-3.x-blue.svg)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![GUI](https://img.shields.io/badge/GUI-Tkinter-green)](https://docs.python.org/3/library/tkinter.html)
[![Algorithm](https://img.shields.io/badge/Algorithm-DTW-orange)](https://en.wikipedia.org/wiki/Dynamic_time_warping)

> **A behavioral biometrics authentication system** that uses **Keystroke Dynamics** and **Dynamic Time Warping (DTW)** to verify a user’s identity based on typing patterns.

---

## 📌 Overview
Keystroke dynamics analyzes the way a user types by measuring **dwell times** (key hold) and **flight times** (interval between keys).  
This project implements a **DTW-based classifier** in a **Tkinter GUI**, allowing:
- **Enrollment**: record a user’s typing profile.
- **Verification**: authenticate based on DTW distance to reference profile.
- **Analysis**: visualize DTW distances and compare samples.

📄 Detailed methodology and evaluation can be found in the [full project report](docs/rapport.pdf).

---

## ✨ Features
- 🖥️ **User-friendly GUI** built with Tkinter.
- ⌨️ **Real-time keystroke capture** using the `keyboard` library.
- 📊 **DTW-based matching** for authentication.
- 📈 **Visualization of DTW distances** per enrollment sample.
- 🔒 Adjustable **authentication threshold**.

---


## 🛠 Installation

### 1️⃣ Clone the repository
```bash
git clone https://github.com/<your-username>/keystroke-biometrics-dtw.git
cd keystroke-biometrics-dtw 
```

### 2️⃣ Install dependencies
```bash
pip install -r requirements.txt
```

## 🚀 Usage

### Run the GUI
```bash
python src/keystroke_app.py
```

### Main Functions:
* **Enroll Typing Profile**: Capture reference samples (3 recommended).
* **Verify Identity**: Compare a new typing sample with a stored profile.
* **Show DTW Analysis**: View DTW distances and the threshold line.

---

### 📷 Screenshots

> _Screenshots are stored in the [`docs/screenshots`](docs/screenshots/) directory._

---


### 📚 References
* [Dynamic Time Warping (Wikipedia)](https://en.wikipedia.org/wiki/Dynamic_time_warping)
* [Keyboard Python Library](https://pypi.org/project/keyboard/)
* [Matplotlib Documentation](https://matplotlib.org/stable/contents.html)

---

### 📜 License
This project is licensed under the MIT License – see the `LICENSE` file for details.

---

### 👨‍💻 Author
Mihoub Rahma

### 📧 Contact
mihoubrahma@gmail.com
