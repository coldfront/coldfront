// SPDX-FileCopyrightText: (C) ColdFront Authors
//
// SPDX-License-Identifier: AGPL-3.0-or-later

import { getCSSVariable } from './data';
import Chart from 'chart.js/auto';

export function initGaugeChart(): void {
  const gauges = document.querySelectorAll<HTMLCanvasElement>(
    'div.chart-container > canvas.gauge-chart'
  );
  for (const element of gauges) {
    if (element !== null) {
      const used = Number(element?.getAttribute('data-used') || 0);
      let total = Number(element?.getAttribute('data-total') || 0) - used;
      const title = String(element?.getAttribute('data-title') || '');

      if (total < 0) {
        total = 0;
      }

      createGaugeChart(element, title, used, total);
    }
  }
}

function createGaugeChart(
  canvas: HTMLCanvasElement,
  title: string,
  value: number,
  total: number
): void {
  new Chart(canvas, {
    type: 'doughnut',
    data: {
      labels: ['Used', 'Available'],
      datasets: [
        {
          data: [value, total],
          // This uses bootstraps colors
          backgroundColor: [
            getCSSVariable('--bs-success'),
            getCSSVariable('--bs-secondary'),
          ],
          borderColor: [
            getCSSVariable('--bs-success'),
            getCSSVariable('--bs-secondary'),
          ],
          borderWidth: 1,
        },
      ],
    },
    options: {
      radius: '70%',
      rotation: 270,
      circumference: 180,
      responsive: true,
      plugins: {
        legend: {
          display: false,
        },
        title: {
          display: true,
          text: title,
          position: 'bottom',
        },
      },
    },
  });
}
