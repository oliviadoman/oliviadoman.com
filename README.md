# oliviadoman.com

Personal portfolio of Olivia Doman, Software Engineer, Visual Computing.

A static site: plain HTML, CSS, and JavaScript, with no build step needed to deploy.

## Structure

- `index.html`: home page, with the live 2.5D parallax forest at the top
- `work/`: one page per project
- `assets/css/site.css`: all styles
- `assets/js/site.js`: parallax hero, video loops
- `assets/img/`, `assets/video/`, `assets/parallax/`: media
- `assets/Olivia_Doman_Resume.pdf`: resume linked from the site
- `tools/build_site.py`: optional generator that rebuilds the HTML pages from one file of project content

## Deploy

Hosted on Cloudflare Pages, connected to this repository. Every push to `main` publishes automatically.

Settings: framework preset "None", build command empty, output directory `/`.

## Updating

Edit the HTML directly, or change the project text in `tools/build_site.py` and run:

```
python3 tools/build_site.py . launch
```
