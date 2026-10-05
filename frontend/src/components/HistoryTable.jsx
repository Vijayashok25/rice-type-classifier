import React from 'react';
import { Trash2 } from 'lucide-react';

export default function HistoryTable({ history, loading, onClearHistory }) {
  return (
    <div className="bg-white dark:bg-slate-800 rounded-2xl p-6 shadow-sm border border-slate-200/80 dark:border-slate-700/80">
      <div className="flex flex-col sm:flex-row sm:items-center justify-between pb-4 border-b border-slate-100 dark:border-slate-700/80 mb-4 gap-4">
        <div>
          <h2 className="text-lg font-bold text-slate-800 dark:text-slate-100">Prediction History Dashboard</h2>
          <p className="text-xs text-slate-500 dark:text-slate-400">
            Every classification result is automatically saved into SQLite database (`backend/history.db`).
          </p>
        </div>

        <div className="flex items-center space-x-3">
          <span className="text-xs font-semibold px-3 py-1.5 bg-emerald-50 dark:bg-emerald-950 text-emerald-700 dark:text-emerald-300 rounded-lg border border-emerald-200 dark:border-emerald-800">
            Total Predictions: {history.length}
          </span>

          {history.length > 0 && (
            <button
              onClick={onClearHistory}
              className="px-3 py-1.5 text-xs font-semibold text-rose-600 dark:text-rose-400 bg-rose-50 dark:bg-rose-950/40 hover:bg-rose-100 dark:hover:bg-rose-900/50 rounded-lg border border-rose-200 dark:border-rose-800 flex items-center transition-colors"
            >
              <Trash2 className="w-4 h-4 mr-1.5" /> Clear History
            </button>
          )}
        </div>
      </div>

      {loading ? (
        <div className="py-8 text-center text-xs text-slate-400">Loading prediction history from SQLite...</div>
      ) : history.length === 0 ? (
        <div className="py-12 text-center text-xs text-slate-400">
          No prediction records found in SQLite database.
        </div>
      ) : (
        <div className="overflow-x-auto">
          <table className="w-full text-left border-collapse">
            <thead>
              <tr className="border-b border-slate-200 dark:border-slate-700 text-[11px] uppercase tracking-wider text-slate-400 font-semibold">
                <th className="py-3 px-4"># ID</th>
                <th className="py-3 px-4">Thumbnail</th>
                <th className="py-3 px-4">Filename</th>
                <th className="py-3 px-4">Predicted Variety</th>
                <th className="py-3 px-4">Confidence</th>
                <th className="py-3 px-4">Timestamp</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-slate-100 dark:divide-slate-700/50 text-xs text-slate-700 dark:text-slate-300">
              {history.map((row) => (
                <tr key={row.id} className="hover:bg-slate-50/60 dark:hover:bg-slate-750 transition-colors">
                  <td className="py-3 px-4 font-mono font-semibold text-slate-400">#{row.id}</td>
                  <td className="py-3 px-4">
                    {row.image_data ? (
                      <img src={row.image_data} alt="Thumbnail" className="w-10 h-10 object-cover rounded-md border border-slate-200 dark:border-slate-700" />
                    ) : (
                      <div className="w-10 h-10 bg-slate-100 dark:bg-slate-700 rounded-md flex items-center justify-center text-slate-400">N/A</div>
                    )}
                  </td>
                  <td className="py-3 px-4 font-medium max-w-[180px] truncate" title={row.filename}>
                    {row.filename}
                  </td>
                  <td className="py-3 px-4 font-bold text-emerald-600 dark:text-emerald-400">
                    {row.predicted_class}
                  </td>
                  <td className="py-3 px-4 font-semibold">
                    <span className="px-2.5 py-1 rounded-full text-[11px] bg-emerald-100 dark:bg-emerald-950 text-emerald-700 dark:text-emerald-300 border border-emerald-200 dark:border-emerald-800">
                      {row.confidence.toFixed(1)}%
                    </span>
                  </td>
                  <td className="py-3 px-4 text-slate-400 font-mono text-[11px]">{row.timestamp}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}
    </div>
  );
}
