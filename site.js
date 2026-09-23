/* B. Morvay Coaching: the one script every page loads (with defer).
   Each part checks that its element exists, so pages only run what they use.
   Nothing here stores data on the visitor's device and nothing loads from other sites. */
(function () {
  'use strict';

  var reduceMotion = window.matchMedia('(prefers-reduced-motion: reduce)');

  // Footer year
  document.querySelectorAll('[data-year]').forEach(function (el) {
    el.textContent = String(new Date().getFullYear());
  });

  // Mobile menu: a disclosure button. Escape, a link, a click outside or tabbing away closes it.
  var header = document.querySelector('.site-header');
  var toggle = header && header.querySelector('.menu-toggle');
  var menu = document.getElementById('site-menu');
  if (header && toggle && menu) {
    var setOpen = function (open) {
      header.classList.toggle('menu-open', open);
      toggle.setAttribute('aria-expanded', String(open));
      toggle.setAttribute('aria-label', open ? 'Close menu' : 'Open menu');
    };
    var isOpen = function () { return toggle.getAttribute('aria-expanded') === 'true'; };
    toggle.addEventListener('click', function () { setOpen(!isOpen()); });
    menu.addEventListener('click', function (e) { if (e.target.closest('a')) setOpen(false); });
    document.addEventListener('keydown', function (e) {
      if (e.key === 'Escape' && isOpen()) { setOpen(false); toggle.focus(); }
    });
    document.addEventListener('click', function (e) {
      if (isOpen() && !header.contains(e.target)) setOpen(false);
    });
    header.addEventListener('focusout', function (e) {
      if (isOpen() && e.relatedTarget && !header.contains(e.relatedTarget)) setOpen(false);
    });
  }

  // Blocks rise into place as they come into view. The starting state only exists while this
  // observer is running, so if anything here fails the page is simply all visible. Nothing
  // moves for people who ask for less motion, and a safety timer reveals anything left over.
  var reveals = document.querySelectorAll('[data-reveal]');
  if (reveals.length && !reduceMotion.matches && 'IntersectionObserver' in window) {
    var showAll = function () {
      reveals.forEach(function (el) { el.classList.add('is-in'); });
    };
    document.documentElement.classList.add('reveal-on');
    var revealer = new IntersectionObserver(function (entries) {
      entries.forEach(function (entry) {
        if (!entry.isIntersecting) return;
        entry.target.classList.add('is-in');
        revealer.unobserve(entry.target);
      });
    }, { rootMargin: '0px 0px -6% 0px', threshold: 0.04 });
    reveals.forEach(function (el) { revealer.observe(el); });
    setTimeout(showAll, 4000);
    window.addEventListener('beforeprint', showAll);
  }

  // Back to top: appears after the first screen, then hands keyboard focus to the page start
  var toTop = document.getElementById('back-to-top');
  if (toTop) {
    var showToTop = function () { toTop.classList.toggle('visible', window.scrollY > 900); };
    window.addEventListener('scroll', showToTop, { passive: true });
    showToTop();
    toTop.addEventListener('click', function () {
      window.scrollTo({ top: 0, behavior: reduceMotion.matches ? 'auto' : 'smooth' });
      var main = document.getElementById('main');
      if (main) main.focus({ preventScroll: true });
    });
  }

  // Hero video. Phones get a small version (about 800 KB) and desktops the full one.
  // It is skipped for reduced motion and for data saver, and it only loads once the picture
  // is near the screen, so nobody downloads it without seeing it. The still image stays
  // underneath, which is what shows if playing is blocked (iOS Low Power Mode, for example).
  var media = document.querySelector('[data-hero-video]');
  if (media) {
    var saveData = navigator.connection && navigator.connection.saveData;
    if (!reduceMotion.matches && !saveData) {
      var startVideo = function () {
        var wide = window.matchMedia('(min-width: 861px)').matches;
        var src = wide ? media.getAttribute('data-hero-video') : media.getAttribute('data-hero-video-small');
        if (!src || media.querySelector('video')) return;
        var video = document.createElement('video');
        video.className = 'hero-video';
        video.muted = true; video.loop = true; video.playsInline = true; video.autoplay = true;
        video.setAttribute('muted', ''); video.setAttribute('playsinline', ''); video.setAttribute('autoplay', '');
        video.setAttribute('aria-hidden', 'true');
        video.preload = 'auto';
        video.src = src;
        var button = document.createElement('button');
        button.type = 'button';
        button.className = 'video-toggle';
        button.hidden = true;
        var pauseIcon = '<svg viewBox="0 0 24 24" width="18" height="18" aria-hidden="true"><rect x="6" y="5" width="4" height="14" rx="1" fill="currentColor"/><rect x="14" y="5" width="4" height="14" rx="1" fill="currentColor"/></svg>';
        var playIcon = '<svg viewBox="0 0 24 24" width="18" height="18" aria-hidden="true"><path d="M8 5v14l11-7z" fill="currentColor"/></svg>';
        var showState = function () {
          var paused = video.paused;
          button.innerHTML = paused ? playIcon : pauseIcon;
          button.setAttribute('aria-label', paused ? 'Play background video' : 'Pause background video');
        };
        var tryPlay = function () {
          var played = video.play();
          if (played && played.catch) played.catch(function () {});
        };
        button.addEventListener('click', function () {
          if (video.paused) { tryPlay(); } else { video.pause(); }
        });
        video.addEventListener('play', showState);
        video.addEventListener('pause', showState);
        video.addEventListener('playing', function () { video.classList.add('on'); button.hidden = false; showState(); }, { once: true });
        video.addEventListener('error', function () { video.remove(); button.remove(); });
        media.appendChild(video);
        media.appendChild(button);
        tryPlay();
        // Some phones refuse to start until the person touches the screen (Low Power Mode)
        window.addEventListener('touchstart', tryPlay, { once: true, passive: true });
      };
      // Wait until the page has finished loading, so the video never competes with the
      // text and the picture people see first.
      var watchForVideo = function () {
        if (!('IntersectionObserver' in window)) { startVideo(); return; }
        var watcher = new IntersectionObserver(function (entries) {
          if (entries.some(function (e) { return e.isIntersecting; })) { watcher.disconnect(); startVideo(); }
        }, { rootMargin: '250px' });
        watcher.observe(media);
      };
      if (document.readyState === 'complete') watchForVideo();
      else window.addEventListener('load', watchForVideo, { once: true });
    }
  }

  // Consultation request form (Netlify Forms). Shows sending, error and success states on the page,
  // keeps what the visitor typed if sending fails, and never opens an email app by itself.
  var form = document.getElementById('enquiry-form');
  if (form) {
    var submit = form.querySelector('[type="submit"]');
    var submitLabel = submit.textContent;
    var errorBox = document.getElementById('form-error');
    var success = document.getElementById('form-success');
    var retry = document.getElementById('form-retry');
    var emailLink = document.getElementById('form-email-link');
    var sending = false;

    // Where the visitor came from, sent only with their request: campaign tags on the address
    // and the site that linked here. Nothing is stored on the device.
    var sourceField = form.elements.namedItem('source');
    if (sourceField) {
      var params = new URLSearchParams(window.location.search);
      var parts = ['utm_source', 'utm_medium', 'utm_campaign'].filter(function (k) { return params.get(k); })
        .map(function (k) { return k.replace('utm_', '') + '=' + params.get(k); });
      try {
        if (document.referrer) {
          var from = new URL(document.referrer).hostname;
          if (from && from !== window.location.hostname) parts.push('from=' + from);
        }
      } catch (e) { /* no usable referrer */ }
      sourceField.value = parts.join('; ').slice(0, 300);
    }

    var mailtoFor = function () {
      var data = new FormData(form);
      var body = 'Name: ' + (data.get('name') || '') + '\nEmail: ' + (data.get('email') || '') +
        '\nPhone: ' + (data.get('phone') || '') + '\n\nWhat I would like help with:\n' + (data.get('message') || '');
      return 'mailto:morvaybalazs@gmail.com?subject=' + encodeURIComponent('Consultation request') +
        '&body=' + encodeURIComponent(body);
    };

    var finish = function () {
      sending = false;
      submit.disabled = false;
      submit.textContent = submitLabel;
      form.removeAttribute('aria-busy');
    };

    var showError = function () {
      finish();
      if (emailLink) emailLink.href = mailtoFor();
      errorBox.hidden = false;
      errorBox.focus();
    };

    form.addEventListener('submit', function (e) {
      e.preventDefault();
      if (sending) return;
      if (!form.checkValidity()) { form.reportValidity(); return; }
      sending = true;
      submit.disabled = true;
      submit.textContent = 'Sending...';
      form.setAttribute('aria-busy', 'true');
      errorBox.hidden = true;

      var controller = 'AbortController' in window ? new AbortController() : null;
      var timer = setTimeout(function () { if (controller) controller.abort(); }, 20000);
      fetch('/', {
        method: 'POST',
        headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
        body: new URLSearchParams(new FormData(form)).toString(),
        signal: controller ? controller.signal : undefined
      }).then(function (response) {
        clearTimeout(timer);
        if (!response.ok) throw new Error('HTTP ' + response.status);
        var name = String(new FormData(form).get('name') || '').trim().split(/\s+/)[0];
        var greet = document.getElementById('form-success-name');
        if (greet && name) greet.textContent = ', ' + name;
        form.hidden = true;
        success.hidden = false;
        success.focus();
      }).catch(function () {
        clearTimeout(timer);
        showError();
      });
    });

    if (retry) retry.addEventListener('click', function () {
      if (form.requestSubmit) form.requestSubmit(); else submit.click();
    });
  }

  // Print buttons (check-in template)
  document.querySelectorAll('[data-print]').forEach(function (b) {
    b.addEventListener('click', function () { window.print(); });
  });
})();
