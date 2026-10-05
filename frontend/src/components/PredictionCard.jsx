import React from 'react';
import { Leaf } from 'lucide-react';

export default function PredictionCard({ prediction }) {
  return (
    <div className="bg-white dark:bg-slate-800 rounded-2xl p-6 shadow-sm border border-slate-200/80 dark:border-slate-700/80 flex flex-col justify-between">
      <div>
        <h2 className="text-lg font-bold text-slate-800 dark:text-slate-100 mb-1">Classification Output</h2>
        <p className="text-xs text-slate-500 dark:text-slate-400 mb-5">
          Real-time MobileNetV2 CNN predicted rice variety & confidence score.
        </p>

        {prediction ? (
          <div className="space-y-6">
            {/* Class Badge */}
            <div className="p-5 bg-gradient-to-r from-emerald-500/10 to-teal-500/10 border border-emerald-500/20 rounded-xl flex items-center justify-between">
              <div>
                <span className="text-xs font-semibold uppercase tracking-wider text-emerald-600 dark:text-emerald-400">
                  Predicted Rice Variety
                </span>
                <h3 className="text-3xl font-extrabold text-slate-900 dark:text-white mt-0.5">
                  {prediction.predicted_class}
                </h3>
              </div>
              <div className="text-right">
                <span className="text-xs font-semibold text-slate-500 dark:text-slate-400">Confidence</span>
                <div className="text-2xl font-black text-emerald-600 dark:text-emerald-400">
                  {prediction.confidence.toFixed(1)}%
                </div>
              </div>
            </div>

            {/* Progress Bar */}
            <div>
              <div className="flex justify-between text-xs font-semibold text-slate-600 dark:text-slate-400 mb-1.5">
                <span>Certainty Score</span>
                <span>{prediction.confidence.toFixed(1)}%</span>
              </div>
              <div className="w-full bg-slate-100 dark:bg-slate-700 h-3 rounded-full overflow-hidden">
                <div 
                  className="bg-emerald-500 h-full rounded-full transition-all duration-500 ease-out" 
                  style={{ width: `${prediction.confidence}%` }}
                />
              </div>
            </div>

            {/* Probabilities */}
            <div>
              <h4 className="text-xs font-bold text-slate-700 dark:text-slate-300 uppercase tracking-wider mb-3">
                Class Probabilities Breakdown
              </h4>
              <div className="space-y-2.5">
                {Object.entries(prediction.probabilities || {}).map(([cls, prob]) => (
                  <div key={cls} className="flex items-center text-xs">
                    <span className="w-24 font-semibold text-slate-700 dark:text-slate-300">{cls}</span>
                    <div className="flex-1 bg-slate-100 dark:bg-slate-700 h-2 rounded-full overflow-hidden mx-3">
                      <div 
                        className={`h-full rounded-full transition-all duration-500 ${
                          cls === prediction.predicted_class ? 'bg-emerald-500' : 'bg-slate-300 dark:bg-slate-600'
                        }`} 
                        style={{ width: `${prob}%` }}
                      />
                    </div>
                    <span className="w-12 text-right font-mono font-medium text-slate-600 dark:text-slate-400">
                      {prob.toFixed(1)}%
                    </span>
                  </div>
                ))}
              </div>
            </div>
          </div>
        ) : (
          <div className="h-64 border border-dashed border-slate-200 dark:border-slate-700 rounded-xl flex flex-col items-center justify-center text-center p-6 text-slate-400">
            <Leaf className="w-8 h-8 text-slate-300 dark:text-slate-600" />
            <p className="mt-2 text-sm font-semibold text-slate-500 dark:text-slate-400">No Classification Result</p>
            <p className="text-xs text-slate-400 mt-1 max-w-xs">
              Upload an image on the left panel and click "Classify Rice Grain" to run prediction.
            </p>
          </div>
        )}
      </div>
    </div>
  );
}
