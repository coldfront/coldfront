// SPDX-FileCopyrightText: (C) ColdFront Authors
//
// SPDX-License-Identifier: AGPL-3.0-or-later

import $ from 'jquery';
import DataTable from 'datatables.net-bs4';
import c3 from 'c3';

$(document).ready(function () {
  drawAllocations();
  drawResources();
  new DataTable('#resource-table', {
    pageLength: 10,
    orderClasses: false,
    order: [[1, 'desc']],
  });
});

function drawAllocations() {
  c3.generate({
    bindto: '#chartAllocations',
    donut: {
      title: 'Allocations',
    },
    data: allocations_chart_data,
  });
}

function drawResources() {
  c3.generate({
    bindto: '#chartResources',
    data: resources_chart_data,
    donut: {
      title: 'Active by Type',
    },
  });
}

/* eslint-disable @typescript-eslint/no-non-null-asserted-optional-chain */
const allocations_chart_data = JSON.parse(
  document.getElementById('allocations-chart-data')?.textContent!
);
const resources_chart_data = JSON.parse(
  document.getElementById('resources-chart-data')?.textContent!
);
