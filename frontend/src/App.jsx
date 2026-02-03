import { useState } from 'react';
import { summarizeVideo } from './api';

function App() {
  // 1. State Variables
  const [url, setUrl] = useState('');
  const [loading, setLoading] = useState(false);
  const [data, setData] = useState(null);
  const [error, setError] = useState('');

  // 2. Search Handler
  const handleSearch = async () => {
    if (!url) return;
    
    setLoading(true);
    setError('');
    setData(null);
    
    try {
      const result = await summarizeVideo(url);
      setData(result);
    } catch (err) {
      console.error(err);
      setError("Failed to fetch summary. Check if the Backend is running!");
    } finally {
      setLoading(false);
    }
  };

  // 3. The Visuals
  return (
    <div className="min-h-screen bg-gray-50 p-8 font-sans">
      <div className="max-w-2xl mx-auto">
        <h1 className="text-4xl font-bold text-center text-blue-600 mb-8">
          TubeMind 
        </h1>

        {/* --- INPUT SECTION --- */}
        <div className="flex gap-2 mb-8 shadow-sm">
          <input 
            type="text" 
            placeholder="Paste YouTube URL..." 
            className="flex-1 p-3 rounded-l-lg border border-gray-300 focus:outline-none focus:ring-2 focus:ring-blue-500"
            
            //  THIS ALLOWS TYPING/PASTING
            value={url}
            onChange={(e) => setUrl(e.target.value)}
          />
          
          <button 
            onClick={handleSearch}
            disabled={loading}
            className="bg-blue-600 text-white px-6 py-3 rounded-r-lg font-bold hover:bg-blue-700 disabled:bg-gray-400"
          >
            {loading ? 'Thinking...' : 'Summarize'}
          </button>
        </div>

        {/* --- ERROR MESSAGE --- */}
        {error && (
          <div className="bg-red-100 text-red-700 p-3 rounded-lg mb-6 border-l-4 border-red-500">
            {error}
          </div>
        )}

        {/* --- RESULT CARD --- */}
        {data && (
          <div className="bg-white rounded-lg shadow-md overflow-hidden animate-fade-in">
            {/* Header */}
            <div className="p-4 border-b border-gray-100 flex flex-col md:flex-row gap-4 bg-gray-50">
              {data.thumbnail_url && (
                <img 
                  src={data.thumbnail_url} 
                  alt="Thumbnail" 
                  className="w-full md:w-32 h-auto object-cover rounded border border-gray-200" 
                />
              )}
              <div className="flex-1">
                <h2 className="text-xl font-bold text-gray-800 leading-tight mb-2">
                  {data.title}
                </h2>
                <span className={`inline-block px-2 py-1 rounded text-xs font-bold uppercase tracking-wide ${data.source === 'database' ? 'bg-green-100 text-green-700' : 'bg-blue-100 text-blue-700'}`}>
                  {data.source === 'database' ? ' From Memory' : ' AI Generated'}
                </span>
              </div>
            </div>

            {/* Summary Text */}
            <div className="p-6">
              <h3 className="font-bold text-gray-400 uppercase text-xs tracking-wider mb-3">
                Key Takeaways
              </h3>
              <div className="prose text-gray-700 whitespace-pre-line leading-relaxed">
                {data.summary}
              </div>
            </div>
          </div>
        )}
      </div>
    </div>
  );
}

export default App;