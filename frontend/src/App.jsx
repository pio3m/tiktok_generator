import React, { useState } from 'react';
import { CheckCircle, Loader, Clock } from 'lucide-react';

export default function App() {
  const [question, setQuestion] = useState('');
  const [style, setStyle] = useState('retro, lata 90');
  const [category, setCategory] = useState('');
  const [loading, setLoading] = useState(false);
  const [response, setResponse] = useState(null);
  const [advanced, setAdvanced] = useState(false);
  const [boost, setBoost] = useState(false);
  const [currentStep, setCurrentStep] = useState(0);

  const steps = [
    'Generating text',
    'Generating audio',
    'Generating images',
    'Compositing video',
    'Final export'
  ];

  const [params, setParams] = useState({
    pause_after_intro: 0.5,
    question_fadein: 0.5,
    pause_after_question: 0.5,
    answers_fadein: 0.5,
    delay_between_answers: 0.3,
    pause_after_answers: 0.8,
    countdown_gap: 1.0,
    highlight_delay: 0.5,
    highlight_duration: 3
  });

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setResponse(null);
    setCurrentStep(0);

    const payload = {
      question,
      style,
      category
    };

    if (advanced) payload.timings = params;

    const endpoint = boost
      ? 'http://localhost:5678/webhook-test/boost-mode-id'
      : 'http://localhost:5678/webhook-test/d6745df8-6e8c-4186-8ef1-73213526f7ad';

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
    <main className="min-h-screen bg-black text-white p-6 flex justify-center items-start">
      <div className="w-full max-w-4xl grid grid-cols-1 md:grid-cols-2 gap-6">
        <form onSubmit={handleSubmit} className="space-y-3">
          <h1 className="text-2xl font-bold mb-2">QuizTok Engine</h1>

          <input
            className="w-full bg-gray-900 border border-gray-700 p-2 rounded"
            placeholder="Question"
            value={question}
            onChange={(e) => setQuestion(e.target.value)}
            required
          />

          <input
            className="w-full bg-gray-900 border border-gray-700 p-2 rounded"
            placeholder="Style (e.g. retro, lata 90)"
            value={style}
            onChange={(e) => setStyle(e.target.value)}
          />

          <input
            className="w-full bg-gray-900 border border-gray-700 p-2 rounded"
            placeholder="Category"
            value={category}
            onChange={(e) => setCategory(e.target.value)}
          />

          <div className="flex items-center space-x-4 text-sm mt-2">
            <label className="inline-flex items-center">
              <input type="checkbox" checked={advanced} onChange={() => setAdvanced(!advanced)} className="form-checkbox" />
              <span className="ml-2">Advanced Mode</span>
            </label>
            <label className="inline-flex items-center">
              <input type="checkbox" checked={boost} onChange={() => setBoost(!boost)} className="form-checkbox" />
              <span className="ml-2">Super Boost Mode</span>
            </label>
          </div>

          {advanced && (
            <div className="bg-gray-800 p-4 rounded mt-2 space-y-2 text-sm">
              <p className="font-medium mb-1">Render Parameters</p>
              {Object.entries(params).map(([key, value]) => (
                <div key={key}>
                  <label>{key}</label>
                  <input
                    type="range"
                    min="0"
                    max="5"
                    step="0.1"
                    value={value}
                    onChange={(e) => setParams({ ...params, [key]: parseFloat(e.target.value) })}
                    className="w-full"
                  />
                  <span className="text-xs">{value}s</span>
                </div>
              ))}
            </div>
          )}

          <button type="submit" disabled={loading} className="w-full bg-white text-black p-2 rounded font-semibold mt-4 hover:bg-gray-300">
            {loading ? '⏳ Generuję...' : '🎬 Generate'}
          </button>
        </form>

        <div>
          <h2 className="text-lg font-semibold mb-2">Status</h2>
          <ul className="space-y-3 mb-4">
            {steps.map((label, i) => {
              let Icon = Clock;
              let color = 'text-gray-500';

              if (i < currentStep) {
                Icon = CheckCircle;
                color = 'text-green-400';
              } else if (i === currentStep) {
                Icon = Loader;
                color = 'text-orange-400 ';
              }

              return (
                <li key={i} className={`flex items-center space-x-2 ${color}`}>
                  <Icon className="animate-spin" size={18} />
                  <span className="text-sm ">{label}</span>
                </li>
              );
            })}
          </ul>

          <div className="bg-gray-800 aspect-video rounded flex items-center justify-center text-gray-500">Video preview</div>
          <div className="flex space-x-3 mt-4">
            <button className="bg-gray-700 px-4 py-2 rounded hover:bg-gray-600">Download</button>
            <button className="bg-gray-700 px-4 py-2 rounded hover:bg-gray-600">Generate Again</button>
          </div>
        </div>
      </div>
    </main>
  );
}
