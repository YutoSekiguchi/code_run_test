import { useState, useEffect } from 'react';
import { Play, Save, Download, Upload, Settings, User, Code, Terminal } from 'lucide-react';

const LANGUAGES = {
  python: 'Python',
  javascript: 'JavaScript',
  ruby: 'Ruby',
  php: 'PHP',
  c: 'C',
  cpp: 'C++',
  java: 'Java',
  csharp: 'C#'
} as const;

type Language = keyof typeof LANGUAGES;

export default function App() {
  const [language, setLanguage] = useState<Language>('python');
  const [code, setCode] = useState('');
  const [output, setOutput] = useState('');
  const [isRunning, setIsRunning] = useState(false);

  useEffect(() => {
    loadTemplate('python');
  }, []);

  const loadTemplate = async (selectedLanguage: Language) => {
    try {
      const response = await fetch(`http://localhost:8000/template/${selectedLanguage}`);
      if (response.ok) {
        const template = await response.text();
        setCode(template);
      }
    } catch (error) {
      console.error('Failed to load template:', error);
    }
  };

  const handleLanguageChange = (newLanguage: Language) => {
    setLanguage(newLanguage);
    loadTemplate(newLanguage);
  };

  const runCode = async () => {
    setIsRunning(true);
    setOutput('');
   
    try {
      const response = await fetch('http://localhost:8000/', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/x-www-form-urlencoded',
        },
        body: new URLSearchParams({
          language,
          code,
          deps: ''
        })
      });
     
      const result = await response.text();
      setOutput(result);
    } catch (error) {
      setOutput(`Error: ${error instanceof Error ? error.message : 'Unknown error'}`);
    } finally {
      setIsRunning(false);
    }
  };

  return (
    <div className="h-screen flex flex-col bg-gray-50 p-4">
      {/* Header */}
      <header className="bg-white shadow-sm border-b border-gray-200 flex-shrink-0 rounded-t-lg">
        <div className="container mx-auto px-6 py-3">
          <div className="flex items-center justify-between">
            <div className="flex items-center space-x-3">
              <div className="w-8 h-8 bg-gradient-to-r from-blue-500 to-purple-500 rounded-lg flex items-center justify-center">
                <Code className="w-5 h-5 text-white" />
              </div>
              <div>
                <h1 className="text-lg font-bold text-gray-900">CodeTrack</h1>
              </div>
            </div>
            <div className="flex items-center space-x-4">
              <div className="flex items-center space-x-2 text-gray-700 text-sm">
                <User className="w-4 h-4" />
                <span>田中 太郎</span>
              </div>
              <button className="p-1 hover:bg-gray-100 rounded-lg transition-colors">
                <Settings className="w-4 h-4 text-gray-600" />
              </button>
            </div>
          </div>
        </div>
      </header>

      {/* Toolbar */}
      <div className="bg-white border-b border-gray-200 px-6 py-3 flex-shrink-0">
        <div className="flex items-center justify-between">
          <div className="flex items-center space-x-4">
            <h3 className="text-lg font-semibold text-gray-900">Code Runner</h3>
            <div className="flex items-center space-x-2">
              <label className="text-sm text-gray-600">言語選択:</label>
              <select
                value={language}
                onChange={(e) => handleLanguageChange(e.target.value as Language)}
                className="px-3 py-1 border border-gray-300 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-blue-500"
              >
                {Object.entries(LANGUAGES).map(([key, name]) => (
                  <option key={key} value={key}>{name}</option>
                ))}
              </select>
            </div>
          </div>
          <div className="flex space-x-2">
            <button
              onClick={runCode}
              disabled={isRunning || !code.trim()}
              className="flex items-center px-3 py-2 bg-green-600 hover:bg-green-700 disabled:bg-gray-400 text-white rounded-lg transition-colors text-sm"
            >
              <Play className="w-4 h-4 mr-1" />
              {isRunning ? 'Running' : 'Execute'}
            </button>
            <button className="flex items-center px-3 py-2 bg-blue-600 hover:bg-blue-700 text-white rounded-lg transition-colors text-sm">
              <Save className="w-4 h-4 mr-1" />
              保存
            </button>
            <button className="p-2 bg-gray-200 hover:bg-gray-300 text-gray-700 rounded-lg transition-colors">
              <Upload className="w-4 h-4" />
            </button>
            <button className="p-2 bg-gray-200 hover:bg-gray-300 text-gray-700 rounded-lg transition-colors">
              <Download className="w-4 h-4" />
            </button>
          </div>
        </div>
      </div>

      {/* Editor and Output - Takes remaining height */}
      <div className="flex-1 grid grid-cols-4 gap-0 rounded-b-lg overflow-hidden">
        {/* Code Editor */}
        <div className="bg-gray-900 flex flex-col col-span-3">
          <div className="flex items-center justify-between px-4 py-2 bg-gray-100 border-b border-gray-300 flex-shrink-0">
            <span className="text-sm text-gray-700 font-medium flex items-center">
              <Code className="w-4 h-4 mr-2" />
              main.{language === 'cpp' ? 'cpp' : language === 'javascript' ? 'js' : language}
            </span>
            <div className="flex space-x-2">
              <div className="w-3 h-3 bg-red-400 rounded-full"></div>
              <div className="w-3 h-3 bg-yellow-400 rounded-full"></div>
              <div className="w-3 h-3 bg-green-400 rounded-full"></div>
            </div>
          </div>
          <textarea
            value={code}
            onChange={(e) => setCode(e.target.value)}
            placeholder="Write your code here... ✨"
            className="flex-1 p-4 bg-gray-900 text-gray-100 font-mono text-sm resize-none outline-none border-r border-gray-300"
            spellCheck="false"
          />
        </div>

        {/* Output Panel */}
        <div className="bg-gray-900 flex flex-col">
          <div className="flex items-center px-4 py-2 bg-gray-100 border-b border-gray-300 flex-shrink-0">
            <span className="text-sm text-gray-700 font-medium flex items-center">
              <Terminal className="w-4 h-4 mr-2" />
              実行結果
            </span>
          </div>
          <div className="flex-1 p-4 overflow-y-auto">
            <pre className="text-green-400 font-mono text-sm whitespace-pre-wrap">
              {output || (isRunning ? 'Running...' : 'コードを実行すると結果がここに表示されます')}
            </pre>
          </div>
        </div>
      </div>
    </div>
  );
}
