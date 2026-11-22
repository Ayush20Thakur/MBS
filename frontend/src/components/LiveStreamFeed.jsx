import React from 'react';
import { ArrowUpRight, ArrowDownLeft, ShieldAlert } from 'lucide-react';

export default function LiveStreamFeed({ transactions = [] }) {
  return (
    <div className="bg-slate-900/80 border border-slate-800 rounded-xl p-5">
      <h3 className="font-semibold text-sm text-slate-200 mb-4 flex items-center justify-between">
        <span>Real-Time Ingestion Stream</span>
        <span className="text-xs font-normal text-slate-400">WebSocket Active</span>
      </h3>
      <div className="space-y-3">
        {transactions.length === 0 ? (
          <p className="text-xs text-slate-500 py-6 text-center">Awaiting incoming transactions...</p>
        ) : (
          transactions.slice(0, 6).map((tx) => (
            <div key={tx.id} className="flex items-center justify-between p-3 rounded-lg bg-slate-950/60 border border-slate-800/80 hover:border-slate-700 transition">
              <div className="flex items-center gap-3">
                <div className={`w-8 h-8 rounded-full flex items-center justify-center ${tx.status === 'SETTLED' ? 'bg-emerald-500/10 text-emerald-400' : 'bg-rose-500/10 text-rose-400'}`}>
                  {tx.status === 'SETTLED' ? <ArrowUpRight className="w-4 h-4" /> : <ShieldAlert className="w-4 h-4" />}
                </div>
                <div>
                  <p className="text-xs font-medium text-slate-200 font-mono">TX-{tx.id.substring(0, 8)}</p>
                  <p className="text-[10px] text-slate-500">{new Date(tx.created_at).toLocaleTimeString()}</p>
                </div>
              </div>
              <div className="text-right">
                <p className="text-xs font-bold text-white font-mono">${tx.amount.toFixed(2)}</p>
                <span className={`text-[10px] px-1.5 py-0.5 rounded font-semibold ${tx.status === 'SETTLED' ? 'text-emerald-400 bg-emerald-950/50' : 'text-rose-400 bg-rose-950/50'}`}>
                  {tx.status}
                </span>
              </div>
            </div>
          ))
        )}
      </div>
    </div>
  );
}
