import React from 'react';
import { Shield, AlertTriangle, Zap, Globe, Gauge } from 'lucide-react';

export default function FraudRadar({ incidents = [] }) {
  return (
    <div className="bg-slate-900/80 border border-slate-800 rounded-xl p-5">
      <div className="flex items-center justify-between mb-4">
        <h3 className="font-semibold text-sm text-slate-200">Threat Intelligence & Anomaly Radar</h3>
        <span className="text-[10px] bg-rose-500/10 text-rose-400 border border-rose-500/20 px-2 py-0.5 rounded-full font-mono">
          HIGH RISK ISOLATION
        </span>
      </div>
      <div className="grid grid-cols-2 gap-3 text-xs">
        <div className="p-3 bg-slate-950/60 rounded-lg border border-slate-800 flex items-center gap-2">
          <Zap className="w-4 h-4 text-amber-400" />
          <div>
            <p className="text-slate-400 text-[10px]">Velocity Bursts</p>
            <p className="font-bold text-white font-mono">3 Intercepted</p>
          </div>
        </div>
        <div className="p-3 bg-slate-950/60 rounded-lg border border-slate-800 flex items-center gap-2">
          <Globe className="w-4 h-4 text-cyan-400" />
          <div>
            <p className="text-slate-400 text-[10px]">Impossible Travel</p>
            <p className="font-bold text-white font-mono">1 Flagged</p>
          </div>
        </div>
      </div>
    </div>
  );
}
