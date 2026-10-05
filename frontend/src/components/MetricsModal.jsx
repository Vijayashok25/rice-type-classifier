import React from 'react';
import { X } from 'lucide-react';

export default function MetricsModal({ show, onClose, metricsData }) {
  if (!show) return null;

  return (
    <div className="fixed inset-0 z-50 bg-slate-900/60 backdrop-blur-sm flex items-center justify-center p-4">
      <div className="bg-white dark:bg-slate-800 rounded-2xl max-w-4xl w-full max-h-[90vh] overflow-y-auto p-6 shadow-2xl border border-slate-200 dark:border-slate-700">
        <div className="flex items-center justify-between pb-4 border-b border-slate-100 dark:border-slate-700 mb-6">
          <div>
            <h3 className="text-lg font-bold text-slate-800 dark:text-slate-100">Model Evaluation & Training Metrics</h3>
            <p className="text-xs text-slate-500 dark:text-slate-400">MobileNetV2 CNN Model Performance & Evaluation Plots</p>
          </div>
          <button 
            onClick={onClose}
            className="p-2 rounded-lg text-slate-400 hover:text-slate-600 dark:hover:text-slate-200 bg-slate-100 dark:bg-slate-700"
          >
            <X className="w-5 h-5" />
          </button>
        </div>

        <div className="space-y-6">
          {/* Plots */}
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div className="bg-slate-50 dark:bg-slate-900 p-4 rounded-xl border border-slate-200 dark:border-slate-700">
              <h4 className="text-xs font-bold text-slate-700 dark:text-slate-300 uppercase mb-3">Training Accuracy & Loss Plot</h4>
              {metricsData?.has_accuracy_loss_plot ? (
                <img src="/model-files/accuracy_loss_plot.png" alt="Accuracy Loss Plot" className="w-full rounded-lg shadow-sm" />
              ) : (
                <p className="text-xs text-slate-400 py-8 text-center">Plot not generated yet. Run train.py to generate.</p>
              )}
            </div>

            <div className="bg-slate-50 dark:bg-slate-900 p-4 rounded-xl border border-slate-200 dark:border-slate-700">
              <h4 className="text-xs font-bold text-slate-700 dark:text-slate-300 uppercase mb-3">Confusion Matrix Heatmap</h4>
              {metricsData?.has_confusion_matrix ? (
                <img src="/model-files/confusion_matrix.png" alt="Confusion Matrix" className="w-full rounded-lg shadow-sm" />
              ) : (
                <p className="text-xs text-slate-400 py-8 text-center">Matrix plot not generated yet. Run train.py to generate.</p>
              )}
            </div>
          </div>

          {/* Classification Report */}
          <div className="bg-slate-900 text-slate-200 p-4 rounded-xl font-mono text-xs overflow-x-auto">
            <h4 className="text-[11px] uppercase tracking-wider text-emerald-400 font-bold mb-2">Classification Report</h4>
            <pre className="whitespace-pre-wrap">{metricsData?.classification_report || "No classification report text found."}</pre>
          </div>
        </div>
      </div>
    </div>
  );
}
