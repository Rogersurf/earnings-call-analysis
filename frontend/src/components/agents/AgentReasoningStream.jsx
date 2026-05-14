import React, { useState, useEffect, useRef } from 'react';
import { motion } from 'framer-motion';
import { Zap, CheckCircle, AlertTriangle, Cpu } from 'lucide-react';

export default function AgentReasoningStream({ streamData }) {
  const [messages, setMessages] = useState([]);
  const [currentIndex, setCurrentIndex] = useState(0);
  const intervalRef = useRef(null);

  useEffect(() => {
    intervalRef.current = setInterval(() => {
      if (currentIndex < streamData.length) {
        setMessages(prev => [streamData[currentIndex], ...prev]);
        setCurrentIndex(i => i + 1);
      } else {
        clearInterval(intervalRef.current);
      }
    }, 2000);
    return () => clearInterval(intervalRef.current);
  }, [currentIndex, streamData]);

  const getIcon = (type) => {
    switch(type) {
      case 'warning': return <Zap className="w-4 h-4 text-yellow-400" />;
      case 'alert': return <AlertTriangle className="w-4 h-4 text-red-400" />;
      default: return <CheckCircle className="w-4 h-4 text-green-400" />;
    }
  };

  return (
    <div className="bg-black/60 backdrop-blur-sm border border-cyan-500/30 rounded-2xl p-4 h-full overflow-y-auto">
      <div className="flex items-center gap-2 mb-4">
        <Cpu className="w-5 h-5 text-cyan-400 animate-pulse" />
        <h3 className="text-sm font-semibold text-cyan-300">MULTI‑AGENT REASONING STREAM</h3>
      </div>
      <div className="space-y-3">
        {messages.map((msg, idx) => (
          <motion.div
            key={idx}
            initial={{ opacity: 0, x: -20 }}
            animate={{ opacity: 1, x: 0 }}
            className="bg-zinc-900/80 border border-zinc-800 rounded-xl p-3"
          >
            <div className="flex items-start gap-2">
              {getIcon(msg.type)}
              <div className="flex-1">
                <div className="flex justify-between text-xs">
                  <span className="font-mono text-cyan-300">{msg.agent}</span>
                  <span className="text-zinc-500">conf: {(msg.confidence * 100).toFixed(0)}%</span>
                </div>
                <p className="text-sm text-zinc-200 mt-1">{msg.message}</p>
                <div className="w-full bg-zinc-800 rounded-full h-1 mt-2">
                  <div className="bg-cyan-400 h-1 rounded-full transition-all duration-500" style={{ width: `${msg.confidence * 100}%` }} />
                </div>
              </div>
            </div>
          </motion.div>
        ))}
        {currentIndex >= streamData.length && (
          <div className="text-center text-xs text-zinc-500">✓ All agents finished reasoning</div>
        )}
      </div>
    </div>
  );
}