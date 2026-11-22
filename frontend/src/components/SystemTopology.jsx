import React from 'react';
import { Server, Database, Activity } from 'lucide-react';

export default function SystemTopology() {
  return (
    <div className="bg-slate-900/80 border border-slate-800 rounded-xl p-5">
      <h3 className="font-semibold text-sm text-slate-200 mb-4 flex items-center gap-2">
        <Activity className="w-4 h-4 text-indigo-400" />
        Cluster Node Topology
      </h3>
      <div className="grid grid-cols-3 gap-3 text-center text-xs">
        <div className="p-3 bg-slate-950/60 border border-slate-800 rounded-lg">
          <Server className="w-5 h-5 mx-auto text-indigo-400 mb-1" />
          <p className="font-semibold text-white">API Gateway</p>
          <p className="text-[10px] text-emerald-400">3 Replicas</p>
        </div>
        <div className="p-3 bg-slate-950/60 border border-slate-800 rounded-lg">
          <Database className="w-5 h-5 mx-auto text-cyan-400 mb-1" />
          <p className="font-semibold text-white">PostgreSQL</p>
          <p className="text-[10px] text-emerald-400">Multi-AZ Master</p>
        </div>
        <div className="p-3 bg-slate-950/60 border border-slate-800 rounded-lg">
          <Server className="w-5 h-5 mx-auto text-amber-400 mb-1" />
          <p className="font-semibold text-white">Redis Cluster</p>
          <p className="text-[10px] text-emerald-400">In-Memory Bus</p>
        </div>
      </div>
    </div>
  );
}
