# Agent 2 — Homepage + Shared Site Upgrade

## Goal
Redesign the homepage and upgrade `shared/site.css` + `shared/site.js` for dark mode, better cards, and cleaner navigation. This is primarily HTML/CSS/JS work — no Python.

## Working directory
`/Users/mschwar/plots`

## Context
This is a GitHub Pages site with 6 data visualization plots. The current site uses a plain light theme. One of the plots (`model-sizes`) has a dark-themed D3 chart. We want to:
1. Add a dark mode toggle that persists via localStorage
2. Improve the homepage card grid (better stats, better spacing)
3. Fix a fragile nav detection bug in `site.js`
4. Improve mobile layout

**Read these files before starting:**
- `/Users/mschwar/plots/index.html`
- `/Users/mschwar/plots/shared/site.css`
- `/Users/mschwar/plots/shared/site.js`
- `/Users/mschwar/plots/adoption-timeline/index.html` (sample subpage)

---

## Task 2A: `shared/site.css` — Dark mode + design improvements

### Add dark mode CSS variables
The current `:root` block uses light colors. Add a `[data-theme="dark"]` block:

```css
[data-theme="dark"] {
    --color-bg: #0f1117;
    --color-surface: #1c1f2e;
    --color-text: #e8eaf6;
    --color-text-muted: #9ca3af;
    --color-link: #60a5fa;
    --color-border: #2d3148;
    --color-highlight-bg: #1e1a2e;
    --color-highlight-border: #4c3880;
    --shadow: 0 2px 8px rgba(0,0,0,0.4);
}
```

### Improve card design
Current cards are plain boxes. Upgrade:
- Add a subtle gradient top border on hover (use `::before` pseudo-element)
- Increase card border-radius to 14px
- Add `border: 1px solid var(--color-border)` so cards have visible edges in dark mode
- Add a `.card-stat` class: large bold number, small muted label beneath it — used to show the key headline number for each plot

### Dark mode toggle button
Add a `.theme-toggle` button style:
```css
.theme-toggle {
    position: fixed;
    top: 16px;
    right: 16px;
    background: var(--color-surface);
    border: 1px solid var(--color-border);
    border-radius: 20px;
    padding: 6px 14px;
    cursor: pointer;
    font-size: 13px;
    color: var(--color-text);
    z-index: 100;
    transition: background 0.2s;
}
```

### Mobile fix
The current breakpoint at 600px jumps from 3-col to 1-col. Add an intermediate:
```css
@media (max-width: 900px) {
    .cards { grid-template-columns: repeat(2, 1fr); }
}
@media (max-width: 560px) {
    .cards { grid-template-columns: 1fr; }
}
```

Remove the existing `@media (max-width: 600px)` `.links` and table rules and rewrite them more cleanly.

---

## Task 2B: `shared/site.js` — Fix nav + add dark mode logic

### Fix fragile nav detection
The current code does:
```js
const isSubpage = window.location.pathname.includes('/plots/') && ...
```
This breaks on local file:// URLs and custom domains. Replace with:
```js
// Inject nav on any page that isn't the root index
const isRoot = document.body.dataset.page === 'home';
if (!isRoot) { /* inject nav */ }
```

### Add dark mode toggle logic
```js
function initTheme() {
    const saved = localStorage.getItem('theme') || 'light';
    document.documentElement.setAttribute('data-theme', saved);
    // Create toggle button
    const btn = document.createElement('button');
    btn.className = 'theme-toggle';
    btn.setAttribute('aria-label', 'Toggle dark mode');
    btn.textContent = saved === 'dark' ? '☀ Light' : '☾ Dark';
    btn.addEventListener('click', () => {
        const next = document.documentElement.getAttribute('data-theme') === 'dark' ? 'light' : 'dark';
        document.documentElement.setAttribute('data-theme', next);
        localStorage.setItem('theme', next);
        btn.textContent = next === 'dark' ? '☀ Light' : '☾ Dark';
    });
    document.body.appendChild(btn);
}
```
Call `initTheme()` in the DOM ready handler.

---

## Task 2C: `index.html` — Homepage improvements

### Add `data-page="home"` to body tag
```html
<body data-page="home">
```

### Add key stat to each card
Inside each `.card-content`, add a `.card-stat` div after `<h2>`:
- Plot 1 (AI Compute): `<div class="card-stat"><span class="stat-number">10²⁷</span><span class="stat-label">FLOPs frontier 2026</span></div>`
- Plot 2 (Adoption): `<div class="card-stat"><span class="stat-number">60×</span><span class="stat-label">faster adoption since 1969</span></div>`
- Plot 3 (Energetic): `<div class="card-stat"><span class="stat-number">10⁶×</span><span class="stat-label">efficiency gain per dollar</span></div>`
- Plot 4 (Civilization): `<div class="card-stat"><span class="stat-number">1M yrs</span><span class="stat-label">of infrastructure stacking</span></div>`
- Plot 5 (Energy Leverage): `<div class="card-stat"><span class="stat-number">17×</span><span class="stat-label">metabolic baseline 2024</span></div>`
- Plot 6 (Model Sizes): `<div class="card-stat"><span class="stat-number">3,000×</span><span class="stat-label">param growth since 2019</span></div>`

Add CSS for `.card-stat` in site.css:
```css
.card-stat {
    display: flex;
    flex-direction: column;
    margin: 0.25rem 0 0.75rem;
}
.stat-number {
    font-size: 1.6rem;
    font-weight: 700;
    color: var(--color-link);
    line-height: 1;
}
.stat-label {
    font-size: 0.75rem;
    color: var(--color-text-muted);
    margin-top: 2px;
}
```

### Update subtitle
Change "Six" to "Six" (already done) — verify it says "Six interactive timelines".

### Add `data-page="home"` to the body tag.

---

## Constraints
- Keep the light theme as default — dark mode is opt-in via toggle
- Don't break the existing subpage nav bar behavior
- Don't add any external dependencies (no extra CDN links)
- Test that the CSS variables cascade correctly for both themes

## Done when
- `site.css` has dark mode variables, `.card-stat` styles, `.theme-toggle` styles, improved mobile breakpoints
- `site.js` has theme toggle logic + fixed nav detection
- `index.html` has card stats for all 6 plots, `data-page="home"` on body
- All subpage `index.html` files (adoption-timeline, ai-compute-timeline, etc.) still work with the nav bar
