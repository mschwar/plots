/**
 * Unified Dashboard — Singularity View
 * Multi-lane timeline showing all exponential progress plots.
 */

const LANES = [
  { id: 'energy', name: 'Energy Leverage', color: '#f59e0b', csv: '../energy-leverage-per-person/data/energy_leverage_datapoints.csv' },
  { id: 'compute', name: 'AI Compute (FLOPs)', color: '#60a5fa', csv: '../ai-compute-timeline/data/ai_milestones.csv' },
  { id: 'models', name: 'LLM Model Sizes', color: '#a78bfa', csv: '../model-sizes/data/llm_model_sizes.csv' },
  { id: 'benchmarks', name: 'AI Benchmarks', color: '#34d399', csv: '../ai-benchmark-progress/data/benchmark_data.csv' },
  { id: 'adoption', name: 'Tech Adoption Speed', color: '#f472b6', csv: '../adoption-timeline/data/tech_adoption.csv' },
  { id: 'civilization', name: 'Civilization Phases', color: '#e8eaf6', csv: '../civilization-scaling/data/civilization_metrics.csv' },
];

const MARGIN = { top: 20, right: 40, bottom: 40, left: 120 };
const LANE_HEIGHT = 80;
const WIDTH = 1400 - MARGIN.left - MARGIN.right;
const TIME_DOMAIN = [-1000000, 2030];

async function loadCSV(url) {
  const response = await fetch(url);
  const text = await response.text();
  return d3.csvParse(text);
}

function parseYear(value) {
  if (!value) return null;
  const num = parseFloat(value);
  if (isNaN(num)) return null;
  return num;
}

function initDashboard() {
  const container = d3.select('#dashboard-container');
  const tooltip = d3.select('body').append('div').attr('class', 'tooltip');

  const totalHeight = LANES.length * (LANE_HEIGHT + 20) + MARGIN.top + MARGIN.bottom;
  const svg = container.append('svg')
    .attr('width', WIDTH + MARGIN.left + MARGIN.right)
    .attr('height', totalHeight);

  const g = svg.append('g')
    .attr('transform', `translate(${MARGIN.left},${MARGIN.top})`);

  const xScale = d3.scaleSymlog()
    .domain(TIME_DOMAIN)
    .range([0, WIDTH])
    .constant(1000);

  Promise.all(LANES.map(lane => loadCSV(lane.csv).then(data => ({ ...lane, data }))))
    .then(lanesWithData => {
      renderLanes(g, lanesWithData, xScale, tooltip);
    })
    .catch(err => {
      console.error('Failed to load dashboard data:', err);
      container.append('p').style('color', '#ef4444')
        .text('Error loading dashboard data. Ensure CSV files are accessible.');
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
        const year = parseYear(d.Year || d.year || d.date);
        return year ? { ...d, year } : null;
      })
      .filter(d => d !== null)
      .sort((a, b) => a.year - b.year);

    laneG.selectAll('.event-dot')
      .data(events)
      .enter()
      .append('circle')
      .attr('class', 'event-dot')
      .attr('cx', d => xScale(d.year))
      .attr('cy', LANE_HEIGHT / 2)
      .attr('r', 4)
      .attr('fill', lane.color)
      .attr('opacity', 0.8)
      .on('mouseover', function(event, d) {
        d3.select(this).attr('r', 7).attr('opacity', 1);
        tooltip.style('opacity', 1)
          .style('left', (event.pageX + 10) + 'px')
          .style('top', (event.pageY - 10) + 'px')
          .html(`<strong>${d.Event || d.Model || d.name || 'Event'}</strong><br/>Year: ${d.year}`);
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
    .text('Time (years, log scale) →');
}

if (document.readyState === 'loading') {
  document.addEventListener('DOMContentLoaded', initDashboard);
} else {
  initDashboard();
}
