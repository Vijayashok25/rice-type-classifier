import React, { useState, useEffect } from 'react';
import Navbar from './components/Navbar';
import ImageUploader from './components/ImageUploader';
import PredictionCard from './components/PredictionCard';
import HistoryTable from './components/HistoryTable';
import MetricsModal from './components/MetricsModal';

export default function App() {
  const [darkMode, setDarkMode] = useState(false);
  const [selectedFile, setSelectedFile] = useState(null);
  const [imagePreview, setImagePreview] = useState(null);
  const [loading, setLoading] = useState(false);
  const [prediction, setPrediction] = useState(null);
  const [error, setError] = useState(null);
  const [history, setHistory] = useState([]);
  const [historyLoading, setHistoryLoading] = useState(false);
  const [showMetrics, setShowMetrics] = useState(false);
  const [metricsData, setMetricsData] = useState(null);

  useEffect(() => {
    if (darkMode) {
      document.documentElement.classList.add('dark');
    } else {
      document.documentElement.classList.remove('dark');
    }
  }, [darkMode]);

  const fetchHistory = async () => {
    setHistoryLoading(true);
    try {
      const res = await fetch('/history');
      const data = await res.json();
      if (data.success) {
        setHistory(data.history);
      }
    } catch (err) {
      console.error("Failed to load prediction history", err);
    } finally {
      setHistoryLoading(false);
    }
  };

  useEffect(() => {
    fetchHistory();
  }, []);

  const handleFileChange = (file) => {
    if (!file) return;
    if (!file.type.startsWith('image/')) {
      setError("Please select a valid image file (JPG, PNG, WEBP).");
      return;
    }
    setError(null);
    setSelectedFile(file);
    setPrediction(null);

    const reader = new FileReader();
    reader.onloadend = () => {
      setImagePreview(reader.result);
    };
    reader.readAsDataURL(file);
  };

  const handleClassify = async () => {
    if (!selectedFile) return;
    setLoading(true);
    setError(null);

    const formData = new FormData();
    formData.append('image', selectedFile);

    try {
      const response = await fetch('/predict', {
        method: 'POST',
        body: formData,
      });
      const data = await response.json();

      if (response.ok && data.success) {
        setPrediction(data);
        fetchHistory();
      } else {
        setError(data.error || "Classification failed.");
      }
    } catch (err) {
      setError("Unable to connect to Flask REST API server.");
    } finally {
      setLoading(false);
    }
  };

  const handleClearHistory = async () => {
    if (!window.confirm("Are you sure you want to clear all prediction history?")) return;
    try {
      const res = await fetch('/history', { method: 'DELETE' });
      const data = await res.json();
      if (data.success) {
        setHistory([]);
      }
    } catch (err) {
      alert("Failed to clear history.");
    }
  };

  const handleOpenMetrics = async () => {
    try {
      const res = await fetch('/metrics');
      const data = await res.json();
      if (data.success) {
        setMetricsData(data);
        setShowMetrics(true);
      }
    } catch (err) {
      alert("Failed to fetch model metrics");
    }
  };

  const resetSelection = () => {
    setSelectedFile(null);
    setImagePreview(null);
    setPrediction(null);
    setError(null);
  };

  return (
    <div className="min-h-screen flex flex-col bg-slate-50 text-slate-800 dark:bg-slate-900 dark:text-slate-100 transition-colors duration-200">
      <Navbar 
        darkMode={darkMode} 
        setDarkMode={setDarkMode} 
        onOpenMetrics={handleOpenMetrics} 
      />

      <main className="flex-1 max-w-7xl w-full mx-auto p-6 space-y-8">
        <div className="grid grid-cols-1 lg:grid-cols-12 gap-6">
          <div className="lg:col-span-6">
            <ImageUploader 
              selectedFile={selectedFile}
              imagePreview={imagePreview}
              onFileChange={handleFileChange}
              onClassify={handleClassify}
              loading={loading}
              error={error}
              onReset={resetSelection}
            />
          </div>

          <div className="lg:col-span-6">
            <PredictionCard prediction={prediction} />
          </div>
        </div>

        <HistoryTable 
          history={history}
          loading={historyLoading}
          onClearHistory={handleClearHistory}
        />
      </main>

      <MetricsModal 
        show={showMetrics} 
        onClose={() => setShowMetrics(false)} 
        metricsData={metricsData} 
      />

      <footer className="border-t border-slate-200 dark:border-slate-800 py-4 px-6 text-center text-xs text-slate-400">
        Rice Type Classifier ML Project &bull; MobileNetV2 CNN &bull; Flask REST API &bull; SQLite &bull; React
      </footer>
    </div>
  );
}
