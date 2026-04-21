// SPDX-FileCopyrightText: (C) ColdFront Authors
//
// SPDX-License-Identifier: AGPL-3.0-or-later

import Chart from 'chart.js/auto';
import { renderChart, ColorPalette } from './data';
import type { ChartData, ChartDataItem } from './data';

export function initResourceChart(): void {
  renderChart(
    'resource-summary-chart',
    'portal/data/resource-by-type',
    createResourceChart
  );
}

function createResourceChart(
  canvas: HTMLCanvasElement,
  chartData: ChartData
): void {
  new Chart(canvas, {
    type: 'doughnut',
    data: {
      labels: chartData.data.map((row: ChartDataItem) => row.name),
      datasets: [
        {
          data: chartData.data.map((row: ChartDataItem) => row.total),
          backgroundColor: ColorPalette.PRIMARY,
          borderColor: ColorPalette.PRIMARY.map((color) => color + '80'),
          borderWidth: 1,
        },
      ],
    },
    options: {
      radius: '70%',
      responsive: true,
      plugins: {
        legend: {
          position: 'bottom',
        },
        title: {
          display: false,
        },
      },
    },
  });
}
