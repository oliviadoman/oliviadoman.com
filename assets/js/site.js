/* oliviadoman.com: parallax hero, yarn thread, video loops, draft notes */
(function () {
  'use strict';
  var reduce = window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  var canHover = window.matchMedia && window.matchMedia('(hover: hover)').matches;

  function store(key, val) {
    try {
      if (val === undefined) return window.localStorage.getItem(key);
      window.localStorage.setItem(key, val);
    } catch (e) { return null; }
  }

  /* ---------- Draft notes ---------- */
  var notes = document.querySelectorAll('.note');
  if (notes.length) {
    var saved = store('draft-notes');
    var on = saved === null ? true : saved === 'on';
    document.body.classList.toggle('show-notes', on);
    var btn = document.createElement('button');
    btn.type = 'button';
    btn.className = 'notes-toggle';
    function label() {
      var showing = document.body.classList.contains('show-notes');
      btn.innerHTML = (showing ? 'Hide draft notes' : 'Show draft notes') + ' <span class="count">' + notes.length + '</span>';
      btn.setAttribute('aria-pressed', String(showing));
    }
    btn.addEventListener('click', function () {
      document.body.classList.toggle('show-notes');
      store('draft-notes', document.body.classList.contains('show-notes') ? 'on' : 'off');
      label();
      window.dispatchEvent(new Event('resize'));
    });
    label();
    document.body.appendChild(btn);
  }

  /* ---------- Video loops: play only while on screen ---------- */
  var vids = document.querySelectorAll('video[data-loop]');
  if (vids.length && 'IntersectionObserver' in window) {
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (en) {
        var v = en.target;
        if (en.isIntersecting && !reduce) {
          if (v.preload === 'none') v.preload = 'auto';
          var p = v.play(); if (p && p.catch) p.catch(function () {});
        } else { v.pause(); }
      });
    }, { threshold: 0.25 });
    vids.forEach(function (v) { v.muted = true; io.observe(v); });
  }

  /* ---------- Parallax stages ---------- */
  var IMG_W = 1408, IMG_H = 768, VERT = 25 / 80;
  function parallax(stage) {
    var layers = Array.prototype.slice.call(stage.querySelectorAll('.layer'));
    var factors = layers.map(function (l) { return parseFloat(l.getAttribute('data-f')) || 0; });
    var range = parseFloat(stage.getAttribute('data-range')) || 80;
    var tx = 0, ty = 0, x = 0, y = 0, lastMove = -1e9, last = performance.now();
    var phases = [0.7, 2.1, 4.0, 1.3, 5.2, 3.3, 0.2, 2.8, 4.6, 1.9];
    function drift(t) {
      var sx = 0, sy = 0, n = 0;
      for (var o = 1; o <= 5; o++) { sx += Math.sin(o * t + phases[o - 1]) / o; sy += Math.sin(o * t * 0.9 + phases[o + 4]) / o; n += 1 / o; }
      return [Math.max(-1, Math.min(1, sx / n * 1.6)), Math.max(-1, Math.min(1, sy / n * 1.6))];
    }
    function move(cx, cy) {
      var r = stage.getBoundingClientRect();
      tx = Math.max(-1, Math.min(1, ((cx - r.left) / r.width) * 2 - 1));
      ty = Math.max(-1, Math.min(1, ((cy - r.top) / r.height) * 2 - 1));
      lastMove = performance.now();
    }
    if (canHover) {
      stage.addEventListener('pointermove', function (e) { if (e.pointerType === 'mouse') move(e.clientX, e.clientY); });
      stage.addEventListener('pointerleave', function () { tx = 0; ty = 0; });
    }
    stage.setRange = function (r) { range = r; };
    var visible = true;
    if ('IntersectionObserver' in window) {
      new IntersectionObserver(function (es) { visible = es[0].isIntersecting; }).observe(stage);
    }
    function frame(now) {
      var dt = Math.min(0.05, (now - last) / 1000); last = now;
      if (visible) {
        var idle = now - lastMove > 2500;
        if (idle && !reduce) { var d = drift(now / 3800); tx = d[0]; ty = d[1]; }
        var k = reduce ? 1 : 1 - Math.pow(0.0012, dt);
        x += (tx - x) * k; y += (ty - y) * k;
        var w = stage.clientWidth, h = stage.clientHeight;
        var s = Math.max(w / IMG_W, h / IMG_H);
        var cx = -x * range, cy = -y * range * VERT;
        layers.forEach(function (el, i) {
          var sc = i === 0 ? 1.06 : 1;
          el.style.transform = 'translate3d(' + (cx * factors[i] * s).toFixed(2) + 'px,' + (cy * factors[i] * s).toFixed(2) + 'px,0) scale(' + sc + ')';
        });
      }
      requestAnimationFrame(frame);
    }
    requestAnimationFrame(frame);
    return stage;
  }
  document.querySelectorAll('[data-parallax]').forEach(function (stage) {
    var p = parallax(stage);
    var group = document.querySelector('[data-px-for="' + stage.id + '"]');
    if (!group) return;
    var verdict = group.querySelector('.px-verdict');
    group.querySelectorAll('button[data-range]').forEach(function (b) {
      b.addEventListener('click', function () {
        group.querySelectorAll('button[data-range]').forEach(function (o) { o.setAttribute('aria-pressed', String(o === b)); });
        p.setRange(parseFloat(b.getAttribute('data-range')));
        if (verdict) verdict.textContent = b.getAttribute('data-verdict');
      });
    });
  });

  /* ---------- Yarn thread (home) ---------- */
  var host = document.querySelector('[data-thread]');
  if (host) {
    var NS = 'http://www.w3.org/2000/svg';
    var svg = document.createElementNS(NS, 'svg');
    svg.setAttribute('class', 'thread-layer');
    svg.setAttribute('aria-hidden', 'true');
    var defs = document.createElementNS(NS, 'defs');
    var mask = document.createElementNS(NS, 'mask');
    mask.setAttribute('id', 'thread-reveal');
    mask.setAttribute('maskUnits', 'userSpaceOnUse');
    var mpath = document.createElementNS(NS, 'path');
    mpath.setAttribute('fill', 'none'); mpath.setAttribute('stroke', '#fff'); mpath.setAttribute('stroke-width', '40');
    mpath.setAttribute('stroke-linecap', 'round');
    mask.appendChild(mpath); defs.appendChild(mask); svg.appendChild(defs);
    var g = document.createElementNS(NS, 'g');
    g.setAttribute('mask', 'url(#thread-reveal)');
    var base = document.createElementNS(NS, 'path');
    var ply = document.createElementNS(NS, 'path');
    [base, ply].forEach(function (p) {
      p.setAttribute('fill', 'none'); p.style.stroke = 'var(--thread)';
      p.setAttribute('stroke-linecap', 'round'); p.setAttribute('stroke-linejoin', 'round'); g.appendChild(p);
    });
    base.setAttribute('stroke-width', '6'); base.setAttribute('stroke-opacity', '0.32');
    ply.setAttribute('stroke-width', '3'); ply.setAttribute('stroke-dasharray', '9 6');
    svg.appendChild(g);
    host.insertBefore(svg, host.firstChild);
    var len = 0;

    function layout() {
      var hb = host.getBoundingClientRect();
      var W = host.clientWidth, H = host.scrollHeight;
      svg.setAttribute('viewBox', '0 0 ' + W + ' ' + H);
      svg.setAttribute('width', W); svg.setAttribute('height', H);
      var knots = host.querySelectorAll('[data-knot]');
      var pts = [];
      knots.forEach(function (k, i) {
        var r = k.getBoundingClientRect();
        if (!r.width) return;
        var side = k.getAttribute('data-knot');
        var xx = side === 'left' ? Math.max(18, r.left - hb.left - 28) : side === 'right' ? Math.min(W - 18, r.right - hb.left + 28) : r.left - hb.left + r.width / 2;
        pts.push([xx, r.top - hb.top + Math.min(r.height / 2, 40)]);
      });
      if (!pts.length) return;
      var d = 'M ' + (W + 20) + ' 0';
      var prev = [W + 20, 0];
      pts.forEach(function (p, i) {
        var dy = p[1] - prev[1];
        d += ' C ' + prev[0].toFixed(1) + ' ' + (prev[1] + dy * 0.55).toFixed(1) + ', ' + p[0].toFixed(1) + ' ' + (p[1] - dy * 0.55).toFixed(1) + ', ' + p[0].toFixed(1) + ' ' + p[1].toFixed(1);
        d += i % 2 ? ' a 22 22 0 1 0 1 0' : ' a 22 22 0 1 1 -1 0';
        prev = p;
      });
      d += ' C ' + prev[0] + ' ' + (prev[1] + 220) + ', ' + (W * 0.6) + ' ' + (H - 120) + ', ' + (W * 0.6) + ' ' + (H + 40);
      [base, ply, mpath].forEach(function (p) { p.setAttribute('d', d); });
      len = mpath.getTotalLength();
      mpath.setAttribute('stroke-dasharray', len + ' ' + len);
      reveal();
    }
    function reveal() {
      if (!len) return;
      if (reduce) { mpath.setAttribute('stroke-dashoffset', '0'); return; }
      var hb = host.getBoundingClientRect();
      var seen = (window.innerHeight * 0.85 - hb.top) / host.scrollHeight;
      var prog = Math.max(0.04, Math.min(1, seen * 1.08));
      mpath.setAttribute('stroke-dashoffset', String(len * (1 - prog)));
    }
    var raf = 0;
    window.addEventListener('scroll', function () { if (!raf) raf = requestAnimationFrame(function () { raf = 0; reveal(); }); }, { passive: true });
    window.addEventListener('resize', layout);
    if ('ResizeObserver' in window) new ResizeObserver(function () { layout(); }).observe(host);
    window.addEventListener('load', layout);
    layout();
  }
})();
