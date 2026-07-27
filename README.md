# ✋ GestureFlow

> **An AI-powered Hand Gesture Recognition System that transforms natural hand movements into intuitive computer interactions using Computer Vision and Machine Learning.**

<p align="center">

![Python](https://img.shields.io/badge/Python-3.10+-3776AB?style=for-the-badge&logo=python&logoColor=white)
![OpenCV](https://img.shields.io/badge/OpenCV-Computer%20Vision-5C3EE8?style=for-the-badge&logo=opencv&logoColor=white)
![MediaPipe](https://img.shields.io/badge/MediaPipe-Hand%20Tracking-FF6F00?style=for-the-badge)
![NumPy](https://img.shields.io/badge/NumPy-Numerical%20Computing-013243?style=for-the-badge&logo=numpy)
![Status](https://img.shields.io/badge/Status-Active%20Development-success?style=for-the-badge)
![License](https://img.shields.io/badge/License-MIT-blue?style=for-the-badge)

</p>

---

# ✨ Features

Current Features:

- 🎥 Real-time webcam integration
- ✋ MediaPipe-based hand landmark detection
- 🎯 Accurate 21-point hand tracking
- 🖱️ Air Mouse cursor control
- ⚡ Optimized cursor movement
- 🎚️ Dynamic cursor smoothing
- 🚫 Dead-zone filtering to reduce cursor jitter
- 📍 Screen coordinate mapping
- 📊 Real-time FPS monitoring
- 🤏 Thumb–Index pinch detection foundation
- 🧩 Modular architecture for future gesture expansion

---

# 📖 Project Overview

GestureFlow is an AI-powered Computer Vision project that enables users to control their computer using natural hand gestures.

Instead of relying on traditional input devices, GestureFlow uses MediaPipe to detect hand landmarks in real time and converts finger movements into cursor actions.

The project is designed with a modular architecture, making it easy to expand with additional gesture-controlled interactions like clicking, dragging, scrolling, and virtual drawing.

The goal is to build an efficient, scalable, and intuitive Human–Computer Interaction system while exploring practical applications of Artificial Intelligence and Computer Vision.

---

# 🛠️ Tech Stack

### Programming Language

- Python

### Computer Vision

- OpenCV
- MediaPipe

### Libraries

- NumPy
- PyAutoGUI

### Development Tools

- VS Code
- Git
- GitHub

---

# 📂 Project Structure

```text
GestureFlow/
│
├── src/
│   ├── camera/
│   │   └── camera_manager.py
│   │
│   ├── hand_tracking/
│   │   └── hand_detector.py
│   │
│   ├── gestures/
│   │   ├── __init__.py
│   │   ├── gesture_recognizer.py
│   │   └── gesture_utils.py
│   │
│   ├── mouse/
│   │   └── air_mouse.py
│   │
│   └── presentation/
│
├── main.py
├── requirements.txt
└── README.md
```

---

# 🚀 Installation

## 1. Clone the Repository

```bash
git clone https://github.com/BuiltByAdvait/GestureFlow.git
cd GestureFlow
```

---

## 2. Create a Virtual Environment

### Windows

```bash
python -m venv .venv
.venv\Scripts\activate
```

### macOS / Linux

```bash
python3 -m venv .venv
source .venv/bin/activate
```

---

## 3. Install Dependencies

```bash
pip install -r requirements.txt
```

---

## 4. Run GestureFlow

```bash
python main.py
```

---

# 🎮 Usage

1. Launch the application.
2. Allow webcam access.
3. Position your hand in front of the camera.
4. Move your index finger to control the mouse cursor.
5. Use the Thumb–Index pinch gesture (currently under development) for future click interactions.

---

# 📸 Screenshots

> Screenshots and demonstrations will be added as development progresses.

---

# 🔮 Future Roadmap

Planned Improvements:

- 🖱️ Left Click using Thumb–Index Pinch
- 🖱️ Right Click Gesture
- ✊ Drag & Drop Support
- 📜 Scroll Gesture
- 🎯 Gesture Debouncing
- 📏 Auto Cursor Calibration
- 🎨 Air Canvas
- ⚡ Performance Optimization
- 🤖 Advanced Gesture Recognition
- 🧠 Improved Gesture Stability
- ✨ Enhanced User Experience

---

# 🤝 Contributing

Contributions are welcome!

If you'd like to contribute:

1. Fork the repository.
2. Create a new feature branch.
3. Commit your changes.
4. Push your branch.
5. Open a Pull Request.

Please ensure your code follows clean coding practices and is well documented.

---

# 📄 License

This project is licensed under the **MIT License**.

Feel free to use, modify, and distribute this project under the terms of the MIT License.

---

# 👨‍💻 Author

## Advait Bankar

**GitHub**

https://github.com/BuiltByAdvait

**LinkedIn**

https://www.linkedin.com/in/advaitbankar

---

# ⭐ Support

If you enjoyed this project or found it useful:

- ⭐ Star this repository
- 🍴 Fork it
- 💡 Suggest new features
- 🤝 Contribute to the project

Your support motivates future development and continuous improvements.

---

<p align="center">

### 🚀 Building the Future of Human–Computer Interaction, One Gesture at a Time.

Made with ❤️ by **Advait Bankar**

</p>