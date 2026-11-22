# Algorithmic Complexity Analysis

## 1. Time Complexity
- **Sliding-Window Rate Limiter**: $\mathcal{O}(K)$ where $K$ is the number of requests in the moving 60-second window. Purging expired timestamps runs in linear time relative to window density.
- **Idempotency Key Verification**: $\mathcal{O}(1)$ average lookups via indexed B-Tree in PostgreSQL / in-memory hash index.
- **Double-Entry Journal Insertion**: $\mathcal{O}(1)$ for atomic insertion of two balancing journal entries.
- **Isolation Forest Evaluation**: $\mathcal{O}(T \cdot \log N)$ where $T$ is number of trees (100) and $N$ is sample depth, operating well under 5ms.

## 2. Space Complexity
- Ledger space: Strictly $\mathcal{O}(N)$ where $N$ is total number of processed transactions.
