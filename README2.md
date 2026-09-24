# Air Canvas – GestureFlow

## Overview

Added an Air Canvas module to GestureFlow that allows users to draw on a virtual canvas using hand gestures detected through the webcam.

The Air Canvas works with the existing MediaPipe hand-tracking and gesture-recognition system.

---

## Branch

`sg-air_canvas`

---

## Files Added

### `src/canvas/air_canvas.py`

New Air Canvas module containing:

- Virtual white drawing canvas
- Finger-based drawing
- Color selection
- Brush size selection
- Eraser
- Clear canvas
- Save canvas as PNG
- Toolbar interaction
- Gesture-based mode switching

---

## File Modified

### `main.py`

Integrated the Air Canvas into the existing GestureFlow application.

The existing camera, hand detection, gesture recognition, and Air Mouse functionality were kept intact.

---

## Gesture Controls

| Gesture | Function |
|---|---|
| ☝️ ONE finger | Drawing mode |
| ✌️ TWO fingers | Toolbar selection mode |
| ✊ FIST | Stop drawing |

---

## Toolbar Features

The Air Canvas toolbar provides:

### Colors

- Red
- Blue
- Green
- Black

### Brush Sizes

- Small
- Medium
- Large

### Tools

- Eraser
- Clear
- Save

---

## Drawing System

The index fingertip is used as the drawing pointer.

MediaPipe landmark:

`8 = Index Finger Tip`

The fingertip coordinates are converted from normalized MediaPipe coordinates into pixel coordinates of the webcam frame.

Lines are drawn between the previous fingertip position and the current fingertip position using OpenCV.

---

## Eraser

The eraser uses the same fingertip movement system as drawing but draws white lines over the existing canvas.

The eraser has a larger size than the normal brushes for easier removal of drawings.

---

## Clear Canvas

The **CLEAR** toolbar option resets the entire canvas to white.

---

## Save Canvas

The **SAVE** toolbar option saves the current drawing as:

`air_canvas.png`

The save confirmation is displayed temporarily on the screen.

---

## Toolbar Selection

Toolbar interaction uses a combination of:

1. Two-finger gesture
2. Index fingertip positioning
3. Thumb-index pinch

The fingertip position is stored before the pinch so that the selected toolbar item remains accurate even if the fingertip moves slightly during the pinch.

---

## Existing Components Reused

The Air Canvas integrates with the existing GestureFlow components:

- `CameraManager`
- `HandDetector`
- `GestureRecognizer`
- MediaPipe hand landmarks
- OpenCV
- NumPy

The existing Air Mouse implementation was not replaced.

---

## Technologies

- Python
- OpenCV
- MediaPipe
- NumPy

---

## Implementation Flow

```text
Webcam
   ↓
CameraManager
   ↓
HandDetector
   ↓
MediaPipe Hand Landmarks
   ↓
GestureRecognizer
   ↓
AirCanvas
   ↓
Drawing / Toolbar / Eraser / Clear / Save