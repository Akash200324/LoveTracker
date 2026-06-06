const CACHE_NAME = 'love-tracker-cache-v1';
const urlsToCache = [
  '/dashboard/',
  '/static/manifest.json',
  '/static/images/pwa_icon.png'
];

self.addEventListener('install', function(event) {
  // Perform install steps
  event.waitUntil(
    caches.open(CACHE_NAME)
      .then(function(cache) {
        console.log('Opened cache');
        // Do not fail install if cache fails, as offline is a progressive enhancement
        return cache.addAll(urlsToCache).catch((err) => {
          console.warn('Failed to cache all resources on install:', err);
        });
      })
  );
});

self.addEventListener('fetch', function(event) {
  event.respondWith(
    fetch(event.request).catch(function() {
      return caches.match(event.request);
    })
  );
});
