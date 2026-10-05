import React, { useRef } from 'react';
import { Upload, Loader2 } from 'lucide-react';

export default function ImageUploader({ selectedFile, imagePreview, onFileChange, onClassify, loading, error, onReset }) {
  const fileInputRef = useRef(null);

  const handleDragOver = (e) => e.preventDefault();

  const handleDrop = (e) => {
    e.preventDefault();
    if (e.dataTransfer.files && e.dataTransfer.files[0]) {
      onFileChange(e.dataTransfer.files[0]);
    }
  };

  return (
    <div className="bg-white dark:bg-slate-800 rounded-2xl p-6 shadow-sm border border-slate-200/80 dark:border-slate-700/80 flex flex-col justify-between">
      <div>
        <h2 className="text-lg font-bold text-slate-800 dark:text-slate-100 mb-1">Upload Rice Image</h2>
        <p className="text-xs text-slate-500 dark:text-slate-400 mb-5">
          Select or drag an image of Arborio, Basmati, Ipsala, Jasmine, or Karacadag rice grain.
        </p>

        {/* Drop zone */}
        <div 
          onDragOver={handleDragOver}
          onDrop={handleDrop}
          onClick={() => fileInputRef.current?.click()}
          className={`border-2 border-dashed rounded-xl p-6 flex flex-col items-center justify-center cursor-pointer transition-all ${
            imagePreview 
              ? 'border-emerald-500 bg-emerald-50/20 dark:bg-emerald-950/20' 
              : 'border-slate-300 dark:border-slate-600 hover:border-emerald-400 hover:bg-slate-50 dark:hover:bg-slate-750'
          }`}
        >
          <input 
            type="file" 
            ref={fileInputRef}
            onChange={(e) => e.target.files[0] && onFileChange(e.target.files[0])}
            accept="image/*" 
            className="hidden" 
          />

          {imagePreview ? (
            <div className="w-full flex flex-col items-center">
              <img 
                src={imagePreview} 
                alt="Rice Grain Preview" 
                className="max-h-64 object-contain rounded-lg shadow-sm border border-slate-200 dark:border-slate-700" 
              />
              <p className="mt-3 text-xs font-medium text-emerald-600 dark:text-emerald-400">
                {selectedFile ? selectedFile.name : "Image Loaded"}
              </p>
            </div>
          ) : (
            <>
              <Upload className="w-10 h-10 text-emerald-500 mb-3" />
              <p className="text-sm font-semibold text-slate-700 dark:text-slate-300">
                Drag & drop your rice image here
              </p>
              <p className="text-xs text-slate-400 mt-1">
                Supports JPG, PNG, WEBP (Resized to 224x224 automatically)
              </p>
            </>
          )}
        </div>

        {error && (
          <div className="mt-4 p-3 bg-rose-50 dark:bg-rose-950/50 border border-rose-200 dark:border-rose-800 rounded-lg text-xs text-rose-600 dark:text-rose-300">
            {error}
          </div>
        )}
      </div>

      <div className="mt-6 flex items-center space-x-3">
        <button
          onClick={onClassify}
          disabled={!selectedFile || loading}
          className={`flex-1 py-3 px-4 rounded-xl font-bold text-sm text-white shadow-md transition-all flex items-center justify-center ${
            !selectedFile || loading
              ? 'bg-slate-300 dark:bg-slate-700 cursor-not-allowed opacity-70'
              : 'bg-emerald-600 hover:bg-emerald-700 active:scale-[0.98]'
          }`}
        >
          {loading ? (
            <>
              <Loader2 className="w-4 h-4 mr-2 animate-spin" /> Classifying Rice Grain...
            </>
          ) : (
            "Classify Rice Grain"
          )}
        </button>

        {imagePreview && (
          <button
            onClick={onReset}
            className="py-3 px-4 rounded-xl font-semibold text-xs text-slate-600 dark:text-slate-300 bg-slate-100 dark:bg-slate-700 hover:bg-slate-200 dark:hover:bg-slate-600"
          >
            Reset
          </button>
        )}
      </div>
    </div>
  );
}
