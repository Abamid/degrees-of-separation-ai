# 🎬 Degrees of Separation AI App

[![Streamlit App](https://img.shields.io/badge/Live%20Demo-Streamlit-success?logo=streamlit)](https://degrees-of-separation-ai-2stbrykxkyz4wvyxlfuchq.streamlit.app/)
[![Made with Python](https://img.shields.io/badge/Made%20with-Python-3776AB?logo=python)](https://www.python.org/)
[![License](https://img.shields.io/badge/License-MIT-blue.svg)](#license)

---

## 💡 Project Overview

**Degrees of Separation AI** is an interactive web application that helps users discover how two actors are connected through shared movie roles — applying graph search (BFS) on real-world movie-actor data.

Built with **Python**, powered by **Streamlit**, and hosted on the cloud, this project is ideal for demonstrating AI search logic, graph theory, and app deployment skills.

---

## 🔍 Features

- 🔗 Find the shortest path (degrees) between two movie stars  
- 📂 Uses real-world CSV datasets (`people`, `movies`, `stars`)  
- 🧠 Implements Breadth-First Search (BFS) under the hood  
- ⚡️ Instant results, clean interface  
- ☁️ Fully deployed via Streamlit Cloud  

---

## 🚀 Live Demo

👉 **Try it now:**  
🔗 [https://degrees-of-separation-ai-2stbrykxkyz4wvyxlfuchq.streamlit.app/](https://degrees-of-separation-ai-2stbrykxkyz4wvyxlfuchq.streamlit.app/)

---

## 🧪 How It Works

1. User inputs two actor names.  
2. App uses BFS to find the shortest co-star path via shared movies.  
3. Results are displayed step-by-step with movie titles and actors.

---

## 📁 Project Structure

```
degrees-of-separation-ai/
│
├── streamlit_app.py        # Main Streamlit app logic
├── requirements.txt        # App dependencies
├── README.md               # Project documentation
└── small/                  # Sample dataset folder
    ├── people.csv
    ├── movies.csv
    └── stars.csv
```

---

## 🛠 Installation (Local Run)

1. **Clone this repo:**

```bash
git clone https://github.com/Abamid/degrees-of-separation-ai.git
cd degrees-of-separation-ai
```

2. **Create virtual environment & install dependencies:**

```bash
pip install -r requirements.txt
```

3. **Run the app:**

```bash
streamlit run streamlit_app.py
```

---

## 🧰 Technologies Used

- Python 3.10+
- Streamlit
- Pandas
- Graph/BFS Search Algorithm
- CSV Dataset Manipulation

---

## 🤝 Contributions

Contributions, feedback, and issues are welcome!  
Fork the repo, open a pull request, or create an issue.

---

## 📄 License

This project is licensed under the MIT License.

---

## 👤 About the Developer

**Abubakar Amidu**  
Geologist | Data Scientist | AI Explorer  
📧 Email: abubakaramidu@gmail.com  

If you like this project, give it a ⭐ and share it with your community!
