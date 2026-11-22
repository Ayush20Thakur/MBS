const API_BASE = '/api/v1';

export async function fetchHealth() {
  const res = await fetch(`${API_BASE}/health`);
  return res.json();
}

export async function fetchTransactions() {
  const res = await fetch(`${API_BASE}/transactions/`);
  return res.json();
}

export async function fetchFraudIncidents() {
  const res = await fetch(`${API_BASE}/fraud/incidents`);
  return res.json();
}

export async function fetchFraudRules() {
  const res = await fetch(`${API_BASE}/fraud/rules`);
  return res.json();
}
