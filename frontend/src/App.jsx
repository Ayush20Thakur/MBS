import React, { useState, useEffect } from 'react';
import Navbar from './components/Navbar';
import MetricCard from './components/MetricCard';
import LiveStreamFeed from './components/LiveStreamFeed';
import { DollarSign, ShieldAlert, Cpu, CheckCircle2 } from 'lucide-react';
import { fetchHealth } from './services/api';

export default function App() {
  const [health, setHealth] = useState(null);

  useEffect(() => {
    fetchHealth().then(setHealth).catch(console.error);
  }, []);

  const demoTxs = [
    { id: '4a1b8c2d-9011', amount: 350.00, status: 'SETTLED', created_at: new Date() },
    { id: '7e3f2a1b-4492', amount: 82000.00, status: 'REJECTED', created_at: new Date() },
    { id: '1c9d4e5f-1184', amount: 1250.50, status: 'SETTLED', created_at: new Date() },
  ];

  return (
    <div className="min-h-screen bg-slate-950 flex flex-col">
      <Navbar />
      <main className="flex-1 max-w-7xl w-full mx-auto px-6 py-8">
        {/* Metric Grid */}
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-5 mb-8">
          <MetricCard title="Settled Volume (24h)" value="$2,491,820" change="+14.2%" icon={DollarSign} trend="up" />
          <MetricCard title="Peak Ingestion TPS" value="1,450 req/s" change="+8.1%" icon={Cpu} trend="up" />
          <MetricCard title="Interception Rate" value="99.4%" change="-0.02%" icon={ShieldAlert} trend="up" />
          <MetricCard title="Ledger Invariants" value="100% Balanced" change="Zero Drift" icon={CheckCircle2} trend="up" />
        </div>

        {/* Dynamic Panels */}
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
          <div className="lg:col-span-2">
            <LiveStreamFeed transactions={demoTxs} />
          </div>
          <div className="bg-slate-900/80 border border-slate-800 rounded-xl p-5">
            <h3 className="font-semibold text-sm text-slate-200 mb-3">Cluster Health & Node Telemetry</h3>
            <p className="text-xs text-slate-400 mb-4">
              Direct connection to distributed consensus coordinators and isolation forest inference workers.
            </p>
            <div className="space-y-2 text-xs font-mono">
              <div className="flex justify-between py-1 border-b border-slate-800">
                <span className="text-slate-400">Node Status:</span>
                <span className="text-emerald-400 font-semibold">{health?.status || 'ONLINE'}</span>
              </div>
              <div className="flex justify-between py-1 border-b border-slate-800">
                <span className="text-slate-400">Service:</span>
                <span className="text-slate-200">{health?.service || 'SentinelFlow'}</span>
              </div>
              <div className="flex justify-between py-1 border-b border-slate-800">
                <span className="text-slate-400">Engine Core:</span>
                <span className="text-indigo-400">FastAPI Asyncpg</span>
              </div>
            </div>
          </div>
        </div>
      </main>
    </div>
  );
}
