export function formatCurrency(amount, currency = 'USD') {
  return new Intl.NumberFormat('en-US', {
    style: 'currency',
    currency: currency,
  }).format(amount);
}

export function truncateHash(hash, length = 8) {
  if (!hash) return '';
  return `${hash.substring(0, length)}...`;
}
