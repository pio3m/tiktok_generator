import React, { useState, useEffect } from 'react';
import { ClipLoader } from "react-spinners";

import { CheckCircle, Loader, Clock } from 'lucide-react';

export default function App() {
  const [question, setQuestion] = useState('');
  const [style, setStyle] = useState('retro, lata 90');
  const [category, setCategory] = useState('');
  const [activeTab, setActiveTab] = useState('basic');
  const [loading, setLoading] = useState(false);
  const [response, setResponse] = useState(null);
  const [elapsed, setElapsed] = useState(0);
  const [currentStep, setCurrentStep] = useState(0);

  const steps = [
    'Generating text',
    'Generating audio',
    'Generating images',
    'Compositing video',
    'Final export'
  ];

  useEffect(() => {
    let interval;
    if (loading) {
      setElapsed(0);
      interval = setInterval(() => {
        setElapsed((prev) => prev + 1);
      }, 1000);
    }
    return () => clearInterval(interval);
  }, [loading]);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setResponse(null);
    setCurrentStep(0);

    const payload = { question, style, category };

    const endpoint = 'http://localhost:5678/webhook-test/d6745df8-6e8c-4186-8ef1-73213526f7ad';

    try {
      const res = await fetch(endpoint, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(payload)
      });
      const data = await res.json();
      setResponse(data);
    } catch (err) {
      setResponse({ error: 'Błąd połączenia z backendem' });
    }

    setLoading(false);
  };

  return (
    <main className="min-h-screen bg-gray-100 text-gray-900 flex flex-col md:flex-row">
      {/* LEWA KOLUMNA */}
      <div className="basis-1/2 flex flex-col items-center justify-center relative p-8 bg-white">
        <img
          src="/logo.png" // Podmień na swoją ścieżkę do logo
          alt="QuizTok Logo"
          className="absolute top-8 left-8 w-40"
        />

     <div className="w-[250px] h-[500px] flex items-center justify-center shadow-2xl relative rounded-3xl overflow-hidden bg-black">
        <svg viewBox="0 0 250 500" xmlns="http://www.w3.org/2000/svg" className="absolute w-full h-full pointer-events-none">
          <rect rx="40" ry="40" width="250" height="500" fill="#000" />
          <circle cx="125" cy="20" r="6" fill="#555" /> {/* Kamera */}
          <rect x="110" y="12" width="30" height="4" rx="2" fill="#555" /> {/* Głośnik */}
        </svg>
        <div className="absolute top-8 left-0 right-0 bottom-8 flex items-center justify-center">
          <video
            src="/example.mp4"
            className="h-full w-full object-cover rounded-[30px]"
            controls
            playsInline
          />
        </div>
      </div>


      </div>

      {/* PRAWA KOLUMNA */}
      <div className="basis-1/2 bg-gray-50 p-10 flex flex-col">
        <button onClick={() => console.log('Back')} className="text-sm text-gray-500 mb-4 self-start">&larr; Back</button>

        <p className="text-sm mb-4 text-gray-600">Wprowadź pytanie i wygeneruj quiz video w kilka sekund.</p>

        {/* ZAKŁADKI */}
        <div className="flex mb-6 border border-gray-200 rounded overflow-hidden self-start">
          <button
            className={`px-4 py-2 text-sm font-medium ${activeTab === 'basic' ? 'bg-white text-orange-600' : 'bg-gray-200 text-gray-600'}`}
            onClick={() => setActiveTab('basic')}
          >
            Basic generator
          </button>
          <button
            className={`px-4 py-2 text-sm font-medium ${activeTab === 'advanced' ? 'bg-white text-orange-600' : 'bg-gray-200 text-gray-600'}`}
            onClick={() => setActiveTab('advanced')}
          >
            Advanced settings
          </button>
        </div>

        {/* FORMULARZ */}
        <form onSubmit={handleSubmit} className="space-y-4">
          <textarea
            className="w-full bg-white border border-gray-300 p-3 rounded shadow-sm resize-none"
            placeholder="Type your question here..."
            rows={4}
            value={question}
            onChange={(e) => setQuestion(e.target.value)}
            required
          />

          {activeTab === 'advanced' && (
            <>
              <input
                className="w-full bg-white border border-gray-300 p-2 rounded shadow-sm"
                placeholder="Style (e.g. retro, lata 90)"
                value={style}
                onChange={(e) => setStyle(e.target.value)}
              />
              <input
                className="w-full bg-white border border-gray-300 p-2 rounded shadow-sm"
                placeholder="Category"
                value={category}
                onChange={(e) => setCategory(e.target.value)}
              />
            </>
          )}

          <button type="submit" disabled={loading} className="w-full bg-gradient-to-r from-pink-500 to-orange-400 text-white p-3 rounded font-semibold hover:opacity-90 transition">
            {loading ? '⏳ Generating...' : '🎬 Create Now!'}
          </button>
        </form>

        {response && (
          <div className="bg-green-100 text-green-700 p-4 rounded mt-6">
            <pre className="text-sm whitespace-pre-wrap">{JSON.stringify(response, null, 2)}</pre>
          </div>
        )}
      </div>

      {/* PEŁNOEKRANOWY SPINNER */}
      {loading && (
        <div className="fixed inset-0 bg-black bg-opacity-80 flex flex-col justify-center items-center z-50">
          <ClipLoader color="#FF6B00" size={80} />
          <p className="text-white mt-4 text-lg font-semibold">Generuję wideo... proszę czekać</p>
          <p className="text-gray-300 text-sm mt-1">Czas: {elapsed}s</p>
        </div>
      )}
    </main>
  );
}
