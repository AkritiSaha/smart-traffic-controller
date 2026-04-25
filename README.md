# 🚦 Smart Traffic Light Controller

> An AI-based traffic light system that changes signals based on vehicle density — built as part of a Smart City AI internship project.

---

## 📌 What It Does

- 📷 **Uses camera or dummy input** to get vehicle count per lane
- 🧠 **AI Rule Engine** prioritizes the busiest lane for green signal
- 🚦 **Simulates signal switching** in real-time across 4 lanes (North, South, East, West)

---

## 🧠 How the AI Logic Works

```
Vehicle Count (Camera / Dummy)
        ↓
AI Rule Engine
priority_score = vehicle_count × 1.5
        ↓
Sort lanes: Highest score → gets GREEN first
        ↓
Green Time = proportional to traffic load (10s – 45s)
        ↓
Signal switches lane by lane
```

---

## 🗂️ Project Structure

```
smart-traffic-controller/
├── traffic_controller.py   # Main AI logic + simulation
├── requirements.txt        # Dependencies
└── README.md
```

---

## 🚀 How to Run

**1. Clone the repository**
```bash
git clone https://github.com/YOUR_USERNAME/smart-traffic-controller.git
cd smart-traffic-controller
```

**2. Install dependencies**
```bash
pip install opencv-python
```

**3. Run the program**
```bash
python traffic_controller.py
```

**4. Choose input mode:**
```
1 → Dummy Input  (simulated vehicle counts — no camera needed)
2 → Camera Input (OpenCV webcam detection)
```

---

## 📟 Sample Output

```
=======================================================
  🏙️  SMART TRAFFIC LIGHT CONTROLLER
  Mode: Dummy Input
=======================================================

  CYCLE 1 of 3
─────────────────────────────────────────────

  📷 STEP 1: Reading Vehicle Counts...
  North   : ████████████░░░░░░░░░░░░░░░░░░ 12 vehicles
  South   : ██████████████████████░░░░░░░░ 22 vehicles
  East    : █████████████████████████░░░░░ 25 vehicles
  West    : ███████░░░░░░░░░░░░░░░░░░░░░░░ 7 vehicles

  🧠 STEP 2: AI Rule Engine Computing Priority...

  Priority Queue (High → Low):
    #1  East     → Score: 37.5
    #2  South    → Score: 33.0
    #3  North    → Score: 18.0
    #4  West     → Score: 10.5

  🚦 SIGNAL SWITCHING SIMULATION
  ─────────────────────────────
  ⏱  Priority #1 → East Lane | Green Time: 40s

    East     → 🟢 GREEN
    South    → 🔴 RED
    North    → 🔴 RED
    West     → 🔴 RED

  ✅ 13 vehicles cleared from East lane
```

---

## 🧪 Concepts Demonstrated

| Concept | How |
|---|---|
| AI Rule Engine | Priority score formula based on vehicle density |
| Reinforcement Logic | Busiest lane always served first |
| OpenCV Detection | Camera-based vehicle counting using background subtraction |
| Simulation I/O | Terminal-based real-time signal switching |
| Smart City AI | Traffic management automation |

---

## 📦 Requirements

```
opencv-python
```
Install: `pip install opencv-python`

> Dummy mode works with no dependencies at all (pure Python).

---

## 👩‍💻 About

Built as an internship project exploring **AI in Smart City use-cases** — specifically traffic management and automation using rule-based AI and computer vision.
