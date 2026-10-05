# Rice Type Classifier — End-to-End Machine Learning Project

Production-ready Machine Learning web application that classifies 5 varieties of rice grains (**Arborio**, **Basmati**, **Ipsala**, **Jasmine**, **Karacadag**) using transfer learning with **MobileNetV2 CNN**, a **Flask REST API**, **SQLite** prediction database, and an interactive **React UI** dashboard with dark/light mode toggle.

---

## 🌾 Features

1. **Rice Grain Image Upload & Preview**: Drag-and-drop or select an image file (`JPG`, `PNG`, `WEBP`) with instantaneous UI preview.
2. **CNN Model Classification**: High-accuracy deep learning classification powered by MobileNetV2 pretrained on ImageNet.
3. **Rich Results Display**: Shows predicted rice class, percentage confidence score, and full class probability breakdown bar graph.
4. **SQLite Prediction History**: Every prediction is automatically logged into an SQLite database (`backend/history.db`) with timestamp and thumbnail base64 data.
5. **Interactive Dashboard**: View prediction history, filter count, and clear history on demand.
6. **Model Metrics Modal**: Displays generated Training vs Validation Accuracy/Loss curves, Confusion Matrix heatmap, and Classification Report.
7. **Clean Agricultural / Medical UI**: Modern responsive design with persistent Light/Dark mode toggler.

---

## 📁 Project Structure

```
Rice_Type_Classifier/
├── frontend/                  # React Frontend Application
│   ├── public/
│   │   └── index.html         # Standalone React 18 Single-Page UI (No Node required)
│   ├── src/
│   │   ├── components/        # React Components (Navbar, Uploader, Cards, History Table, Metrics)
│   │   │   ├── Navbar.jsx
│   │   │   ├── ImageUploader.jsx
│   │   │   ├── PredictionCard.jsx
│   │   │   ├── HistoryTable.jsx
│   │   │   └── MetricsModal.jsx
│   │   ├── App.jsx            # Main React Entrypoint
│   │   └── index.css          # Tailwind CSS styles
│   └── package.json           # React npm configuration
│
├── backend/                   # Flask REST API & SQLite Database
│   ├── db.py                  # SQLite helper functions (init, insert, fetch, delete)
│   └── history.db             # SQLite database file
│
├── model/                     # Machine Learning Artifacts
│   ├── rice_classifier.h5     # Trained Keras MobileNetV2 Model
│   ├── class_indices.json     # Class name mapping dictionary
│   ├── accuracy_loss_plot.png # Training metrics evaluation curve
│   ├── confusion_matrix.png   # Confusion Matrix Heatmap
│   └── classification_report.txt # Scikit-Learn Classification Report
│
├── dataset/                   # Dataset reference directory
├── train.py                   # Model training & evaluation pipeline script
├── predict.py                 # Standalone prediction module & CLI test tool
├── app.py                     # Main Flask REST API application server
├── requirements.txt           # Python package dependencies
└── README.md                  # Project documentation
```

---

## 🚀 Quick Start Guide

### 1. Prerequisites & Environment Setup

Ensure Python 3.10+ is installed on your system.

Install all required Python dependencies:
```bash
pip install -r requirements.txt
```

---

### 2. Machine Learning Model Training (Optional / Evaluation)

To train a new MobileNetV2 CNN model on the dataset or re-generate evaluation curves, run:
```bash
python train.py --epochs 15 --samples-per-class 1000
```

* `--samples-per-class 1000`: Stages a balanced 5,000 image dataset for fast training with 98%+ validation accuracy.
* `--dataset "path/to/dataset"`: Pass custom dataset directory if stored in a different location.
* `--eval-only`: Evaluates pre-trained model and generates confusion matrix & classification report without retraining.

---

### 3. Run Standalone CLI Prediction Test

Test model classification directly from command line on any sample rice grain image:
```bash
python predict.py --image "C:\Users\visha\OneDrive - vit.ac.in\children_analysis\Rice_Image_Dataset\Basmati\Basmati (1).jpg"
```

---

### 4. Launch Flask REST API Server & Web UI

Start the Flask REST server:
```bash
python app.py
```

Then open your browser at:
👉 **[http://127.0.0.1:5000/](http://127.0.0.1:5000/)**

---

## 🔌 Backend REST API Specification

| Method | Endpoint | Description | Request Payload | Response |
| :--- | :--- | :--- | :--- | :--- |
| `POST` | `/predict` | Classify image & store in SQLite | `multipart/form-data` with `image` file | `{ success, predicted_class, confidence, probabilities, id, timestamp, image_data }` |
| `GET` | `/history` | Fetch prediction history | None | `{ success, count, class_distribution, history: [...] }` |
| `DELETE` | `/history` | Clear SQLite prediction history | None | `{ success, message }` |
| `GET` | `/metrics` | View training curves & report | None | `{ success, classification_report, has_accuracy_loss_plot, has_confusion_matrix }` |
| `GET` | `/health` | API health check | None | `{ status: "online", classes: [...] }` |

---

## 🧠 ML Architecture & Training Details

- **Base Architecture**: Pre-trained `MobileNetV2` (ImageNet weights) with base layers frozen for transfer learning feature extraction.
- **Top Layers**: `GlobalAveragePooling2D` $\rightarrow$ `Dense(256, ReLU)` $\rightarrow$ `Dropout(0.3)` $\rightarrow$ `Dense(5, Softmax)`.
- **Image Resolution**: $224 \times 224 \times 3$ RGB.
- **Preprocessing**: `preprocess_input` (MobileNetV2 scaling to $[-1, 1]$ range).
- **Augmentation**: Rotation ($20^\circ$), width/height shift ($10\%$), zoom ($15\%$), shear ($10\%$), horizontal flip, brightness adjustment ($[0.8, 1.2]$).
- **Callbacks**: `ModelCheckpoint` (saves best validation accuracy model), `EarlyStopping` (patience 4), `ReduceLROnPlateau` (patience 2).
