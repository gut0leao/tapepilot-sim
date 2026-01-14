# TapePilot – Transport & Capstan Simulator

TapePilot is a **visual and interactive simulator** for tape recorder transport systems,
focused on **capstan servo control**, **encoder feedback**, and **real-time fault injection**.

The simulator models physical components such as **reels**, **capstan**, **pinch roller**, and
**tape path** using **SVG-based mechanics**, while plotting control signals and system response
in real time.

This project serves as a **testbed for control strategies** before deploying them to
embedded hardware (e.g. Arduino / MCU).

---

## ✨ Features

- SVG-based visual representation of tape transport mechanics
- Animated reels, capstan, and tape path
- Transport controls (PLAY, STOP, FF, REW, PAUSE)
- Real-time tachometer feedback
- Live plots of:
  - RPM (setpoint vs measured)
  - Control output (PWM / torque)
  - Control error
  - Tape tension (simulated)
- Dynamic fault injection via sliders:
  - Tape friction
  - Encoder jitter / noise
  - (planned) encoder dropouts, slip, back-tension
- Designed for iterative experimentation and control tuning

---

## 🎯 Project Goals

- Simulate tape recorder transport mechanics with visual fidelity
- Experiment with capstan control strategies (PID and beyond)
- Observe tachometer behavior under disturbances
- Inject mechanical and sensing faults in real time
- Validate control logic before embedded deployment

---

## 🚫 Non-goals

- Audio signal processing or audio quality simulation
- Emulation of specific commercial tape recorder brands
- Hard real-time guarantees (this is a simulation environment)

---

## 🧠 Technical Overview

The project is structured around three loosely coupled layers:

1. **Physical model**
   - Capstan dynamics
   - Reel inertia
   - Tape tension and friction
2. **Control**
   - Encoder-based feedback
   - PID and experimental control laws
3. **Visualization & UI**
   - SVG-based mechanics (Qt Graphics Scene)
   - Real-time plots and operator controls

This separation allows the same control logic to be reused later in embedded firmware.

---

## 🛠️ Tech Stack

- **Python 3.12+**
- **PySide6 (Qt)** – GUI, SVG rendering, and animation
- **QtSvg** – SVG support
- **pyqtgraph** – real-time plotting
- **NumPy** – numerical modeling

---

## 🗂️ Project Structure

```
tapepilot-sim/
├─ assets/
│  └─ svg/              # Mechanical components (SVGs)
├─ sim/
│  ├─ plant.py          # Physical models
│  ├─ encoder.py        # Encoder simulation
│  ├─ controller.py     # Control algorithms
│  └─ faults.py         # Fault injection
├─ ui/
│  ├─ main_window.py    # Main Qt window
│  ├─ mechanics_scene.py# SVG mechanics scene
│  └─ plots.py          # Real-time plots
├─ app.py               # Application entry point
└─ README.md
```

---

## 💻 Platform Support

Tested on:

- **Windows 11**
  - WSL2
  - Ubuntu 24.04
  - WSLg (GUI support)

No external X server is required when using WSLg.

---

## 🚀 Getting Started (WSL / Ubuntu 24.04)

### 1. System dependencies

```bash
sudo apt update
sudo apt install -y python3 python3-venv python3-pip   libgl1 libegl1 libxkbcommon0 libxcb-cursor0   libxrender1 libxext6 libx11-6
```

### 2. Clone the repository

```bash
git clone https://github.com/gut0leao/tapepilot-sim.git
cd tapepilot-sim
```

### 3. Create a virtual environment

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -U pip
```

### 4. Install Python dependencies

```bash
pip install pyside6 pyqtgraph numpy
```

### 5. Run the simulator

```bash
python app.py
```

---

## 🎛️ Using the Simulator

- Use the **transport buttons** to change operating modes
- Adjust **fault sliders** to inject disturbances in real time
- Observe how the tachometer and control loop respond
- Monitor plots for stability, overshoot, and correction behavior

---

## 📦 SVG Assets Guidelines

- Each moving component should be a **separate SVG file**
  - Reels
  - Capstan
  - Pinch roller
- SVGs should have a clean `viewBox` with minimal margins
- Rotation pivots are defined programmatically from the SVG bounding box

SVGs can be created with tools such as Inkscape or Illustrator.

---

## 📜 License

This project is licensed under the **MIT License**.  
You are free to use, modify, and redistribute it, including for commercial purposes.

---

## 👤 Author

**Guto Leão**  
GitHub: https://github.com/gut0leao

---

## 🚧 Project Status

**Experimental / Work in Progress**

This project is under active development.
APIs, models, and visuals may change frequently.
