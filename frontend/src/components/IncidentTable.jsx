import React from 'react';
import { AlertCircle, Eye, CheckCircle } from 'lucide-react';

export default function IncidentTable({ incidents = [] }) {
  return (
    <div className="bg-slate-900/80 border border-slate-800 rounded-xl p-5">
      <h3 className="font-semibold text-sm text-slate-200 mb-3 flex items-center gap-2">
        <AlertCircle className="w-4 h-4 text-rose-400" />
        Case Review Queue
      </h3>
      <div className="overflow-x-auto">
        <table className="w-full text-left text-xs">
          <thead>
            <tr className="border-b border-slate-800 text-slate-400">
              <th className="pb-2">Case ID</th>
              <th className="pb-2">Risk Score</th>
              <th className="pb-2">Primary Factor</th>
              <th className="pb-2 text-right">Action</th>
            </tr>
          </thead>
          <tbody className="divide-y divide-slate-800/60 text-slate-300">
            <tr>
              <td className="py-2.5 font-mono text-indigo-400">CASE-9921</td>
              <td className="py-2.5 font-mono text-rose-400 font-bold">0.94</td>
              <td className="py-2.5 text-slate-400">Amount &gt; $50k Ceiling</td>
              <td className="py-2.5 text-right">
                <button className="text-[11px] bg-slate-800 hover:bg-slate-700 text-slate-200 px-2 py-0.5 rounded transition">
                  Investigate
                </button>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
  );
}
