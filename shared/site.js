/* Plots – Shared Site JavaScript */

(function() {
    'use strict';

    function injectNavBar() {
        if (document.querySelector('.nav-bar')) return;

        const isRoot = document.body.dataset.page === 'home';
        if (isRoot) return;

        const nav = document.createElement('div');
        nav.className = 'nav-bar';
        nav.innerHTML = '<a href="../">&larr; Back to Plots</a>';
        document.body.insertBefore(nav, document.body.firstChild);
    }

    function initTheme() {
        const saved = localStorage.getItem('theme') || 'light';
        document.documentElement.setAttribute('data-theme', saved);

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

    function init() {
        injectNavBar();
        initTheme();
    }

    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', init);
    } else {
        init();
    }
})();
