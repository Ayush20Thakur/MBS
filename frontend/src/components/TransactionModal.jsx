import React, { useState } from 'react';
import { X, Send } from 'lucide-react';

export default function TransactionModal({ isOpen, onClose, onSend }) {
  if (!isOpen) return null;
  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/60 backdrop-blur-sm">
      <div className="bg-slate-900 border border-slate-800 rounded-xl p-6 w-full max-w-md shadow-2xl">
        <div className="flex justify-between items-center mb-4">
          <h3 className="font-bold text-white text-base">Initiate Ledger Transfer</h3>
          <button onClick={onClose} className="text-slate-400 hover:text-white"><X className="w-5 h-5" /></button>
        </div>
        <form className="space-y-4 text-xs">
          <div>
            <label className="text-slate-400 block mb-1">Source Account ID</label>
            <input type="text" className="w-full bg-slate-950 border border-slate-800 rounded-lg px-3 py-2 text-white" placeholder="SF1000000001" />
          </div>
          <div>
            <label className="text-slate-400 block mb-1">Destination Account ID</label>
            <input type="text" className="w-full bg-slate-950 border border-slate-800 rounded-lg px-3 py-2 text-white" placeholder="SF1000000002" />
          </div>
          <div>
            <label className="text-slate-400 block mb-1">Transfer Amount (USD)</label>
            <input type="number" step="0.01" className="w-full bg-slate-950 border border-slate-800 rounded-lg px-3 py-2 text-white" placeholder="250.00" />
          </div>
          <button type="button" className="w-full bg-indigo-600 hover:bg-indigo-500 text-white font-semibold py-2.5 rounded-lg flex items-center justify-center gap-2 transition">
            <Send className="w-4 h-4" /> Execute Transfer
          </button>
        </form>
      </div>
    </div>
  );
}
