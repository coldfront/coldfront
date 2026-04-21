// SPDX-FileCopyrightText: (C) ColdFront Authors
//
// SPDX-License-Identifier: AGPL-3.0-or-later

import Chart from 'chart.js/auto';
import { renderChart } from './data';
import type { ChartData, ChartDataItem } from './data';

export function initPubChart(): void {
  renderChart(
    'pubs-by-year-chart',
    'publication/data/by-year',
    createPubChart
  );
}

function createPubChart(canvas: HTMLCanvasElement, chartData: ChartData): void {
  new Chart(canvas, {
    type: 'bar',
    data: {
      labels: chartData.data.map((row: ChartDataItem) => row.name),
      datasets: [
        {
          label: 'Publications',
          data: chartData.data.map((row: ChartDataItem) => row.total),
        },
      ],
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      scales: {
        y: {
          beginAtZero: true,
          suggestedMax: 10,
          ticks: {
            stepSize: 1,
          },
          grid: {
            display: false,
          },
        },
        x: {
          grid: {
            display: false,
          },
        },
      },
      plugins: {
        title: {
          display: false,
        },
        legend: {
          display: false,
        },
      },
    },
  });
}
