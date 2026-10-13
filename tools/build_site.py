#!/usr/bin/env python3
"""Generates the oliviadoman.com draft: index.html, work/*.html, notes.html.
Also writes index.artifact.html (same page without the document wrapper) for preview publishing."""
import html, os, sys

OUT = sys.argv[1]
LAUNCH = len(sys.argv) > 2 and sys.argv[2] == 'launch'
FEATURED = ['pupper', 'handyreader', 'spectral', 'yarn', 'flower'] if LAUNCH else ['spectral', 'yarn', 'charfx', 'blobs', 'flower', 'handyreader']
MORE = ['diffusion', 'vellum'] if LAUNCH else ['diffusion', 'procedural', 'vellum', 'pupper']
FONTS = 'https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,400;0,500;1,400&family=Karla:wght@400;500;600;700&display=swap'
GH = 'https://github.com/oliviadoman'
PX_REPO = GH + '/2.5D_Parallax_Pipeline-Senior_Project-'
SP_REPO = GH + '/Spectral_Path_Tracer'
PUP_REPO = GH + '/Pupper_Pickerupper-CS248a-'
LINKEDIN = 'https://www.linkedin.com/in/oliviadoman/'
EMAIL = 'olivia.d.doman@gmail.com'

ALL_NOTES = []  # (page_title, page_href, kind, text)

def esc(s): return html.escape(s, quote=True)

def note(kind, text, page=None):
    ALL_NOTES.append((page[0], page[1], kind, text))
    if LAUNCH: return ''
    label = 'Question' if kind == 'q' else 'Needed'
    cls = 'note q' if kind == 'q' else 'note'
    return f'<aside class="{cls}"><b>{label}</b>{text}</aside>'

def head(title, desc, pre):
    return f'''<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>{esc(title)}</title>
<meta name="description" content="{esc(desc)}">
<meta property="og:title" content="{esc(title)}">
<meta property="og:description" content="{esc(desc)}">
<meta property="og:image" content="{pre}assets/img/parallax-poster.jpg">
<link rel="icon" type="image/svg+xml" href="{pre}assets/img/favicon.svg">
<link rel="icon" type="image/png" sizes="32x32" href="{pre}assets/img/favicon-32.png">
<link rel="apple-touch-icon" href="{pre}assets/img/apple-touch-icon.png">
<meta name="theme-color" content="#16170f">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="{FONTS}">
<link rel="stylesheet" href="{pre}assets/css/site.css">
</head>
<body>
'''

def tail(pre):
    return f'<script src="{pre}assets/js/site.js"></script>\n</body>\n</html>\n'

def banner(pre):
    if LAUNCH: return ''
    return f'<div class="draft-banner">Draft site. Pink notes are content still needed, blue notes are design questions. <a href="{pre}notes.html">See every note on one page</a>.</div>\n'

def nav(pre, current=''):
    def a(href, label, key):
        cur = ' aria-current="page"' if key == current else ''
        return f'<a href="{href}"{cur}>{label}</a>'
    home = pre if pre else './'
    return f'''<header class="nav"><div class="wrap nav-inner">
<a class="brand" href="{home}"><img src="{pre}assets/img/logo-cream.svg" alt="" width="34" height="30">Olivia Doman</a>
<nav class="nav-links" aria-label="Main">{a(home + '#work', 'Work', 'work')}{'' if LAUNCH else a(home + '#reel', 'Reel', 'reel')}{a(home + '#about', 'About', 'about')}<a href="{pre}assets/Olivia_Doman_Resume.pdf">Resume</a>{a(home + '#contact', 'Contact', 'contact')}</nav>
</div></header>
'''

def footer(pre):
    return f'''<footer class="footer" id="contact"><div class="wrap footer-inner">
<div style="display:flex;flex-direction:column;gap:8px"><img class="footer-logo" src="{pre}assets/img/logo-cream.svg" alt="Olivia Doman monogram" width="54" height="48"><h2>Let's make something.</h2><span class="email">{EMAIL}</span></div>
<div class="footer-links"><a href="{LINKEDIN}">LinkedIn</a><a href="{GH}">GitHub</a>{'' if LAUNCH else '<a href="https://vimeo.com/927695302">Vimeo</a>'}<a href="{pre}assets/Olivia_Doman_Resume.pdf">Resume</a></div>
</div></footer>
'''

def video(pre, name, ratio='ratio-16x9', flag=None, extra=''):
    if LAUNCH: flag = None
    f = f'<span class="watermark-flag">{flag}</span>' if flag else ''
    return (f'<div class="frame {ratio} {extra}">{f}<video data-loop muted loop playsinline preload="none" '
            f'poster="{pre}assets/img/{name}-poster.jpg" aria-label="Silent loop"><source src="{pre}assets/video/{name}.mp4" type="video/mp4"></video></div>')

def image(pre, name, alt, ratio='ratio-16x9', extra=''):
    return f'<div class="frame {ratio} {extra}"><img src="{pre}assets/img/{name}" alt="{esc(alt)}" loading="lazy"></div>'

def placeholder(title, sub, ratio='ratio-16x9'):
    return f'<div class="frame placeholder {ratio}"><strong>{title}</strong><span>{sub}</span></div>'

def px_stage(pre, sid, rng=80):
    return (f'<div class="px-stage" id="{sid}" data-parallax data-range="{rng}" role="img" aria-label="Snowy forest built from three depth layers that shift with the mouse">'
            f'<div class="layer" data-f="0.10" style="background-image:url(\'{pre}assets/parallax/bg.jpg\')"></div>'
            f'<div class="layer" data-f="0.35" style="background-image:url(\'{pre}assets/parallax/layer0.webp\')"></div>'
            f'<div class="layer" data-f="0.75" style="background-image:url(\'{pre}assets/parallax/layer1.webp\')"></div></div>')

# ---------------------------------------------------------------- projects
P = {}
ORDER = ['parallax', 'spectral', 'yarn', 'charfx', 'blobs', 'flower', 'handyreader', 'diffusion', 'procedural', 'vellum', 'pupper']

def proj(slug, **kw): P[slug] = kw

proj('parallax', title='2.5D Parallax Pipeline', line='Turning a single image into a moving, layered background for LED volume stages',
     tags='Senior project · Depth estimation · Inpainting · Python')
proj('spectral', title='Spectral Path Tracer', line='A GPU path tracer that renders real light dispersion',
     tags='CS 248A · Slang · with Daniel Reichfeld')
proj('yarn', title='Crocheted Yarn Sim', line='Yarn-level physics for loose, stretchy crochet fabric',
     tags='Houdini Vellum · Simulation')
proj('charfx', title='Character Particle FX', line='A dancer dissolving into grains that trail behind at different speeds',
     tags='Houdini POPs · Vellum · Mixamo')
proj('blobs', title='Attack of the Blobs', line='Real-time soft-body physics with 100+ blobs, pegs, and a spike pit',
     tags='CS 248B · p5.js · JavaScript')
proj('flower', title='Flower Still Life', line='Sculpted, hand-textured flowers lit and rendered in Cycles',
     tags='CS 148 · Blender · Cycles')
proj('handyreader', title='HandyReader', line='American Sign Language to English subtitles, from hand keypoints',
     tags='CS 231N · PyTorch · MediaPipe · LLaMA')
proj('diffusion', title='Diffusion Models', line='Denoising, generation, and image restoration with pretrained diffusion models',
     tags='Poster · DDPM · Posterior sampling')
proj('procedural', title='Procedural Modeling', line='A reel of procedurally built geometry',
     tags='Reel · Houdini')
proj('vellum', title='Vellum Grains', line='Grains pushed by wind, colored by internal stress',
     tags='Houdini study')
proj('pupper', title='Pupper Pickleball Assistant', line='A quadruped robot that collects pickleballs on a voice command, then comes to find you',
     tags='CS 123 · ROS 2 · YOLOv5 · Team of 3')

def card_media(pre, slug, ratio):
    if slug == 'parallax': return video(pre, 'parallax', ratio)
    if slug == 'spectral': return image(pre, 'prism.jpg', 'Glass prism splitting white light into a rainbow', ratio)
    if slug == 'yarn': return video(pre, 'yarn-sphere', ratio, 'Re-render without watermark')
    if slug == 'charfx': return video(pre, 'charfx', ratio, 'Re-render without watermark')
    if LAUNCH and slug == 'handyreader': return image(pre, 'handyreader-tile.svg', 'Diagram of the 21 hand keypoints HandyReader tracks', ratio)
    if slug == 'blobs': return placeholder('Attack of the Blobs recording', '10 to 15 seconds of blobs pouring through the spike pit', ratio)
    if slug == 'flower': return image(pre, 'flower.jpg', 'Sculpted pink flowers in a glass vase by a window', ratio)
    if slug == 'handyreader': return placeholder('HandyReader demo', 'Live signing with the hand keypoint overlay', ratio)
    if slug == 'diffusion': return image(pre, 'diff-denoise.jpg', 'Noisy face and its denoised result', ratio)
    if slug == 'procedural': return placeholder('Procedural reel still', 'Frame from your Vimeo reel', ratio)
    if slug == 'vellum': return video(pre, 'vellum', ratio, 'Watermark')
    if slug == 'pupper': return video(pre, 'pupper', ratio)

# ---------------------------------------------------------------- home
def build_home(pre=''):
    pg = ('Home page', 'index.html')
    o = []
    o.append(f'''<section class="hero" id="hero-px" data-parallax data-range="70" aria-label="Introduction">
<div class="scene">
<div class="layer" data-f="0.10" style="background-image:url('{pre}assets/parallax/bg.jpg')"></div>
<div class="layer" data-f="0.35" style="background-image:url('{pre}assets/parallax/layer0.webp')"></div>
<div class="layer" data-f="0.75" style="background-image:url('{pre}assets/parallax/layer1.webp')"></div>
</div>
<div class="hero-copy"><div class="wrap"><div class="inner">
<span class="eyebrow">Software Engineer · Visual Computing</span>
<h1>Olivia Doman</h1>
<p class="lede">I build rendering, simulation, and generative AI tools for film and virtual production. Stanford Computer Science, Visual Computing.</p>
<div class="btn-row"><a class="btn solid" href="#work">See my work</a><a class="btn" href="{pre}assets/Olivia_Doman_Resume.pdf">Resume</a><a class="btn" href="#contact">Get in touch</a></div>
</div></div></div>
<span class="hero-tag">Move your mouse. This forest is my 2.5D parallax pipeline, running live.</span>
</section>
''')
    o.append('<div class="wrap" style="display:flex;flex-direction:column;gap:10px;margin-top:20px">'
             + note('q', 'Hero: should the top be this live, mouse-driven forest (current), or a silent reel highlights loop? On phones it drifts on its own.', pg)
             + note('q', 'Title: "Software Engineer, Visual Computing" (your July resume) or "Visual Computing Engineer" (your 2026 resume)? Pick one and I will match it everywhere.', pg)
             + '</div>')

    o.append('<main>')
    # Selected work
    o.append(f'<section class="section" id="work"><div class="wrap">')
    o.append('<div class="section-head"><h2 data-knot="left">Selected work</h2><span class="muted">Rendering, simulation, and FX</span></div>')
    d = P['parallax']
    o.append(f'''<a class="lead-card" href="{pre}work/parallax.html" data-knot="right">
{card_media(pre, 'parallax', 'ratio-wide')}
<div class="lead-meta"><div><span class="eyebrow">01 · Lead project</span><span class="card-title" style="font-size:clamp(32px,4vw,44px)">{d['title']}</span><span class="card-line">{d['line']}</span></div><span class="card-tags">{d['tags']}</span></div>
</a>''')
    o.append('<div class="grid-2">')
    sides = ['left', 'right', 'left', 'right', 'left', 'right']
    for i, slug in enumerate(FEATURED):
        d = P[slug]
        extra = ''
        if slug == 'blobs': extra = note('need', 'Screen recording of Attack of the Blobs. See the checklist for specs.', pg)
        if slug == 'handyreader': extra = note('need', 'Demo clip, final report, and teammates. Without the report, I would move this to More work.', pg)
        if slug in ('yarn', 'charfx'): extra = note('need', 'Clean re-render without the Houdini Apprentice watermark (Karma, Indie or Education license).', pg)
        knot = f' data-knot="{sides[i]}"' if i % 2 == 0 else ''
        o.append(f'''<div style="display:flex;flex-direction:column;gap:12px;min-width:0"><a class="card" href="{pre}work/{slug}.html"{knot}>
{card_media(pre, slug, 'ratio-16x9')}
<span class="eyebrow">{i + 2:02d}</span><span class="card-title">{d['title']}</span><span class="card-line">{d['line']}</span><span class="card-tags">{d['tags']}</span>
</a>{extra}</div>''')
    o.append('</div></div></section>')

    # Reel
    if not LAUNCH: o.append(f'''<section class="section" id="reel"><div class="wrap">
<div class="section-head"><h2 data-knot="right">Reel</h2><span class="muted">60 to 90 seconds</span></div>
{placeholder('Reel coming soon', 'Vimeo embed goes here once the reel is cut', 'ratio-16x9')}
<div style="margin-top:14px;display:flex;flex-direction:column;gap:10px">{note('need', 'The reel itself. Until it exists, I would hide this section and remove Reel from the menu.', pg)}{note('q', 'Hide the Reel section until it is ready, or keep a "coming soon" placeholder?', pg)}</div>
</div></section>''')

    # More work
    o.append('<section class="section" id="more"><div class="wrap"><div class="section-head"><h2 data-knot="left">More work</h2><span class="muted">Studies, posters, and team projects</span></div><div class="grid-4"' + (' style="grid-template-columns:repeat(2,minmax(0,1fr))"' if LAUNCH else '') + '>')
    for slug in MORE:
        d = P[slug]
        o.append(f'<a class="mini card" href="{pre}work/{slug}.html">{card_media(pre, slug, "ratio-4x3")}<span class="mini-title">{d["title"]}</span><span class="mini-tags">{d["tags"]}</span></a>')
    o.append('</div>' + '<div style="margin-top:14px">' + note('q', 'Keep Vellum Grains here? It started from an Entagma tutorial, so it is credited on its page. I would keep it only if you want more Houdini on the site.', pg) + '</div></div></section>')

    # Experience
    o.append(f'''<section class="section" id="experience"><div class="wrap">
<div class="section-head"><h2 data-knot="right">Experience</h2></div>
<div class="xp">
<div class="xp-item"><h3>Rodeo FX</h3><span class="xp-role">Software Developer Intern</span><span class="xp-date">Jul 2025 - May 2026 · Venice, CA</span>
<ul><li>Built and shipped AI-driven image and video tools inside a live, high-end VFX pipeline</li><li>Engineered custom Python and PyTorch ComfyUI nodes with API integrations for artists</li><li>Evaluated outputs with artists against production standards</li></ul></div>
<div class="xp-item"><h3>AGBO Studios</h3><span class="xp-role">Innovation Pipeline Intern</span><span class="xp-date">Jun 2024 - Sep 2024 · Los Angeles, CA</span>
<ul><li>Built pipeline automation tools for animation workflows across production teams</li><li>Worked in Maya, Unreal Engine, MetaHumans, Flow, and Rez</li><li>Presented research on emerging tools to technical and executive leadership</li></ul></div>
<div class="xp-item"><h3>Monolith Studios</h3><span class="xp-role">Student Intern</span><span class="xp-date">Aug 2022 - Sep 2023 · Los Angeles, CA</span>
<ul><li>Supported LED volume deployment for in-camera VFX</li><li>Worked hands-on with Unreal Engine real-time visualization</li><li>Attended SIGGRAPH 2022 and 2023</li></ul></div>
</div>
<div style="margin-top:16px;display:flex;flex-direction:column;gap:10px">{note('q', 'AGBO dates differ between your resumes: Sep 2024 or Dec 2024? I used Sep 2024 from your July resume.', pg)}{note('q', 'Studio work stays text only because of NDAs. Is there anything public (credits, a talk, a released project) you are allowed to link?', pg)}</div>
</div></section>''')

    # About
    o.append(f'''<section class="section" id="about"><div class="wrap about">
<div class="portrait"><img src="{pre}assets/img/headshot.jpg" alt="Portrait of Olivia Doman" loading="lazy"></div>
<div class="about-copy">
<h2 style="font-size:clamp(36px,5vw,52px);font-style:italic" data-knot="right">About</h2>
<p>I studied Computer Science at Stanford on the Visual Computing track, where I spent most of my time on rendering, simulation, and computer vision. My senior project, advised by Kayvon Fatahalian, asked how far a single image can go as a moving background for LED volume stages.</p>
<p>Outside of class I have worked where art and engineering meet: generative AI tools for artists at Rodeo FX, pipeline automation at AGBO, and virtual production at Monolith. I like building the tools that let artists move faster without giving up control.</p>
{note('need', 'This bio is a draft I wrote from your resume. Rewrite it in your own voice, or tell me what to change.', pg)}
{note('q', 'Add a personal line, like riding with the Stanford Equestrian Team? A small human detail helps recruiters remember you.', pg)}
<div class="tags"><span class="tag">Python</span><span class="tag">C++</span><span class="tag">C</span><span class="tag">JavaScript</span><span class="tag">Slang</span><span class="tag">PyTorch</span><span class="tag">Houdini</span><span class="tag">Unreal Engine</span><span class="tag">Maya</span><span class="tag">Blender</span><span class="tag">ComfyUI</span><span class="tag">USD</span></div>
</div>
</div></section>''')
    o.append('</main>')
    o.append('<div class="wrap" style="margin-top:40px;display:flex;flex-direction:column;gap:10px">'
             + note('q', 'Your phone number is on the resume PDF linked from this site. Keep it public, or should I make a version with email only?', pg)
             + note('need', 'A Vimeo profile link. The footer currently links to the Procedural Modeling video.', pg)
             + '</div>')
    o.append(footer(pre))
    return '\n'.join(o)

# ---------------------------------------------------------------- project pages
def meta_grid(items):
    items = [(k, v) for k, v in items if not v.startswith('[')]
    return '<div class="p-meta">' + ''.join(f'<div><span>{k}</span><span>{v}</span></div>' for k, v in items) + '</div>'

def section(title, body):
    return f'<section class="p-section"><h2>{title}</h2><div class="prose">{body}</div></section>'

def fig(pre, name, cap, alt=None, ratio='ratio-16x9', kind='img', extra=''):
    media = image(pre, name, alt or cap, ratio, extra) if kind == 'img' else video(pre, name, ratio, extra=extra)
    return f'<figure>{media}<figcaption>{cap}</figcaption></figure>'

def links(items):
    return '<div class="btn-row">' + ''.join(f'<a class="btn{" solid" if i == 0 else ""}" href="{h}">{t}</a>' for i, (t, h) in enumerate(items)) + '</div>'

def page(slug):
    pre = '../'
    d = P[slug]
    pg = (d['title'], f'work/{slug}.html')
    N = lambda k, t: note(k, t, pg)
    hero, meta, summary, body, lnk = '', [], '', [], []

    if slug == 'parallax':
        summary = 'Can one photo become a convincing, camera-reactive background for an LED volume stage, with no manual cleanup per shot? I built a pipeline to find out, then measured exactly where it holds up and where it breaks.'
        meta = [('Role', 'Sole researcher and engineer'), ('Course', 'CS 191W, senior project'), ('Advisor', 'Prof. Kayvon Fatahalian'), ('Tools', 'Python, OpenCV, ComfyUI, Stable Diffusion 1.5'), ('Year', '2026')]
        hero = (px_stage(pre, 'px-main', 80)
                + '<div class="px-controls" data-px-for="px-main">'
                + '<button type="button" data-range="30" aria-pressed="false" data-verdict="No visible artifacts. Production ready.">Subtle, 30px</button>'
                + '<button type="button" data-range="80" aria-pressed="true" data-verdict="Slight fringing. Fine for wide shots. This is the limit I found.">Limit, 80px</button>'
                + '<button type="button" data-range="150" aria-pressed="false" data-verdict="Cutout edges show. Watch the near trees.">Too far, 150px</button>'
                + '<span class="px-verdict">Slight fringing. Fine for wide shots. This is the limit I found.</span></div>'
                + '<p class="muted" style="margin-top:10px;font-size:14px">Move your mouse over the scene. These are the real layers from the pipeline, shifted live in your browser.</p>')
        body.append(section('The problem', '<p>LED volume stages put a digital background behind actors, and that background has to shift as the camera moves so it reads as real depth. Full 3D environments look best, but they take a long time to build.</p><p>I wanted to know how far a simpler 2.5D approach could go: estimate depth from one image, split it into layers, fill in what each layer hides, and slide the layers at different speeds.</p>'
                            '<div class="callout"><span class="eyebrow">Key finding</span><span class="big">Convincing parallax holds up to about 80px of camera movement.</span><span class="soft" style="font-size:14px">Past that, hard layer edges and inpainting seams start to show.</span></div>'))
        body.append('<section class="p-section"><h2>How it works</h2><div class="prose" style="max-width:none"><div class="steps">'
                    + f'<figure>{image(pre, "px-original.jpg", "Original single image", "ratio-wide")}<span class="n">STEP 1</span><b>Single image in</b><figcaption>One RGB photo, no 3D data</figcaption></figure>'
                    + f'<figure>{image(pre, "px-depth-anything.jpg", "Depth map from Depth Anything V2", "ratio-wide")}<span class="n">STEP 2</span><b>Estimate depth</b><figcaption>Depth Anything V2, MiDaS, ZoeDepth</figcaption></figure>'
                    + f'<figure>{image(pre, "px-layer1.jpg", "Near tree layer cut out on magenta", "ratio-wide")}<span class="n">STEP 3</span><b>Split into layers</b><figcaption>3 to 6 RGBA layers, feathered edges</figcaption></figure>'
                    + f'<figure>{image(pre, "px-inpaint.jpg", "Background with foreground inpainted away", "ratio-wide")}<span class="n">STEP 4</span><b>Fill hidden areas</b><figcaption>Stable Diffusion inpainting</figcaption></figure>'
                    + '</div><p>The layers are then composited with a different speed per depth (×0.10, ×0.35, ×0.75) and exported as video, or, as on this page, moved live in the browser.</p></div></section>')
        body.append(section('Comparing depth models', '<div class="table-wrap"><table><thead><tr><th>Model</th><th>Edge quality</th><th>Layer separation</th><th>Runtime</th></tr></thead><tbody>'
                            '<tr><td>Depth Anything V2</td><td>High, fine branches</td><td>Clean boundaries</td><td>3.2 s</td></tr>'
                            '<tr><td>MiDaS</td><td>Moderate, blurred</td><td>Noisy at edges</td><td>2.1 s</td></tr>'
                            '<tr><td>ZoeDepth</td><td>High contrast, coarse</td><td>Fragmented midground</td><td>4.8 s</td></tr></tbody></table></div>'
                            '<div class="gallery">' + fig(pre, 'px-depth-anything.jpg', 'Depth Anything V2', ratio='ratio-wide') + fig(pre, 'px-depth-midas.jpg', 'MiDaS', ratio='ratio-wide') + fig(pre, 'px-depth-zoe.jpg', 'ZoeDepth', ratio='ratio-wide') + '</div>'))
        body.append(section('Where it breaks', '<div class="compare">' + fig(pre, 'threshold-small', 'Small camera move (±25px): clean', kind='vid', ratio='ratio-wide') + fig(pre, 'threshold-large', 'Large camera move (±150px): edges and seams show', kind='vid', ratio='ratio-wide') + '</div>'
                            '<ul><li><strong>Up to 30px:</strong> no visible artifacts, production ready</li><li><strong>30 to 80px:</strong> slight edge fringing, acceptable for wide shots</li><li><strong>Past 80px:</strong> hard cutout edges, not usable</li></ul>'))
        body.append(section('Design decisions', '<ul><li><strong>Union mask inpainting.</strong> Each layer is inpainted using the union of every mask in front of it, which removes ghosted foreground objects on the background.</li><li><strong>Handheld camera path.</strong> Camera motion is built from summed harmonics, like fractional Brownian motion, so it drifts organically instead of sweeping mechanically.</li><li><strong>Edge feathering.</strong> Alpha edges get a 15px Gaussian blur before compositing to soften hard depth cuts.</li></ul>'))
        lnk = [('Read the paper', PX_REPO + '/blob/main/paper/CS191W_Paper_Doman.pdf'), ('View on GitHub', PX_REPO)]
        notes = [N('q', 'Your resume mentions real-time Unreal Engine compositing. Do you have Unreal footage? It would be the strongest proof shot on this page.'),
                 N('need', 'Two README fixes on GitHub: the clone link still says YOUR_USERNAME, and the paper link points to a file name that does not exist.'),
                 N('q', 'For the live demo: rebuild with 4 to 6 layers and a cleaner background inpaint? It would look less like cardboard cutouts.')]
    elif slug == 'spectral':
        summary = 'Most renderers treat light as a single RGB color, which makes rainbows and prism effects impossible. We extended a GPU path tracer to trace individual wavelengths of light instead.'
        meta = [('Role', '[Your part]'), ('Course', 'CS 248A, final project'), ('Team', 'With Daniel Reichfeld'), ('Tools', 'Slang, GPU path tracing'), ('Year', '[Year]')]
        hero = image(pre, 'prism.jpg', 'Rainbow fringing through a glass prism', 'ratio-wide', 'contain')
        body.append(section('What it does', '<ul><li><strong>Per-ray wavelength sampling.</strong> Each ray carries one wavelength between 380 and 700nm, kept monochromatic end to end.</li><li><strong>Dispersion.</strong> Glass index of refraction varies with wavelength using the Cauchy equation, n(λ) = A + B/λ².</li><li><strong>Spectral to RGB.</strong> CIE 1931 color matching functions convert each sample to sRGB, keeping negative values until tone mapping so they cancel correctly.</li><li><strong>Runtime toggle.</strong> Switch between spectral and RGB rendering without recompiling.</li></ul>'))
        body.append(section('Results', '<div class="gallery">' + fig(pre, 'caustic.jpg', 'Rainbow caustics: light dispersed through glass onto the ground, up to 10 refraction bounces', ratio='ratio-square', extra='contain') + fig(pre, 'sphere.jpg', 'Chromatic aberration along a glass sphere, 1024 samples per pixel', ratio='ratio-square', extra='contain') + fig(pre, 'prism-direct.jpg', 'Prism under direct light', ratio='ratio-square', extra='contain') + fig(pre, 'sphere-spectral.jpg', 'Spectral glass sphere', ratio='ratio-square', extra='contain') + '</div>'))
        body.append(section('Performance', '<p>The spectral path adds almost nothing per ray: one Cauchy evaluation and one color table lookup. The real cost is samples. Each sample now carries one wavelength instead of full RGB, so clean diffuse surfaces need about 1024 samples per pixel and clean glass caustics need 2048 to 4096.</p>'))
        lnk = [('View on GitHub', SP_REPO), ('Read the write-up', SP_REPO + '/blob/main/Spectral_PathTracer_WriteUp.pdf')]
        notes = [N('need', 'Which parts did you build, and which did Daniel? I left Role as a placeholder.'),
                 N('need', 'One long, high sample count prism or caustic render. The caustic image is still grainy.'),
                 N('q', 'Add a spectral vs. RGB side by side of the same scene? It explains the project in one glance.')]
    elif slug == 'yarn':
        summary = 'Real crochet stretches a lot because of its loose, looping structure. This simulation uses Houdini\'s Vellum solver to reproduce that behavior at the level of individual strands.'
        meta = [('Role', '[Solo or team?]'), ('Course', '[Course]'), ('Tools', 'Houdini, Vellum')]
        hero = video(pre, 'yarn-sphere', 'ratio-16x9', 'Re-render without watermark')
        body.append(section('Approach', '<p>I built the fabric from crochet stitch geometry and simulated it with Vellum constraints, drawing on research into stitch-level textiles:</p><ul><li>Guo, Lin, Narayanan, McCann. <em>Representing Crochet with Stitch Meshes</em>. SIGGRAPH.</li><li>Kaldor, James, Marschner. <em>Simulating Knitted Cloth at the Yarn Level</em>.</li><li>Ben Watts. <em>Design Through FX</em>. SIGGRAPH 2018.</li></ul>'))
        body.append(section('Tuning', '<ul><li><strong>Substeps and constraint iterations</strong> tuned for detail and stability.</li><li><strong>Stretch and bend stiffness</strong> calibrated to yarn, so the fabric keeps its shape while it drapes.</li><li><strong>Damping</strong> adjusted so it settles naturally without wobbling.</li></ul>'))
        body.append(section('What I would fix next', '<p>On the sphere, stretch stiffness had to be high to keep the fabric from sliding off, which introduced small kinks in the yarn. Bend damping reduced them, but some remain. Occasional stray strands also need parameter tweaks or smoothing after the sim.</p>'
                            + '<div class="gallery">' + fig(pre, 'yarn-flat', 'Flat drop test', kind='vid', extra='') + '</div>'))
        notes = [N('need', 'Watermark-free render with a soft yarn material and lighting.'), N('q', 'Which course was this for, and was it solo?')]
    elif slug == 'charfx':
        summary = 'A dancing figure that comes apart into grains, each trailing the motion at its own speed. Inspired by Method Studios\' AICP reel.'
        meta = [('Tools', 'Houdini, POP network'), ('Character', 'TurboSquid'), ('Animation', 'Mixamo'), ('Course', '[Course]')]
        hero = video(pre, 'charfx', 'ratio-16x9', 'Re-render without watermark')
        body.append(section('Approach', '<p>An animation deforms the character from a starting pose into a dance. I attached a POP network to the original points so particles follow the body, then shaped how they inherit its velocity.</p><p>Most of the work went into inherited velocity, delay, and drag, and into layering several characters, so the grains spread out at different rates and the shape trails off the way it does in the reference.</p>'))
        body.append(section('Reference', '<p>Method Studios\' AICP reel, the character section around 0:59 to 1:02.</p><div class="btn-row"><a class="btn" href="https://www.sidefx.com/community/method-aicp-reel/">See the reference</a></div>'))
        notes = [N('need', 'Watermark-free Karma render, ideally with a slow camera move. This could be a home page loop.'), N('q', 'Which course was this for?')]
    elif slug == 'blobs':
        summary = 'A real-time soft-body simulation where 100 or more squishy blobs pour through a field of pegs and into a spike pit.'
        meta = [('Course', 'CS 248B, Animation and Simulation'), ('Starter code', 'Prof. Doug L. James'), ('Tools', 'p5.js, JavaScript')]
        hero = placeholder('Attack of the Blobs recording', '10 to 15 seconds, recorded at full screen', 'ratio-16x9')
        body.append(section('How it works', '<p>Each blob is a ring of 15 particles held together by springs:</p><ul><li><strong>Stretch springs</strong> between neighbors keep the outline from tearing.</li><li><strong>Bend springs</strong> resist sharp folds.</li><li><strong>Area preservation</strong> pushes outward so blobs stay round instead of collapsing.</li><li><strong>Penalty contact forces</strong> with damping handle collisions with pegs, spikes, and other blobs.</li></ul><p>The challenge is stability: with 100+ blobs piling up, stiffness and damping have to be tuned so nothing explodes or tunnels through.</p>'))
        notes = [N('need', 'Screen recording of the full 100-blob run.'), N('q', 'Live, playable version here? Only if Prof. James is fine with the solution code being viewable.'), N('need', 'A note on what you added beyond the starter code.')]
    elif slug == 'flower':
        summary = 'A quiet still life of sculpted flowers by a window, modeled, textured, and lit from scratch in Blender and rendered in Cycles.'
        meta = [('Course', 'CS 148, Intro to Computer Graphics and Imaging'), ('Tools', 'Blender, Cycles'), ('Year', '2024')]
        hero = image(pre, 'flower.jpg', 'Sculpted pink flowers in a glass vase by a window', 'ratio-16x9')
        body.append(section('Modeling', '<p>I sculpted the flowers from modified spheres, shaping and placing each petal by hand, and modeled the flower centers, desk, and window from scratch. The vase is an imported asset, scaled to fit the scene.</p>'))
        body.append(section('Texturing', '<p>I UV-unwrapped the petals and hand-painted a gradient from yellow at the base to pink at the tips, then added a procedural surface texture with material nodes. The centers use a displacement map for a pollen-like surface. Wood, wall, and window materials combine image textures, displacement, and node setups.</p>'))
        body.append(section('Camera', '<p>Depth of field focuses on the flowers and lets the window and room fall softly out of focus.</p><p class="muted" style="font-size:14px">Assets: vase from Free3D; sunrise HDRI, wall, and wood textures from Poly Haven.</p>'))
        notes = [N('need', 'The untextured clay version (Variant B) for a before and after slider.'), N('q', 'There is also an earlier, darker render with a different vase. Show it as a process image, or leave it out?')]
    elif slug == 'handyreader':
        summary = 'An end-to-end system that turns signed American Sign Language sentences into English subtitles. It tracks the hands, recognizes each signed word with a recurrent network, then uses a language model to turn the words into a fluent sentence.'
        meta = [('Course', 'CS 231N, Deep Learning for Computer Vision'), ('Team', 'Olivia Doman, Arunima Srivastav, Daniel Reichfeld'), ('My part', 'Video segmentation pipeline and pose model evaluation'), ('Tools', 'PyTorch, MediaPipe Hands, LLaMA 3.2'), ('Year', '2025')]
        hero = image(pre, 'handyreader-tile.svg', 'Diagram of the 21 hand keypoints HandyReader tracks', 'ratio-16x9') if LAUNCH else placeholder('HandyReader demo', 'Live signing with the hand skeleton drawn on top', 'ratio-16x9')
        body.append(section('Results', '<div class="callout"><span class="eyebrow">Word recognition</span><span class="big">75% top-1 accuracy across a 2,000 sign vocabulary.</span><span class="soft" style="font-size:14px">78.8% at the best validation epoch. End to end, on 100 test sentences, translations kept the meaning with a bag-of-words F1 of 0.68.</span></div>'
            '<p>Most prior work recognizes fingerspelled letters or a few dozen signs. HandyReader works at the word level from continuous video, which is what full sentence translation needs.</p>'))
        body.append(section('The pipeline', '<ul><li><strong>Segment.</strong> A signed sentence video is split into word-level clips.</li><li><strong>Track.</strong> MediaPipe Hands finds the hands, the frame is cropped dynamically around them, and 21 3D keypoints are extracted per frame.</li><li><strong>Recognize.</strong> A GRU classifies each clip\'s keypoint sequence into an ASL gloss, the written label for a sign.</li><li><strong>Translate.</strong> LLaMA 3.2 turns the gloss sequence into an English sentence, so <strong>STORE I GO YESTERDAY</strong> becomes <strong>"I went to the store yesterday."</strong></li></ul>'))
        body.append(section('The model', '<p>Each clip is 32 frames of 21 joints in 3D, flattened to 63 values per frame. A two-layer GRU with 128 hidden units reads the sequence, and its final hidden state goes through batch normalization, dropout, and a linear layer to pick one of 2,000 signs.</p><p>We chose a GRU because signs are defined by motion over time, and GRUs capture that while staying lighter and faster to train than LSTMs. It clearly beat a 1D convolutional baseline.</p>'
            '<p>The dataset has 60,000 sequences, balanced at 40 training, 5 validation, and 5 test samples per sign. To make the model robust to different signers, training data was augmented with jitter, noise, spatial shifts, and time warping between 0.75 and 1.25 times speed, then smoothed over time with a Gaussian filter.</p>'))
        body.append('<section class="p-section wide"><h2>What it learned</h2><div class="prose" style="max-width:none">'
            '<div class="compare">' + fig(pre, 'hr-loss.png', 'Training and validation loss', ratio='ratio-4x3', extra='paper') + fig(pre, 'hr-accuracy.png', 'Validation accuracy by epoch', ratio='ratio-4x3', extra='paper') + '</div>'
            '<p>The most confused pairs tell the story. Early in training, mistakes were random, like PARENTS for HIPPOPOTAMUS. By epoch 3, the model only confused signs that look or mean alike, such as TEACHER and PROFESSOR, or JOURNEY and TRIP. A few pairs, like SKETCH and DRAW or SKILL and TALENT, stayed hard throughout, because the signs themselves are nearly identical.</p>'
            '<div class="compare">' + fig(pre, 'hr-confusion-01.png', 'Most confused signs, epoch 1: unrelated pairs', ratio='ratio-square', extra='paper') + fig(pre, 'hr-confusion-16.png', 'Most confused signs, epoch 16: similar signs only', ratio='ratio-square', extra='paper') + '</div></div></section>')
        body.append(section('My part', '<p>I built the pipeline that segments continuous signing into sentences and words, which made it possible to evaluate the system at both levels. I also ran the early evaluation of pose extractors, comparing MediaPipe Hands and ViTPose, which set the keypoint approach the final model is built on.</p><p class="muted" style="font-size:14px">Arunima Srivastav led the GRU classifier and training pipeline. Daniel Reichfeld built the first classifier versions and the LLaMA translation script.</p>'))
        notes = [N('q', 'A short demo clip would still help: the hand skeleton tracking a few signs. Want a script to record one?')]
    elif slug == 'diffusion':
        summary = 'Diffusion models generate images by learning to reverse a gradual noise process. This project explores how pretrained diffusion models handle denoising, generating faces from pure noise, and restoring damaged images.'
        meta = [('Course', '[Course]'), ('Tools', 'PyTorch, pretrained DDPM'), ('Format', 'Research poster')]
        hero = image(pre, 'diff-denoise.jpg', 'Single step denoising: noisy input and clean output', 'ratio-wide', 'contain')
        body.append(section('Approach', '<p>In the forward process, noise is added until an image is pure noise. A network learns to predict that noise at each step, and sampling runs the process backward to recover a clean image. For inpainting and deblurring, Diffusion Posterior Sampling keeps each step consistent with the damaged input.</p>'))
        body.append(section('Results', '<div class="gallery">' + fig(pre, 'diff-denoise.jpg', 'Single step denoising with a pretrained DDPM. PSNR 32.55, LPIPS 0.093.', ratio='ratio-wide', extra='contain') + fig(pre, 'diff-sample.jpg', '1000-step sample from pure Gaussian noise', ratio='ratio-square', extra='contain') + fig(pre, 'diff-inpaint.jpg', 'Inpainting with SDEdit: the masked box is filled with realistic skin and eye', ratio='ratio-wide', extra='contain') + fig(pre, 'diff-deblur.jpg', 'Deblurring a Gaussian blur: core facial structure recovered', ratio='ratio-wide', extra='contain') + '</div>'
                            '<div class="table-wrap"><table><thead><tr><th>Noise steps</th><th>300</th><th>500</th><th>700</th></tr></thead><tbody><tr><td>PSNR</td><td>25.72</td><td>29.58</td><td>30.91</td></tr><tr><td>LPIPS</td><td>0.122</td><td>0.087</td><td>0.088</td></tr></tbody></table></div>'
                            '<div class="table-wrap"><table><thead><tr><th>Method</th><th>SDEdit t=500</th><th>ScoreALD [10, 20]</th><th>ScoreALD [20, 10]</th></tr></thead><tbody><tr><td>PSNR</td><td>20.14</td><td>23.13</td><td>19.49</td></tr><tr><td>LPIPS</td><td>0.445</td><td>0.354</td><td>0.341</td></tr></tbody></table></div>'))
        notes = [N('q', 'Which course was this poster for? And please confirm which result each table belongs to; I matched them by position on the poster.'), N('need', 'If you reuse the poster file: fix "Postier" to "Posterior" and "NuerIPS" to "NeurIPS".')]
    elif slug == 'procedural':
        summary = 'A reel of procedurally modeled geometry.'
        meta = [('Course', '[Course]'), ('Tools', 'Houdini')]
        hero = placeholder('Procedural Modeling reel', 'Embed from Vimeo on the live site', 'ratio-16x9')
        body.append(section('Watch', '<p>The full reel is on Vimeo.</p><div class="btn-row"><a class="btn solid" href="https://vimeo.com/927695302">Watch on Vimeo</a></div>'))
        notes = [N('need', 'A short description of what is in the reel, which course it was for, and a still frame or original file.')]
    elif slug == 'vellum':
        summary = 'Vellum grains pushed around by wind forces, colored by the stress between neighboring particles as they move.'
        meta = [('Tools', 'Houdini, Vellum, POP solvers'), ('Based on', 'Entagma abstract particles tutorial')]
        hero = video(pre, 'vellum', 'ratio-16x9', 'Watermark')
        body.append(section('Approach', '<p>Vellum constraints handle how grains interact with each other, while POP solvers add wind and other forces at the particle level. Color comes from a stress attribute: how much the distance between neighboring particles changes as they move.</p><p class="muted" style="font-size:14px">Started from an Entagma tutorial on abstract particles.</p>'))
        notes = [N('q', 'Keep this study on the site, or cut it?')]
    elif slug == 'pupper':
        summary = 'A pickleball assistant built on Stanford\'s Pupper quadruped robot. Say "Pupper, retrieve" and it searches for every ball on the court, scoops each one into a rolling collector cage, then turns to find you and brings them back.'
        meta = [('Course', 'CS 123, robotics'), ('Team', 'Avery Voss, Olivia Doman, Will Jenkins'), ('Tools', 'ROS 2, Python, YOLOv5 on a Hailo accelerator, OpenAI Realtime API'), ('Year', '2025')]
        hero = video(pre, 'pupper', 'ratio-16x9')
        body.append(section('The system', '<p>Pupper runs three pieces that talk to each other over ROS 2:</p><ul>'
            '<li><strong>Vision.</strong> Each camera frame is unwrapped from fisheye to equirectangular, then YOLOv5 runs on a Hailo AI accelerator on the robot, detecting balls and people and publishing their bounding boxes.</li>'
            '<li><strong>Behavior.</strong> A state machine running at 10 Hz turns those detections into motion commands.</li>'
            '<li><strong>Voice.</strong> Microphone audio streams to OpenAI\'s Realtime API, along with a camera snapshot for context. The model replies with a fixed set of action phrases, so "retrieve balls" becomes one clear command the robot can act on.</li></ul>'))
        body.append('<section class="p-section"><h2>How it decides what to do</h2><div class="prose" style="max-width:none">'
            '<div class="table-wrap"><table><thead><tr><th>State</th><th>What Pupper does</th><th>Moves on when</th></tr></thead><tbody>'
            '<tr><td>Search</td><td>Turns in place at 0.5 rad/s, toward the side it last saw a ball</td><td>A ball appears</td></tr>'
            '<tr><td>Track</td><td>Walks at 0.3 m/s while a proportional controller keeps the ball centered</td><td>The ball reaches the bottom of the frame</td></tr>'
            '<tr><td>Collect</td><td>Walks forward for 2.5 seconds, rolling the ball into the collector cage it pushes</td><td>Time is up, then it searches again</td></tr>'
            '<tr><td>Hand off</td><td>After 15 seconds with no ball in sight, decides it has found them all and barks</td><td>Switches to tracking a person</td></tr>'
            '<tr><td>Follow</td><td>Finds and walks toward the nearest person</td><td>The person fills 60% of the frame, then it stops</td></tr>'
            '</tbody></table></div>'
            '<p>To keep it locked onto the same ball when several are in view, it always picks the detection closest to where its target was in the last frame.</p></div></section>')
        body.append('<section class="p-section"><h2>Watch a full run</h2><div class="prose" style="max-width:none">'
            f'<div class="frame ratio-16x9"><video controls playsinline preload="none" poster="{pre}assets/img/pupper-full-poster.jpg"><source src="{pre}assets/video/pupper-full.mp4" type="video/mp4"></video></div>'
            '<p class="muted" style="font-size:14px">Unedited, about a minute and a half: searching, collecting three balls, then bringing them back.</p>'
            '<div class="gallery">' + fig(pre, 'pupper-return', 'Bringing the full cage back to a person', kind='vid') + fig(pre, 'pupper', 'Turning toward a ball and scooping it into the cage', kind='vid') + '</div></div></section>')
        body.append(section('Tuning it on the court', '<p>Early versions overshot the ball, so we slowed tracking from 0.75 to 0.3 m/s and tuned the steering gain until it held a ball steadily in the center. Detection on the robot has to be fast enough to keep up with walking, which is why it runs on the Hailo accelerator instead of the main processor.</p><p>Pupper also has a bit of personality: it barks when it starts and when it finishes, and can wiggle and bob on command.</p>'))
        lnk = [('View on GitHub', PUP_REPO)]
        notes = [N('need', 'One short clip of Pupper finding a ball.'), N('need', 'Which parts you built.'), N('q', 'Keep this on the site? It shows range, but it is the furthest from graphics and VFX roles.')]

    live = LIVE_ORDER
    i = live.index(slug)
    nxt = live[(i + 1) % len(live)]
    o = [nav(pre, 'work')]
    o.append(f'<main class="wrap"><div class="p-head"><a class="back" href="../#work">Back to all work</a><h1>{d["title"]}</h1><p class="p-summary">{summary}</p></div>')
    o.append(meta_grid(meta))
    o.append(hero)
    o.append('<div style="display:flex;flex-direction:column;gap:10px;margin-top:20px">' + ''.join(notes) + '</div>')
    o.append('<div class="p-body">' + ''.join(body) + '</div>')
    if lnk: o.append('<div style="margin-top:clamp(48px,6vw,72px)">' + links(lnk) + '</div>')
    o.append(f'<nav class="next" aria-label="More projects"><a class="btn" href="../#work">All work</a><a class="next-link" href="{nxt}.html"><span class="muted" style="font-size:13px">Next project</span><span class="next-title">{P[nxt]["title"]}</span></a></nav>')
    o.append('</main>')
    o.append(footer(pre))
    return '\n'.join(o)

# ---------------------------------------------------------------- notes page
GLOBAL = [
    ('need', 'Clean, watermark-free Houdini re-renders (yarn sim and character FX at minimum). Check for a Stanford Houdini Education license or use Houdini Indie.'),
    ('need', 'Domain: transfer oliviadoman.com to Cloudflare and cancel the WordPress plan before it renews on November 23, 2026.'),
    ('q', 'Fonts: Cormorant Garamond for headings and Karla for text. Keep, or try something sharper?'),
    ('q', 'Dark only, or add a light version that follows the visitor\'s system setting?'),
    ('q', 'Card hover: images lift and their shadow grows. Too much, or just right?'),
]

def build_notes(pre=''):
    groups = {}
    for title, href, kind, text in ALL_NOTES:
        groups.setdefault((title, href), []).append((kind, text))
    need = sum(1 for n in ALL_NOTES if n[2] == 'need') + sum(1 for k, _ in GLOBAL if k == 'need')
    q = len(ALL_NOTES) + len(GLOBAL) - need
    o = [nav(pre)]
    o.append(f'<main class="wrap"><div class="p-head"><a class="back" href="./">Back to the site</a><h1>Draft notes</h1><p class="p-summary">Everything still needed before launch, and every design question, in one list. {need} items needed, {q} questions.</p></div>')
    o.append('<div class="notes-list">')
    o.append('<section class="notes-group"><h2>Whole site</h2><ul>' + ''.join(f'<li><span class="kind {"q" if k == "q" else "need"}">{"Question" if k == "q" else "Needed"}</span><span>{t}</span></li>' for k, t in GLOBAL) + '</ul></section>')
    for (title, href), items in groups.items():
        o.append(f'<section class="notes-group"><h2><a href="{href}">{title}</a></h2><ul>' + ''.join(f'<li><span class="kind {"q" if k == "q" else "need"}">{"Question" if k == "q" else "Needed"}</span><span>{t}</span></li>' for k, t in items) + '</ul></section>')
    o.append('</div></main>')
    o.append(footer(pre))
    return '\n'.join(o)

# ---------------------------------------------------------------- write
def write(path, s):
    full = os.path.join(OUT, path)
    os.makedirs(os.path.dirname(full) or OUT, exist_ok=True)
    with open(full, 'w') as f: f.write(s)

home_body = build_home('')
LIVE_ORDER = ['parallax'] + FEATURED + MORE
pages = {s: page(s) for s in LIVE_ORDER}
notes_body = build_notes('')

DESC = 'Olivia Doman, software engineer in visual computing: rendering, simulation, and generative AI tools for film and virtual production.'
write('index.html', head('Olivia Doman', DESC, '') + banner('') + nav('') + home_body + tail(''))
art = (f'<title>Olivia Doman</title>\n<link rel="icon" type="image/svg+xml" href="assets/img/favicon.svg">\n<link rel="stylesheet" href="{FONTS}">\n<link rel="stylesheet" href="assets/css/site.css">\n'
       + banner('') + nav('') + home_body + tail('').replace('</body>\n</html>\n', ''))
write('index.artifact.html', art)
for s, b in pages.items():
    write(f'work/{s}.html', head(f'{P[s]["title"]} · Olivia Doman', P[s]['line'], '../') + banner('../') + b + tail('../'))
if not LAUNCH: write('notes.html', head('Draft notes · Olivia Doman', 'Content still needed and open design questions', '') + nav('') + notes_body + tail(''))
print('notes:', len(ALL_NOTES) + len(GLOBAL))
