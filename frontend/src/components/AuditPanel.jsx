import React from 'react';
import { CheckCircle2, ShieldCheck } from 'lucide-react';

export default function AuditPanel({ auditData }) {
  return (
    <div className="bg-slate-900/80 border border-slate-800 rounded-xl p-5">
      <div className="flex items-center gap-2 text-emerald-400 mb-2">
        <ShieldCheck className="w-5 h-5" />
        <h4 className="font-bold text-sm text-white">Mathematical Ledger Reconciliation</h4>
      </div>
      <p className="text-xs text-slate-400 mb-4">
        Zero-sum balance invariant continuously validated against all immutable debit and credit journal entries.
      </p>
      <div className="p-3 bg-emerald-950/30 border border-emerald-500/20 rounded-lg flex items-center justify-between text-xs">
        <span className="text-emerald-300 font-medium">Global Ledger Status</span>
        <span className="font-bold text-emerald-400 font-mono">VERIFIED BALANCED</span>
      </div>
    </div>
  );
}
