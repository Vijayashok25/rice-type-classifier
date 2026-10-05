import os
import sys
import json
import argparse
import random
import shutil
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from PIL import Image

import tensorflow as tf
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.applications import MobileNetV2
from tensorflow.keras.applications.mobilenet_v2 import preprocess_input
from tensorflow.keras.layers import Dense, GlobalAveragePooling2D, Dropout
from tensorflow.keras.models import Model, load_model
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.callbacks import ModelCheckpoint, EarlyStopping, ReduceLROnPlateau

from sklearn.metrics import classification_report, confusion_matrix

IMG_WIDTH, IMG_HEIGHT = 224, 224
IMG_SIZE = (IMG_WIDTH, IMG_HEIGHT)
CLASSES = ['Arborio', 'Basmati', 'Ipsala', 'Jasmine', 'Karacadag']
DEFAULT_DATASET_DIR = r'C:\Users\visha\OneDrive - vit.ac.in\children_analysis\Rice_Image_Dataset'

def create_sampled_dataset(source_dir, temp_dir, samples_per_class=1000):
    """
    Subsamples a balanced dataset for fast and efficient high-accuracy training.
    """
    print(f"\n[INFO] Staging balanced dataset in temporary folder '{temp_dir}'...")
    os.makedirs(temp_dir, exist_ok=True)
    
    total_copied = 0
    for cls in CLASSES:
        cls_src = os.path.join(source_dir, cls)
        cls_dst = os.path.join(temp_dir, cls)
        os.makedirs(cls_dst, exist_ok=True)
        
        if os.path.exists(cls_src):
            all_imgs = [f for f in os.listdir(cls_src) if f.lower().endswith(('.png', '.jpg', '.jpeg'))]
            if samples_per_class and samples_per_class < len(all_imgs):
                sampled = random.sample(all_imgs, samples_per_class)
            else:
                sampled = all_imgs
                
            for img in sampled:
                shutil.copy2(os.path.join(cls_src, img), os.path.join(cls_dst, img))
                total_copied += 1
                
            print(f" -> Class '{cls}': {len(sampled)} images staged.")
        else:
            print(f" [WARNING] Class folder '{cls_src}' not found.")
            
    print(f"[INFO] Total images staged for training: {total_copied}")
    return temp_dir

def build_mobilenet_model(num_classes=5, learning_rate=1e-4):
    """
    Builds MobileNetV2 Transfer Learning Model with ImageNet weights.
    """
    base_model = MobileNetV2(
        weights='imagenet',
        include_top=False,
        input_shape=(IMG_WIDTH, IMG_HEIGHT, 3)
    )
    
    # Freeze base model layers for feature extraction
    base_model.trainable = False
    
    x = base_model.output
    x = GlobalAveragePooling2D()(x)
    x = Dense(256, activation='relu')(x)
    x = Dropout(0.3)(x)
    outputs = Dense(num_classes, activation='softmax')(x)
    
    model = Model(inputs=base_model.input, outputs=outputs)
    model.compile(
        optimizer=Adam(learning_rate=learning_rate),
        loss='categorical_crossentropy',
        metrics=['accuracy']
    )
    return model, base_model

def evaluate_and_generate_reports(model, val_generator, output_model_dir):
    """
    Generates Confusion Matrix heatmap, Classification Report text file, and prints evaluation metrics.
    """
    print("\n[INFO] Evaluating model on validation set for Confusion Matrix & Classification Report...")
    val_generator.reset()
    predictions = model.predict(val_generator, verbose=1)
    y_pred = np.argmax(predictions, axis=1)
    y_true = val_generator.classes
    class_labels = list(val_generator.class_indices.keys())
    
    # Classification Report
    report = classification_report(y_true, y_pred, target_names=class_labels)
    print("\n" + "="*60)
    print("CLASSIFICATION REPORT")
    print("="*60)
    print(report)
    print("="*60)
    
    report_path = os.path.join(output_model_dir, 'classification_report.txt')
    with open(report_path, 'w') as f:
        f.write(report)
    print(f"[INFO] Saved Classification Report to '{report_path}'")
    
    # Confusion Matrix
    cm = confusion_matrix(y_true, y_pred)
    plt.figure(figsize=(8, 6))
    sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', xticklabels=class_labels, yticklabels=class_labels)
    plt.title('Rice Type Classifier - Confusion Matrix', fontsize=14, fontweight='bold', pad=15)
    plt.xlabel('Predicted Label', fontsize=12)
    plt.ylabel('True Label', fontsize=12)
    plt.tight_layout()
    
    cm_path = os.path.join(output_model_dir, 'confusion_matrix.png')
    plt.savefig(cm_path, dpi=300)
    plt.close()
    print(f"[INFO] Saved Confusion Matrix heatmap plot to '{cm_path}'")

def train_rice_classifier(data_dir=DEFAULT_DATASET_DIR, output_model_dir='model', epochs=15, batch_size=32, samples_per_class=1000):
    os.makedirs(output_model_dir, exist_ok=True)
    
    # Stage dataset if subsampling requested
    if samples_per_class and samples_per_class > 0:
        temp_dir = os.path.join(output_model_dir, 'temp_dataset')
        working_data_dir = create_sampled_dataset(data_dir, temp_dir, samples_per_class)
    else:
        working_data_dir = data_dir

    print("\n[INFO] Setting up Data Generators (80/20 Train/Val Split, Data Augmentation enabled)...")
    
    train_datagen = ImageDataGenerator(
        preprocessing_function=preprocess_input,
        validation_split=0.20,
        rotation_range=20,
        width_shift_range=0.1,
        height_shift_range=0.1,
        shear_range=0.1,
        zoom_range=0.15,
        horizontal_flip=True,
        brightness_range=[0.8, 1.2],
        fill_mode='nearest'
    )
    
    val_datagen = ImageDataGenerator(
        preprocessing_function=preprocess_input,
        validation_split=0.20
    )
    
    train_generator = train_datagen.flow_from_directory(
        working_data_dir,
        target_size=IMG_SIZE,
        batch_size=batch_size,
        class_mode='categorical',
        subset='training',
        shuffle=True
    )
    
    val_generator = val_datagen.flow_from_directory(
        working_data_dir,
        target_size=IMG_SIZE,
        batch_size=batch_size,
        class_mode='categorical',
        subset='validation',
        shuffle=False
    )
    
    # Save class indices mapping
    class_indices = train_generator.class_indices
    with open(os.path.join(output_model_dir, 'class_indices.json'), 'w') as f:
        json.dump(class_indices, f, indent=4)
    with open('class_indices.json', 'w') as f:
        json.dump(class_indices, f, indent=4)
        
    print(f"[INFO] Class Indices Mapping: {class_indices}")
    
    # Build Model
    model, base_model = build_mobilenet_model(num_classes=len(class_indices))
    
    model_path = os.path.join(output_model_dir, 'rice_classifier.h5')
    root_model_path = 'rice_classifier.h5'
    
    callbacks = [
        ModelCheckpoint(model_path, monitor='val_accuracy', save_best_only=True, verbose=1),
        EarlyStopping(monitor='val_loss', patience=4, restore_best_weights=True, verbose=1),
        ReduceLROnPlateau(monitor='val_loss', factor=0.5, patience=2, verbose=1)
    ]
    
    print("\n[INFO] Starting Transfer Learning Training with MobileNetV2...")
    history = model.fit(
        train_generator,
        epochs=epochs,
        validation_data=val_generator,
        callbacks=callbacks
    )
    
    # Save model to root directory as well
    if os.path.exists(model_path):
        shutil.copy2(model_path, root_model_path)
    else:
        model.save(model_path)
        model.save(root_model_path)
        
    print(f"\n[SUCCESS] Best model successfully saved to '{model_path}' and '{root_model_path}'")
    
    # Output Final Metrics Summary
    acc = history.history['accuracy']
    val_acc = history.history['val_accuracy']
    loss = history.history['loss']
    val_loss = history.history['val_loss']
    
    print("\n" + "="*50)
    print("FINAL TRAINING & VALIDATION METRICS")
    print("="*50)
    print(f"Final Training Accuracy   : {acc[-1]*100:.2f}%")
    print(f"Final Validation Accuracy : {val_acc[-1]*100:.2f}%")
    print(f"Best Validation Accuracy  : {max(val_acc)*100:.2f}%")
    print(f"Final Training Loss       : {loss[-1]:.4f}")
    print(f"Final Validation Loss     : {val_loss[-1]:.4f}")
    print("="*50)
    
    # Plot Accuracy and Loss Graphs
    plt.figure(figsize=(12, 5))
    
    plt.subplot(1, 2, 1)
    plt.plot(acc, label='Train Accuracy', color='#059669', linewidth=2.5)
    plt.plot(val_acc, label='Val Accuracy', color='#2563eb', linewidth=2.5)
    plt.title('MobileNetV2 Training vs Validation Accuracy', fontsize=12, fontweight='bold')
    plt.xlabel('Epochs')
    plt.ylabel('Accuracy')
    plt.grid(True, linestyle='--', alpha=0.5)
    plt.legend(loc='lower right')
    
    plt.subplot(1, 2, 2)
    plt.plot(loss, label='Train Loss', color='#dc2626', linewidth=2.5)
    plt.plot(val_loss, label='Val Loss', color='#d97706', linewidth=2.5)
    plt.title('MobileNetV2 Training vs Validation Loss', fontsize=12, fontweight='bold')
    plt.xlabel('Epochs')
    plt.ylabel('Loss')
    plt.grid(True, linestyle='--', alpha=0.5)
    plt.legend(loc='upper right')
    
    plt.tight_layout()
    plot_path = os.path.join(output_model_dir, 'accuracy_loss_plot.png')
    plt.savefig(plot_path, dpi=300)
    plt.close()
    print(f"[INFO] Saved Accuracy/Loss plot to '{plot_path}'")
    
    # Generate Confusion Matrix and Classification Report
    evaluate_and_generate_reports(model, val_generator, output_model_dir)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Train Rice Type Classifier CNN Model")
    parser.add_argument('--dataset', type=str, default=DEFAULT_DATASET_DIR, help='Path to dataset directory')
    parser.add_argument('--epochs', type=int, default=15, help='Number of training epochs')
    parser.add_argument('--batch-size', type=int, default=32, help='Batch size')
    parser.add_argument('--samples-per-class', type=int, default=1000, help='Subsample count per class (0 for full dataset)')
    parser.add_argument('--eval-only', action='store_true', help='Only evaluate existing model')
    args = parser.parse_args()
    
    if args.eval_only:
        model_file = 'model/rice_classifier.h5' if os.path.exists('model/rice_classifier.h5') else 'rice_classifier.h5'
        model = load_model(model_file)
        val_datagen = ImageDataGenerator(preprocessing_function=preprocess_input)
        val_generator = val_datagen.flow_from_directory(
            args.dataset,
            target_size=IMG_SIZE,
            batch_size=args.batch_size,
            class_mode='categorical',
            shuffle=False
        )
        evaluate_and_generate_reports(model, val_generator, 'model')
    else:
        train_rice_classifier(
            data_dir=args.dataset,
            epochs=args.epochs,
            batch_size=args.batch_size,
            samples_per_class=args.samples_per_class
        )
