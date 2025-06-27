import React, { useState } from 'react';

export default function App() {
  const [question, setQuestion] = useState('');
  const [style, setStyle] = useState('retro, lata 90');
  const [category, setCategory] = useState('');
  const [activeTab, setActiveTab] = useState('basic');
  const [loading, setLoading] = useState(false);
  const [response, setResponse] = useState(null);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setResponse(null);

    const payload = { question, style, category };
    console.log('Sending:', payload);
    setTimeout(() => {
      setResponse({ status: 'ok', ...payload });
      setLoading(false);
    }, 1500);
  };

  return (
    <main className="min-h-screen bg-gray-100 text-gray-900 flex flex-col md:flex-row">
      {/* LEWA KOLUMNA */}
      <div className="basis-1/2 flex flex-col items-center justify-center relative p-8 bg-white">
        <img
          src="/logo.png" // Podmień na ścieżkę do swojego logo
          alt="QuizTok Logo"
          className="absolute top-8 left-8 w-40"
        />
        <div className="w-[250px] h-[500px] rounded-3xl bg-black shadow-2xl flex items-center justify-center">
          <span className="text-white text-sm">Video preview</span>
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
    </main>
  );
}
