# Real-Time Weapon Detection App

A real-time Computer Vision application built with **Streamlit** and **YOLOv8** that detects weapons in CCTV footage and sends instant alerts via **Telegram**.  
Designed to simulate an emergency response system that can notify operators when armed individuals are detected.

---

## Overview

This project leverages **deep learning (YOLOv8)** for weapon detection in real-time from different video sources (uploaded files, webcam, or RTSP streams).  

When a weapon is detected with sufficient confidence across a threshold of consecutive frames, the system:  
- Displays an **alert panel** styled like a command prompt.  
- Sends a **Telegram message** with detection details and location link.  
- Highlights detections in the video feed.  

This prototype demonstrates how AI-based video surveillance can support security systems and emergency operations.

---

## Features

- **Multiple video sources**: Upload MP4 files, use live webcam feed, or connect to RTSP streams.  
- **Real-time detection**: Uses YOLOv8 for accurate and fast predictions.  
- **Customizable thresholds**:  
  - Confidence threshold (0.1–1.0)  
  - Frame threshold (to reduce false positives).  
- **Command-prompt style alert panel**: Live updates of detection events.  
- **Telegram integration**: Instant alert messages with clickable Google Maps location link.  
- **Custom-trained YOLO model**: Fine-tuned to recognize weapons.  

---

## Data Sources

The model was trained on multiple datasets collected from kaggle, roboflow and using the Youtube-GDD dataset.
---

## Training Results

Model: **YOLOv8s** (Ultralytics)  
Epochs: **30**  
Training time: **~5.1 hours**  
GPU: **NVIDIA GeForce RTX 3050 Laptop GPU (4GB VRAM)**  

Validation results (on test set of 2074 images with 1886 instances):  

| Metric   | Score |
|----------|-------|
| Precision (P) | **0.856** |
| Recall (R)    | **0.748** |
| mAP@50        | **0.823** |
| mAP@50-95     | **0.604** |

**Interpretation:**  
- The model achieves **82.3% mAP@50**, which means it’s highly reliable in detecting weapons at an IoU of 0.5.  
- **60.4% mAP@50-95** shows it maintains decent performance across stricter IoU thresholds.  
- With high precision, the model produces fewer false alarms, making it suitable for real-time surveillance.  

---
