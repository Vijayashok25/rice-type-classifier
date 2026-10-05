import React from 'react';
import { Leaf, Sun, Moon, BarChart2 } from 'lucide-react';

export default function Navbar({ darkMode, setDarkMode, onOpenMetrics }) {
  return (
    <header className="sticky top-0 z-30 bg-white/90 dark:bg-slate-800/90 backdrop-blur border-b border-slate-200 dark:border-slate-700 px-6 py-4">
      <div className="max-w-7xl mx-auto flex items-center justify-between">
        <div className="flex items-center space-x-3">
          <div className="p-2 bg-emerald-100 dark:bg-emerald-950 rounded-xl">
            <Leaf className="w-6 h-6 text-emerald-600 dark:text-emerald-400" />
          </div>
          <div>
            <h1 className="text-xl font-bold bg-gradient-to-r from-emerald-600 to-teal-600 dark:from-emerald-400 dark:to-teal-400 bg-clip-text text-transparent">
              Rice Type Classifier
            </h1>
            <p className="text-xs text-slate-500 dark:text-slate-400 font-medium">
              MobileNetV2 Transfer Learning CNN Pipeline
            </p>
          </div>
        </div>

        <div className="flex items-center space-x-3">
          <button 
            onClick={onOpenMetrics}
            className="px-3.5 py-2 text-xs font-semibold text-slate-700 dark:text-slate-200 bg-slate-100 dark:bg-slate-700 hover:bg-slate-200 dark:hover:bg-slate-600 rounded-lg flex items-center transition-colors"
          >
            <BarChart2 className="w-4 h-4 mr-1.5" /> Model Metrics
          </button>

          <button 
            onClick={() => setDarkMode(!darkMode)}
            className="p-2 rounded-lg bg-slate-100 dark:bg-slate-700 hover:bg-slate-200 dark:hover:bg-slate-600 transition-colors"
            title="Toggle Light/Dark Mode"
          >
            {darkMode ? <Sun className="w-5 h-5 text-amber-500" /> : <Moon className="w-5 h-5 text-indigo-400" />}
          </button>
        </div>
      </div>
    </header>
  );
}
