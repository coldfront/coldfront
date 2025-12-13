// SPDX-FileCopyrightText: (C) ColdFront Authors
//
// SPDX-License-Identifier: AGPL-3.0-or-later

import './scss/coldfront.scss';
/* eslint-disable @typescript-eslint/no-unused-vars */
// @ts-expect-error we need to include all of bootstraps javascript in the bundle here
import * as bootstrap from 'bootstrap';
import { initDateSelector } from './dateSelector';
import { initSelect2 } from './select2';
import { initForm } from './form';
import { initDataTable } from './dataTable';
import { getCookie, drawGauges } from './util';
import jQuery from 'jquery';

/* eslint-disable @typescript-eslint/no-explicit-any */

Object.assign(window, {
  getCookie: function (name: string) {
    getCookie(name);
  },
  drawGauges: function (guage_data: Array<any>) {
    drawGauges(guage_data);
  },
  $: jQuery,
  jQuery,
});

function initDocument(): void {
  for (const init of [initDateSelector, initSelect2, initForm, initDataTable]) {
    init();
  }
}
if (document.readyState !== 'loading') {
  initDocument();
} else {
  document.addEventListener('DOMContentLoaded', initDocument);
}
