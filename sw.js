/* Offline shell for the installed app.
 *
 * Bump VERSION whenever index.html changes, or an installed copy can keep
 * serving the old one while offline. Navigations are network-first, so an
 * online launch always picks up a new build even if you forget. */
const VERSION = "v7";
const CACHE = "weekly-planner-" + VERSION;
const PAGE = "./index.html";
const SHELL = [
  "./",
  PAGE,
  "./manifest.webmanifest",
  "./icons/icon-192.png",
  "./icons/icon-512.png",
  "./icons/icon-maskable-512.png",
];

self.addEventListener("install", (e) => {
  e.waitUntil(
    caches.open(CACHE).then((c) => c.addAll(SHELL)).then(() => self.skipWaiting())
  );
});

self.addEventListener("activate", (e) => {
  e.waitUntil(
    caches.keys()
      .then((keys) => Promise.all(keys.filter((k) => k !== CACHE).map((k) => caches.delete(k))))
      .then(() => self.clients.claim())
  );
});

const keepable = (url) => url.origin === location.origin || /fonts\.(googleapis|gstatic)\.com$/.test(url.hostname);

self.addEventListener("fetch", (e) => {
  const req = e.request;
  if (req.method !== "GET") return;

  if (req.mode === "navigate") {
    e.respondWith(
      fetch(req)
        .then((res) => {
          const copy = res.clone();
          caches.open(CACHE).then((c) => c.put(PAGE, copy)).catch(() => {});
          return res;
        })
        .catch(() => caches.match(PAGE).then((hit) => hit || Response.error()))
    );
    return;
  }

  e.respondWith(
    caches.match(req).then((hit) => hit || fetch(req).then((res) => {
      if (res.ok && keepable(new URL(req.url))) {
        const copy = res.clone();
        caches.open(CACHE).then((c) => c.put(req, copy)).catch(() => {});
      }
      return res;
    }).catch(() => caches.match(req).then((h) => h || Response.error())))
  );
});
