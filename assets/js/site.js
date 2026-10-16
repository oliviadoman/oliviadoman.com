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

  /* ---------- v2 depth renderer (WebGL) ----------
     Each layer is warped by its own depth map instead of sliding as a flat card,
     the same math as parallax_v2/layering.py render(): source = dest - shift * depth. */
  var FG = 0.75, ZOOM = 1.09;
  var VS = 'attribute vec2 p;varying vec2 v;void main(){v=vec2(p.x*.5+.5,.5-p.y*.5);gl_Position=vec4(p,0.,1.);}';
  var FS = [
    'precision highp float;varying vec2 v;',
    'uniform sampler2D t0,t1,t2,td;uniform vec2 off;uniform vec4 view;',
    'vec2 warp(vec2 uv,int k){vec2 s=uv;for(int i=0;i<3;i++){vec3 d=texture2D(td,s).rgb;float z=k==0?d.r:(k==1?d.g:d.b);s=uv-off*z;}return s;}',
    'void main(){vec2 uv=view.xy+v*view.zw;',
    'vec3 c=texture2D(t0,warp(uv,0)).rgb;',
    'vec4 a=texture2D(t1,warp(uv,1));c=a.rgb+(1.-a.a)*c;',
    'vec4 b=texture2D(t2,warp(uv,2));c=b.rgb+(1.-b.a)*c;',
    'gl_FragColor=vec4(c,1.);}'
  ].join('\n');

  function depthGL(stage, base, onFail) {
    var canvas = document.createElement('canvas');
    canvas.className = 'px-gl';
    canvas.setAttribute('aria-hidden', 'true');
    var gl = null;
    try { gl = canvas.getContext('webgl', { alpha: false, antialias: false, premultipliedAlpha: false }); } catch (e) { gl = null; }
    if (!gl) return null;
    function sh(type, src) { var s = gl.createShader(type); gl.shaderSource(s, src); gl.compileShader(s); return gl.getShaderParameter(s, gl.COMPILE_STATUS) ? s : null; }
    var vs = sh(gl.VERTEX_SHADER, VS), fs = sh(gl.FRAGMENT_SHADER, FS);
    if (!vs || !fs) return null;
    var prog = gl.createProgram(); gl.attachShader(prog, vs); gl.attachShader(prog, fs); gl.linkProgram(prog);
    if (!gl.getProgramParameter(prog, gl.LINK_STATUS)) return null;
    gl.useProgram(prog);
    var buf = gl.createBuffer(); gl.bindBuffer(gl.ARRAY_BUFFER, buf);
    gl.bufferData(gl.ARRAY_BUFFER, new Float32Array([-1, -1, 1, -1, -1, 1, 1, 1]), gl.STATIC_DRAW);
    var loc = gl.getAttribLocation(prog, 'p'); gl.enableVertexAttribArray(loc); gl.vertexAttribPointer(loc, 2, gl.FLOAT, false, 0, 0);
    var uOff = gl.getUniformLocation(prog, 'off'), uView = gl.getUniformLocation(prog, 'view');
    var files = [['t0', 'l0.jpg', false], ['t1', 'l1.webp', true], ['t2', 'l2.webp', true], ['td', 'depth.png', false]];
    var api = { ready: false }, left = files.length, failed = false;
    files.forEach(function (f, i) {
      var im = new Image();
      im.onload = function () {
        if (failed) return;
        gl.activeTexture(gl.TEXTURE0 + i);
        var t = gl.createTexture(); gl.bindTexture(gl.TEXTURE_2D, t);
        gl.pixelStorei(gl.UNPACK_PREMULTIPLY_ALPHA_WEBGL, f[2]);
        gl.pixelStorei(gl.UNPACK_COLORSPACE_CONVERSION_WEBGL, f[0] === 'td' ? gl.NONE : gl.BROWSER_DEFAULT_WEBGL);
        gl.texImage2D(gl.TEXTURE_2D, 0, f[2] ? gl.RGBA : gl.RGB, f[2] ? gl.RGBA : gl.RGB, gl.UNSIGNED_BYTE, im);
        gl.texParameteri(gl.TEXTURE_2D, gl.TEXTURE_MIN_FILTER, gl.LINEAR);
        gl.texParameteri(gl.TEXTURE_2D, gl.TEXTURE_MAG_FILTER, gl.LINEAR);
        gl.texParameteri(gl.TEXTURE_2D, gl.TEXTURE_WRAP_S, gl.CLAMP_TO_EDGE);
        gl.texParameteri(gl.TEXTURE_2D, gl.TEXTURE_WRAP_T, gl.CLAMP_TO_EDGE);
        gl.uniform1i(gl.getUniformLocation(prog, f[0]), i);
        if (--left === 0) { api.ready = true; stage.classList.add('gl-on'); }
      };
      im.onerror = function () { if (!failed) { failed = true; canvas.remove(); onFail(); } };
      im.src = base + f[1];
    });
    canvas.addEventListener('webglcontextlost', function (e) { e.preventDefault(); api.ready = false; stage.classList.remove('gl-on'); onFail(); });
    var scene = stage.querySelector('.scene') || stage;
    scene.appendChild(canvas);
    api.draw = function (sx, sy) {
      var dpr = Math.min(window.devicePixelRatio || 1, 2);
      var w = stage.clientWidth, h = stage.clientHeight;
      var W = Math.round(w * dpr), H = Math.round(h * dpr);
      if (canvas.width !== W || canvas.height !== H) { canvas.width = W; canvas.height = H; gl.viewport(0, 0, W, H); }
      var s = Math.max(w / IMG_W, h / IMG_H) * ZOOM;
      var zw = (w / s) / IMG_W, zh = (h / s) / IMG_H;
      gl.uniform4f(uView, 0.5 - zw / 2, 0.5 - zh / 2, zw, zh);
      gl.uniform2f(uOff, sx / IMG_W, sy / IMG_H);
      gl.drawArrays(gl.TRIANGLE_STRIP, 0, 4);
    };
    return api;
  }

  /* ---------- Parallax stages ---------- */
  var IMG_W = 1408, IMG_H = 768, VERT = 25 / 80;
  function parallax(stage) {
    var layers = Array.prototype.slice.call(stage.querySelectorAll('.layer[data-f]'));
    var useCSS = function () {
      layers.forEach(function (l) { var bg = l.getAttribute('data-bg'); if (bg) l.style.backgroundImage = 'url(' + bg + ')'; });
    };
    var glr = null;
    if (stage.hasAttribute('data-gl')) {
      glr = depthGL(stage, stage.getAttribute('data-gl'), function () { glr = null; useCSS(); });
      if (!glr) useCSS();
    }
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
        if (glr && glr.ready) { glr.draw(cx * FG, cy * FG); requestAnimationFrame(frame); return; }
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
