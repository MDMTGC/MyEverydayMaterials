const CACHE_NAME = 'myeverydaymaterials-v1';
const STATIC_ASSETS = [
  '/',
  '/css/style.css',
  '/js/main.js',
  '/favicon.svg',
  '/robots.txt',
  '/about',
  '/methodology'
];

// On install, pre-cache core layout assets
self.addEventListener('install', event => {
  event.waitUntil(
    caches.open(CACHE_NAME).then(cache => {
      return cache.addAll(STATIC_ASSETS);
    }).then(() => self.skipWaiting())
  );
});

// Clean up legacy caches
self.addEventListener('activate', event => {
  event.waitUntil(
    caches.keys().then(keys => {
      return Promise.all(
        keys.map(key => {
          if (key !== CACHE_NAME) {
            return caches.delete(key);
          }
        })
      );
    }).then(() => self.clients.claim())
  );
});

// Cache strategy: NetworkFirst for HTML pages, CacheFirst for static assets
self.addEventListener('fetch', event => {
  const request = event.request;
  const url = new URL(request.url);

  // Focus only on local HTTP/HTTPS requests
  if (!url.protocol.startsWith('http')) return;

  // Check if it's an HTML page/navigation request
  const isHtml = request.headers.get('accept').includes('text/html') || 
                 request.mode === 'navigate';

  if (isHtml) {
    // Network-First with Cache Fallback for pages (to ensure fresh data when online)
    event.respondWith(
      fetch(request)
        .then(response => {
          const copy = response.clone();
          caches.open(CACHE_NAME).then(cache => cache.put(request, copy));
          return response;
        })
        .catch(() => {
          return caches.match(request);
        })
    );
  } else {
    // Cache-First with Network Fallback for assets, images, and sitemaps
    event.respondWith(
      caches.match(request).then(cachedResponse => {
        if (cachedResponse) {
          return cachedResponse;
        }
        return fetch(request).then(response => {
          // Cache valid responses
          if (response.status === 200) {
            const copy = response.clone();
            caches.open(CACHE_NAME).then(cache => cache.put(request, copy));
          }
          return response;
        });
      })
    );
  }
});
