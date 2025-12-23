// SPDX-FileCopyrightText: (C) ColdFront Authors
//
// SPDX-License-Identifier: AGPL-3.0-or-later

import './scss/coldfront.scss';
import 'bootstrap';
import 'htmx.org';
import { initDateSelector } from './dateSelector';
import { initSelect2 } from './select2';
import { initForm } from './form';
import { initDataTable } from './dataTable';
import { initCharts } from './charts';
import { initHtmx } from './htmx';
import { initBootstrap } from './bs';
import { getCookie } from './util';
import jQuery from 'jquery';

Object.assign(window, {
  getCookie: function (name: string) {
    getCookie(name);
  },
  $: jQuery,
  jQuery,
});

function initDocument(): void {
  for (const init of [
    initDateSelector,
    initSelect2,
    initForm,
    initDataTable,
    initBootstrap,
    initCharts,
    initHtmx,
  ]) {
    init();
  }
}
if (document.readyState !== 'loading') {
  initDocument();
} else {
  document.addEventListener('DOMContentLoaded', initDocument);
}
