/**
 * Unified Dashboard — manifest-driven synchronized atlas view.
 */

const COLORS = [
  '#60a5fa', '#f472b6', '#34d399', '#e8eaf6', '#f59e0b',
  '#a78bfa', '#22c55e', '#fb7185'
];

const MARGIN = { top: 20, right: 40, bottom: 40, left: 150 };
const LANE_HEIGHT = 80;
const WIDTH = 1400 - MARGIN.left - MARGIN.right;
const TIME_DOMAIN = [-1000000, 2030];

async function loadText(url) {
  const response = await fetch(url);
  if (!response.ok) {
    throw new Error(`${url}: ${response.status}`);
  }
  return response.text();
}

async function loadManifest() {
  const text = await loadText('../plots_manifest.json');
  return JSON.parse(text)
    .filter(entry => entry.status === 'published' && entry.kind !== 'dashboard')
    .sort((a, b) => a.order - b.order);
}

async function loadCSV(url) {
  return d3.csvParse(await loadText(url));
}

function parseYear(row) {
  const raw = row.year || row.Year || row.Years_Ago || row.date;
  if (!raw) return null;
  if (row.Years_Ago) return 2026 - parseFloat(raw);
  const value = parseFloat(String(raw).slice(0, 4));
  return Number.isFinite(value) ? value : null;
}

function eventName(row) {
  return row.event || row.Event || row.Model || row.name || row.label || row.Benchmark || 'Event';
}

function initDashboard() {
  const container = d3.select('#dashboard-container');
  const tooltip = d3.select('body').append('div').attr('class', 'tooltip');

  const totalHeight = 8 * (LANE_HEIGHT + 20) + MARGIN.top + MARGIN.bottom;
  const svg = container.append('svg')
    .attr('viewBox', `0 0 ${WIDTH + MARGIN.left + MARGIN.right} ${totalHeight}`)
    .attr('role', 'img')
    .attr('aria-label', 'Unified dashboard of published Exponential Progress Atlas timelines');

  const g = svg.append('g')
    .attr('transform', `translate(${MARGIN.left},${MARGIN.top})`);

  const xScale = d3.scaleSymlog()
    .domain(TIME_DOMAIN)
    .range([0, WIDTH])
    .constant(1000);

  loadManifest()
    .then(entries => Promise.all(entries.map((entry, index) => (
      loadCSV(`../${entry.data}`).then(data => ({
        id: entry.id,
        name: entry.short_title,
        title: entry.title,
        color: COLORS[index % COLORS.length],
        data,
      }))
    ))))
    .then(lanesWithData => {
      renderLanes(g, lanesWithData, xScale, tooltip);
    })
    .catch(err => {
      console.error('Failed to load dashboard data:', err);
      container.append('p').attr('class', 'error')
        .text('Error loading dashboard data. Ensure manifest and CSV files are accessible.');
    });
}

function renderLanes(g, lanes, xScale, tooltip) {
  lanes.forEach((lane, index) => {
    const laneG = g.append('g')
      .attr('transform', `translate(0, ${index * (LANE_HEIGHT + 20)})`);

    laneG.append('rect')
      .attr('width', WIDTH)
      .attr('height', LANE_HEIGHT)
      .attr('fill', '#161922')
      .attr('rx', 8);

    laneG.append('text')
      .attr('class', 'lane-title')
      .attr('x', -10)
      .attr('y', LANE_HEIGHT / 2)
      .attr('text-anchor', 'end')
      .attr('dominant-baseline', 'middle')
      .text(lane.name)
      .attr('fill', lane.color);

    const events = lane.data
      .map(d => {
        const year = parseYear(d);
        return year === null ? null : { ...d, year };
      })
      .filter(Boolean)
      .sort((a, b) => a.year - b.year);

    laneG.selectAll('.event-dot')
      .data(events)
      .enter()
      .append('circle')
      .attr('class', 'event-dot')
      .attr('cx', d => xScale(d.year))
      .attr('cy', LANE_HEIGHT / 2)
      .attr('r', d => (String(d.estimate_status || d.Impact || '').toLowerCase().includes('speculative') ? 5 : 4))
      .attr('fill', lane.color)
      .attr('opacity', d => (String(d.estimate_status || d.Impact || '').toLowerCase().includes('speculative') ? 0.55 : 0.85))
      .on('mouseover', function(event, d) {
        d3.select(this).attr('r', 7).attr('opacity', 1);
        tooltip.style('opacity', 1)
          .style('left', (event.pageX + 10) + 'px')
          .style('top', (event.pageY - 10) + 'px')
          .html(`<strong>${eventName(d)}</strong><br/>${lane.title}<br/>Year: ${d.year}`);
      })
      .on('mouseout', function() {
        d3.select(this).attr('r', 4).attr('opacity', 0.8);
        tooltip.style('opacity', 0);
      });

    if (index === lanes.length - 1) {
      const axis = d3.axisBottom(xScale)
        .ticks(10)
        .tickFormat(d => d < 0 ? `${Math.abs(d)} BCE` : d.toString());
      laneG.append('g')
        .attr('class', 'axis')
        .attr('transform', `translate(0, ${LANE_HEIGHT})`)
        .call(axis);
    }
  });

  g.append('text')
    .attr('x', WIDTH / 2)
    .attr('y', lanes.length * (LANE_HEIGHT + 20) + 20)
    .attr('text-anchor', 'middle')
    .attr('fill', '#9ca3af')
    .attr('font-size', '13px')
    .text('Time (years, symlog scale) ->');
}

if (document.readyState === 'loading') {
  document.addEventListener('DOMContentLoaded', initDashboard);
} else {
  initDashboard();
}
