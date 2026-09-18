import React, { useState, useRef, useEffect } from 'react';
import axios from 'axios';
import { Bot, Send, User, AlertTriangle, ShieldCheck, MapPin, CheckCircle, Clock, ShieldAlert, Target, Activity } from 'lucide-react';
import { useLanguage } from '../contexts/LanguageContext';
import { useAuth } from '../contexts/AuthContext';

const API_BASE = 'http://localhost:8009/api';

export default function AIIncidentCommander() {
  const { isUrdu } = useLanguage();
  const { isViewer } = useAuth();
  const language = isUrdu ? 'ur' : 'en';
  const [messages, setMessages] = useState([
    {
      role: 'ai',
      content: 'I am the Urban IQ Incident Commander. I can analyze risk zones, evaluate AQI, simulate what-if scenarios, and explain operational priorities. How can I assist you today?',
      timestamp: new Date().toISOString()
    }
  ]);
  const [input, setInput] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const messagesEndRef = useRef(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!input.trim()) return;

    const userMsg = { role: 'user', content: input, timestamp: new Date().toISOString() };
    setMessages(prev => [...prev, userMsg]);
    setInput('');
    setIsLoading(true);

    try {
      // POST to our LangGraph backend
      const res = await axios.post(`${API_BASE}/ai/query`, {
        query: userMsg.content,
        language: language
      });

      const data = res.data;
      
      const aiMsg = {
        role: 'ai',
        content: data.answer,
        intent: data.intent,
        zone_id: data.zone_id,
        confidence: data.confidence,
        evidence: data.evidence,
        provenance: data.provenance,
        status_events: data.status_events,
        timestamp: data.generated_at || new Date().toISOString()
      };
      
      setMessages(prev => [...prev, aiMsg]);
    } catch (error) {
      console.error(error);
      setMessages(prev => [...prev, {
        role: 'ai',
        content: "System error: Unable to reach the LangGraph backend.",
        timestamp: new Date().toISOString()
      }]);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="flex flex-col lg:flex-row gap-6 h-[calc(100vh-140px)] animate-in fade-in duration-500">
      
      {/* Main Chat Area */}
      <div className="flex-1 bg-[#0b0f14] border border-white/5 rounded-2xl flex flex-col overflow-hidden relative shadow-2xl">
        
        {/* Chat Header */}
        <div className="h-16 border-b border-white/5 flex items-center justify-between px-6 bg-[#070b10]/50 backdrop-blur-md">
          <div className="flex items-center space-x-3">
            <div className="w-8 h-8 rounded-lg bg-cyan-500/10 flex items-center justify-center border border-cyan-500/20">
              <Bot className="w-4 h-4 text-cyan-400" />
            </div>
            <div>
              <h2 className="text-sm font-bold text-white tracking-widest uppercase">AI Incident Commander</h2>
              <p className="text-[10px] text-cyan-500 font-bold tracking-widest">LANGGRAPH ORCHESTRATION ONLINE</p>
            </div>
          </div>
        </div>

        {/* Chat Messages */}
        <div className="flex-1 overflow-y-auto p-6 space-y-6">
          {messages.map((msg, idx) => (
            <div key={idx} className={`flex ${msg.role === 'user' ? 'justify-end' : 'justify-start'}`}>
              <div className={`flex max-w-[80%] ${msg.role === 'user' ? 'flex-row-reverse' : 'flex-row'}`}>
                
                {/* Avatar */}
                <div className={`w-8 h-8 rounded-full flex items-center justify-center flex-shrink-0 ${msg.role === 'user' ? 'bg-indigo-500/20 border border-indigo-500/30 ml-4' : 'bg-cyan-500/20 border border-cyan-500/30 mr-4'}`}>
                  {msg.role === 'user' ? <User className="w-4 h-4 text-indigo-400" /> : <Bot className="w-4 h-4 text-cyan-400" />}
                </div>

                {/* Message Body */}
                <div className="flex flex-col space-y-2">
                  <div className={`p-4 rounded-2xl border ${msg.role === 'user' ? 'bg-indigo-500/10 border-indigo-500/20 text-indigo-100 rounded-tr-none' : 'bg-slate-800/50 border-white/5 text-slate-200 rounded-tl-none'}`}>
                    <p className="text-sm whitespace-pre-wrap leading-relaxed">{msg.content}</p>
                    
                    {/* Metadata Footer for AI */}
                    {msg.role === 'ai' && msg.intent && (
                      <div className="mt-4 pt-4 border-t border-white/5 flex flex-wrap gap-4 text-xs text-slate-500">
                        {msg.intent && (
                          <div className="flex items-center">
                            <Target className="w-3 h-3 mr-1 text-slate-400" />
                            Intent: <span className="ml-1 text-slate-300 uppercase">{msg.intent}</span>
                          </div>
                        )}
                        {msg.confidence > 0 && (
                          <div className="flex items-center">
                            <Activity className="w-3 h-3 mr-1 text-slate-400" />
                            Confidence: <span className="ml-1 text-emerald-400">{(msg.confidence * 100).toFixed(1)}%</span>
                          </div>
                        )}
                        <div className="flex items-center">
                          <Clock className="w-3 h-3 mr-1 text-slate-400" />
                          {new Date(msg.timestamp).toLocaleTimeString()}
                        </div>
                      </div>
                    )}
                  </div>
                </div>
              </div>
            </div>
          ))}

          {/* Loading / Streaming State */}
          {isLoading && (
            <div className="flex justify-start">
              <div className="flex max-w-[80%] flex-row">
                <div className="w-8 h-8 rounded-full bg-cyan-500/20 border border-cyan-500/30 flex items-center justify-center mr-4">
                  <Bot className="w-4 h-4 text-cyan-400 animate-pulse" />
                </div>
                <div className="p-4 rounded-2xl rounded-tl-none bg-slate-800/50 border border-white/5 text-slate-400 text-sm flex items-center space-x-2">
                  <div className="w-2 h-2 bg-cyan-500 rounded-full animate-bounce"></div>
                  <div className="w-2 h-2 bg-cyan-500 rounded-full animate-bounce" style={{animationDelay: '150ms'}}></div>
                  <div className="w-2 h-2 bg-cyan-500 rounded-full animate-bounce" style={{animationDelay: '300ms'}}></div>
                  <span className="ml-2 font-bold tracking-widest uppercase text-xs text-cyan-500">Analyzing...</span>
                </div>
              </div>
            </div>
          )}
          <div ref={messagesEndRef} />
        </div>

        {/* Input Area */}
        <div className="p-4 bg-[#070b10]/50 backdrop-blur-md border-t border-white/5">
          <form onSubmit={handleSubmit} className="relative">
            <input
              type="text"
              value={input}
              onChange={(e) => setInput(e.target.value)}
              placeholder={isViewer ? "Viewer mode - Read Only" : "Ask about current risks, scenarios, or specific zones..."}
              className={`w-full bg-slate-900/50 border border-white/10 rounded-xl py-4 pl-4 pr-12 text-sm text-white placeholder-slate-500 focus:outline-none focus:border-cyan-500/50 transition-colors ${isViewer ? 'cursor-not-allowed' : ''}`}
              disabled={isLoading || isViewer}
            />
            <button
              type="submit"
              disabled={isLoading || !input.trim() || isViewer}
              className="absolute right-2 top-2 bottom-2 aspect-square flex items-center justify-center bg-cyan-500 text-[#0b0f14] rounded-lg hover:bg-cyan-400 transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
            >
              <Send className="w-4 h-4" />
            </button>
          </form>
        </div>
      </div>

      {/* Side Panel: Evidence & Provenance */}
      <div className="w-full lg:w-96 flex-shrink-0 bg-[#0b0f14] border border-white/5 rounded-2xl flex flex-col overflow-hidden shadow-2xl">
        <div className="h-16 border-b border-white/5 flex items-center px-6 bg-[#070b10]/50 backdrop-blur-md">
          <ShieldAlert className="w-4 h-4 text-slate-400 mr-2" />
          <h3 className="text-xs font-bold text-slate-400 tracking-widest uppercase">Evidence & Status</h3>
        </div>
        
        <div className="flex-1 overflow-y-auto p-6 space-y-8">
          {/* We show the metadata of the LAST AI message */}
          {(() => {
            const lastAiMsg = [...messages].reverse().find(m => m.role === 'ai' && m.status_events);
            if (!lastAiMsg) return <div className="text-sm text-slate-500 text-center mt-10">No active operation.</div>;

            return (
              <>
                {/* Status Events */}
                <div>
                  <h4 className="text-[10px] font-bold text-slate-500 tracking-widest uppercase mb-4">Graph Execution Stream</h4>
                  <div className="space-y-3">
                    {lastAiMsg.status_events.map((evt, i) => (
                      <div key={i} className="flex items-start">
                        <div className="w-2 h-2 rounded-full bg-emerald-500 mt-1.5 mr-3 flex-shrink-0 relative">
                          {i !== lastAiMsg.status_events.length - 1 && (
                            <div className="absolute top-2 left-1/2 -ml-px w-px h-6 bg-white/10"></div>
                          )}
                        </div>
                        <p className="text-xs text-slate-300">{evt}</p>
                      </div>
                    ))}
                  </div>
                </div>

                {/* Provenance */}
                {lastAiMsg.provenance && lastAiMsg.provenance.length > 0 && (
                  <div>
                    <h4 className="text-[10px] font-bold text-slate-500 tracking-widest uppercase mb-4">Data Provenance</h4>
                    <div className="bg-slate-900/50 border border-white/5 rounded-xl p-4 space-y-2">
                      {lastAiMsg.provenance.map((prov, i) => (
                        <div key={i} className="text-xs text-slate-400 flex items-center">
                          <span className="w-1 h-1 rounded-full bg-slate-600 mr-2"></span>
                          {prov}
                        </div>
                      ))}
                    </div>
                  </div>
                )}

                {/* Evidence */}
                {lastAiMsg.evidence && lastAiMsg.evidence.length > 0 && (
                  <div>
                    <h4 className="text-[10px] font-bold text-slate-500 tracking-widest uppercase mb-4">Grounded Evidence</h4>
                    <div className="bg-blue-500/5 border border-blue-500/10 rounded-xl p-4 space-y-2">
                      {lastAiMsg.evidence.map((ev, i) => (
                        <div key={i} className="text-xs text-blue-200/70 flex items-start">
                          <span className="text-blue-500 mr-2 mt-0.5">•</span>
                          {ev}
                        </div>
                      ))}
                    </div>
                  </div>
                )}
              </>
            );
          })()}
        </div>
      </div>
    </div>
  );
}
