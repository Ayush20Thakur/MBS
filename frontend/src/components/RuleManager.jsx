import React from 'react';
import { Sliders, Plus, Check, X } from 'lucide-react';

export default function RuleManager({ rules = [] }) {
  return (
    <div className="bg-slate-900/80 border border-slate-800 rounded-xl p-5">
      <div className="flex items-center justify-between mb-4">
        <h3 className="font-semibold text-sm text-slate-200 flex items-center gap-2">
          <Sliders className="w-4 h-4 text-indigo-400" />
          Active Policy Rules
        </h3>
        <button className="text-xs flex items-center gap-1 bg-indigo-600 hover:bg-indigo-500 text-white px-2.5 py-1 rounded-md transition font-medium">
          <Plus className="w-3 h-3" /> New Rule
        </button>
      </div>
      <div className="space-y-2 text-xs">
        <div className="p-2.5 bg-slate-950/60 rounded-lg border border-slate-800 flex items-center justify-between">
          <div>
            <p className="font-medium text-slate-200">Single Wire Limit &gt; $50k</p>
            <p className="text-[10px] text-slate-500">Action: Hard Reject</p>
          </div>
          <span className="w-2 h-2 rounded-full bg-emerald-400"></span>
        </div>
        <div className="p-2.5 bg-slate-950/60 rounded-lg border border-slate-800 flex items-center justify-between">
          <div>
            <p className="font-medium text-slate-200">Velocity Limit (5 tx / 60s)</p>
            <p className="text-[10px] text-slate-500">Action: Trigger Flag</p>
          </div>
          <span className="w-2 h-2 rounded-full bg-emerald-400"></span>
        </div>
      </div>
    </div>
  );
}
