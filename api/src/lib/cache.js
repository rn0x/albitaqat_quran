class Cache {
  constructor(defaultTTLSeconds = 300) {
    this.store = new Map();
    this.defaultTTL = defaultTTLSeconds * 1000;
  }

  get(key) {
    const entry = this.store.get(key);
    if (!entry) return null;

    if (Date.now() > entry.expires) {
      this.store.delete(key);
      return null;
    }

    return entry.data;
  }

  set(key, data, ttlSeconds) {
    const ttl = ttlSeconds ? ttlSeconds * 1000 : this.defaultTTL;
    this.store.set(key, {
      data,
      expires: Date.now() + ttl,
    });
  }

  delete(key) {
    this.store.delete(key);
  }

  clear() {
    this.store.clear();
  }

  size() {
    return this.store.size;
  }

  cleanup() {
    const now = Date.now();
    for (const [key, entry] of this.store) {
      if (now > entry.expires) {
        this.store.delete(key);
      }
    }
  }
}

// Singleton instance
let cacheInstance = null;

export function getCache(ttlSeconds) {
  if (!cacheInstance) {
    cacheInstance = new Cache(ttlSeconds);
  }
  return cacheInstance;
}

export function resetCache() {
  cacheInstance = null;
}
