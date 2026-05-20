"use strict";

/**
 * Unified Dashboard — manifest-driven synchronized atlas view.
 *
 * Offline-safe: the page only loads local manifest/CSV assets and renders the
 * dashboard with inline SVG primitives so it works without a remote runtime.
 */

const COLORS = [
  '#60a5fa', '#f472b6', '#34d399', '#e8eaf6', '#f59e0b',
  '#a78bfa', '#22c55e', '#fb7185',
];

const SVG_NS = 'http://www.w3.org/2000/svg';
const MARGIN = { top: 24, right: 36, bottom: 56, left: 150 };
const LANE_HEIGHT = 80;
const LANE_GAP = 20;
const WIDTH = 1400 - MARGIN.left - MARGIN.right;
const TIME_DOMAIN = [-1000000, 2030];
const TIME_CONSTANT = 1000;
const AXIS_TICKS = [-1000000, -100000, -10000, -1000, -100, -10, 0, 10, 100, 1000, 2030];

function loadText(url) {
  return fetch(url).then((response) => {
    if (!response.ok) {
      throw new Error(`${url}: ${response.status}`);
    }
    return response.text();
  });
}

function parseCSV(text) {
  const rows = [];
  let row = [];
  let cell = '';
  let inQuotes = false;
  let i = 0;
  const input = text.replace(/^\uFEFF/, '');

  function pushCell() {
    row.push(cell);
    cell = '';
  }

  function pushRow() {
    if (row.length) {
      rows.push(row);
    }
    row = [];
  }

  while (i < input.length) {
    const char = input[i];
    const next = input[i + 1];

    if (inQuotes) {
      if (char === '"' && next === '"') {
        cell += '"';
        i += 2;
        continue;
      }
      if (char === '"') {
        inQuotes = false;
        i += 1;
        continue;
      }
      cell += char;
      i += 1;
      continue;
    }

    if (char === '"') {
      inQuotes = true;
      i += 1;
      continue;
    }

    if (char === ',') {
      pushCell();
      i += 1;
      continue;
    }

    if (char === '\n') {
      pushCell();
      pushRow();
      i += 1;
      continue;
    }

    if (char === '\r') {
      i += 1;
      continue;
    }

    cell += char;
    i += 1;
  }

  pushCell();
  pushRow();

  if (!rows.length) {
    return [];
  }

  const headers = rows.shift().map((header) => header.trim());
  return rows
    .filter((values) => values.some((value) => value.trim() !== ''))
    .map((values) => {
      const record = {};
      headers.forEach((header, index) => {
        record[header] = (values[index] ?? '').trim();
      });
      return record;
    });
}

function formatYearLabel(year) {
  if (!Number.isFinite(year)) {
    return 'Unknown year';
  }
  const rounded = Math.round(year);
  if (rounded < 0) {
    return `${Math.abs(rounded).toLocaleString()} BCE`;
  }
  if (rounded === 0) {
    return '0';
  }
  return rounded.toLocaleString();
}

function symlog(value, constant = TIME_CONSTANT) {
  return Math.sign(value) * Math.log1p(Math.abs(value) / constant);
}

function createScale(domainMin, domainMax, rangeMin, rangeMax, constant = TIME_CONSTANT) {
  const transformedMin = symlog(domainMin, constant);
  const transformedMax = symlog(domainMax, constant);
  const span = transformedMax - transformedMin || 1;

  return (value) => {
    const transformedValue = symlog(value, constant);
    const normalized = (transformedValue - transformedMin) / span;
    return rangeMin + normalized * (rangeMax - rangeMin);
  };
}

function createSvgElement(tagName, attrs = {}) {
  const element = document.createElementNS(SVG_NS, tagName);
  Object.entries(attrs).forEach(([key, value]) => {
    if (value !== undefined && value !== null) {
      element.setAttribute(key, String(value));
    }
  });
  return element;
}

function appendText(parent, text, attrs = {}) {
  const node = createSvgElement('text', attrs);
  node.textContent = text;
  parent.appendChild(node);
  return node;
}

function loadManifest() {
  return loadText('../plots_manifest.json').then((text) => JSON.parse(text)
    .filter((entry) => entry.status === 'published' && entry.kind !== 'dashboard')
    .sort((a, b) => a.order - b.order));
}

function loadCSV(url) {
  return loadText(url).then(parseCSV);
}

function parseYear(row) {
  const raw = row.year ?? row.Year ?? row.Years_Ago ?? row.date;
  if (raw === null || raw === undefined || raw === '') {
    return null;
  }
  if (row.Years_Ago !== undefined && row.Years_Ago !== null && row.Years_Ago !== '') {
    const yearsAgo = Number.parseFloat(String(raw).trim());
    return Number.isFinite(yearsAgo) ? 2026 - yearsAgo : null;
  }
  const parsed = Number.parseFloat(String(raw).trim());
  return Number.isFinite(parsed) ? parsed : null;
}

function eventName(row) {
  return row.event || row.Event || row.Model || row.name || row.label || row.Benchmark || 'Event';
}

function laneTitle(entry) {
  return entry.short_title || entry.title;
}

function laneLabel(entry) {
  return `${entry.title} (${entry.short_title || entry.title})`;
}

function renderError(container, message) {
  const error = document.createElement('p');
  error.className = 'error';
  error.textContent = message;
  container.innerHTML = '';
  container.appendChild(error);
}

function renderDashboard(entriesWithData) {
  const container = document.getElementById('dashboard-container');
  container.innerHTML = '';

  const intro = document.createElement('section');
  intro.className = 'dashboard-notice';
  intro.innerHTML = '<strong>Offline-safe dashboard</strong> — local manifest and CSV files only. No remote runtime assets are required.';
  container.appendChild(intro);

  const totalHeight = entriesWithData.length * (LANE_HEIGHT + LANE_GAP) + MARGIN.top + MARGIN.bottom;
  const svgWidth = WIDTH + MARGIN.left + MARGIN.right;
  const svg = createSvgElement('svg', {
    viewBox: `0 0 ${svgWidth} ${totalHeight}`,
    width: svgWidth,
    height: totalHeight,
    role: 'img',
    'aria-label': 'Unified dashboard of published Exponential Progress Atlas timelines',
  });
  svg.style.display = 'block';

  const xScale = createScale(TIME_DOMAIN[0], TIME_DOMAIN[1], 0, WIDTH);
  const tooltip = document.createElement('div');
  tooltip.className = 'tooltip';
  tooltip.setAttribute('role', 'status');
  tooltip.setAttribute('aria-live', 'polite');
  document.body.appendChild(tooltip);

  entriesWithData.forEach((entry, index) => {
    const laneY = MARGIN.top + index * (LANE_HEIGHT + LANE_GAP);
    const lane = createSvgElement('g', {
      transform: `translate(${MARGIN.left}, ${laneY})`,
      role: 'group',
      'aria-label': laneLabel(entry),
    });

    lane.appendChild(createSvgElement('rect', {
      width: WIDTH,
      height: LANE_HEIGHT,
      rx: 10,
      fill: '#161922',
      stroke: '#2d3148',
    }));

    appendText(lane, laneTitle(entry), {
      class: 'lane-title',
      x: -12,
      y: LANE_HEIGHT / 2,
      'text-anchor': 'end',
      'dominant-baseline': 'middle',
      fill: COLORS[index % COLORS.length],
    });

    const events = entry.data
      .map((datum) => {
        const year = parseYear(datum);
        return year === null ? null : { ...datum, year };
      })
      .filter(Boolean)
      .sort((a, b) => a.year - b.year);

    events.forEach((event) => {
      const speculative = String(event.estimate_status || event.Impact || '').toLowerCase().includes('speculative');
      const cx = xScale(event.year);
      const cy = LANE_HEIGHT / 2;
      const circle = createSvgElement('circle', {
        class: 'event-dot',
        cx,
        cy,
        r: speculative ? 5 : 4,
        fill: COLORS[index % COLORS.length],
        opacity: speculative ? 0.55 : 0.85,
        tabindex: 0,
        'aria-label': `${eventName(event)} — ${entry.title} — ${formatYearLabel(event.year)}`,
      });

      const showTooltip = (clientX, clientY) => {
        tooltip.innerHTML = `<strong>${eventName(event)}</strong><br>${entry.title}<br>Year: ${formatYearLabel(event.year)}`;
        tooltip.style.left = `${clientX + 12}px`;
        tooltip.style.top = `${clientY - 8}px`;
        tooltip.style.opacity = '1';
      };

      const hideTooltip = () => {
        tooltip.style.opacity = '0';
      };

      circle.addEventListener('mouseenter', (eventLike) => {
        circle.setAttribute('r', speculative ? '7' : '6');
        circle.setAttribute('opacity', '1');
        showTooltip(eventLike.pageX, eventLike.pageY);
      });
      circle.addEventListener('mousemove', (eventLike) => {
        showTooltip(eventLike.pageX, eventLike.pageY);
      });
      circle.addEventListener('mouseleave', () => {
        circle.setAttribute('r', speculative ? '5' : '4');
        circle.setAttribute('opacity', speculative ? '0.55' : '0.85');
        hideTooltip();
      });
      circle.addEventListener('focus', () => {
        showTooltip(window.innerWidth / 2, window.scrollY + laneY + 20);
      });
      circle.addEventListener('blur', hideTooltip);

      lane.appendChild(circle);
    });

    if (index === entriesWithData.length - 1) {
      const axisY = LANE_HEIGHT;
      lane.appendChild(createSvgElement('line', {
        x1: 0,
        x2: WIDTH,
        y1: axisY,
        y2: axisY,
        stroke: '#2d3148',
      }));

      AXIS_TICKS.forEach((tickValue) => {
        if (tickValue < TIME_DOMAIN[0] || tickValue > TIME_DOMAIN[1]) {
          return;
        }
        const x = xScale(tickValue);
        lane.appendChild(createSvgElement('line', {
          x1: x,
          x2: x,
          y1: axisY,
          y2: axisY + 6,
          stroke: '#2d3148',
        }));
        appendText(lane, formatYearLabel(tickValue), {
          x,
          y: axisY + 22,
          'text-anchor': 'middle',
          fill: '#94a3b8',
          'font-size': 11,
        });
      });

      appendText(lane, 'Time (symlog years)', {
        x: WIDTH / 2,
        y: axisY + 42,
        'text-anchor': 'middle',
        fill: '#9ca3af',
        'font-size': 13,
      });
    }

    svg.appendChild(lane);
  });

  container.appendChild(svg);
}

function initDashboard() {
  const container = document.getElementById('dashboard-container');

  loadManifest()
    .then((entries) => Promise.all(
      entries.map((entry) => loadCSV(`../${entry.data}`).then((data) => ({
        ...entry,
        data,
      }))),
    ))
    .then(renderDashboard)
    .catch((error) => {
      console.error('Failed to load dashboard data:', error);
      renderError(container, 'Error loading dashboard data. Ensure the manifest and CSV files are accessible locally.');
    });
}

if (document.readyState === 'loading') {
  document.addEventListener('DOMContentLoaded', initDashboard);
} else {
  initDashboard();
}
