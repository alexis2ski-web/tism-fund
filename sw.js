// tism fund offline worker: the app shell is cached; data.json always tries the network first
// and falls back to the last copy, so the app opens with yesterday's picks when offline.
const SHELL = "tism-shell-v3";
const DATA = "tism-data";
const FILES = ["./", "index.html", "manifest.webmanifest", "icons/icon-180.png", "icons/icon-192.png", "icons/icon-512.png"];
self.addEventListener("install", e => { e.waitUntil(caches.open(SHELL).then(c => c.addAll(FILES))); self.skipWaiting(); });
self.addEventListener("activate", e => {
  e.waitUntil(caches.keys().then(ks => Promise.all(ks.filter(k => k !== SHELL && k !== DATA).map(k => caches.delete(k)))));
  self.clients.claim();
});
self.addEventListener("fetch", e => {
  const url = new URL(e.request.url);
  if (e.request.method !== "GET" || url.origin !== location.origin) return;
  if (url.pathname.endsWith("/data.json")) {
    e.respondWith(fetch(e.request).then(r => { const c = r.clone(); caches.open(DATA).then(x => x.put("data.json", c)); return r; })
      .catch(() => caches.open(DATA).then(x => x.match("data.json"))));
    return;
  }
  // pages: network first so design changes show up on the next open; other files: cache first
  if (e.request.mode === "navigate") {
    e.respondWith(fetch(e.request).then(r => { const c = r.clone(); caches.open(SHELL).then(x => x.put("index.html", c)); return r; })
      .catch(() => caches.match("index.html")));
    return;
  }
  e.respondWith(caches.match(e.request).then(m => m || fetch(e.request)));
});
