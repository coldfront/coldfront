// SPDX-FileCopyrightText: (C) ColdFront Authors
//
// SPDX-License-Identifier: AGPL-3.0-or-later

import './scss/coldfront.scss';
import 'bootstrap';
import 'htmx.org';
import { initDateSelector } from './dateSelector';
import { initSelect2 } from './select2';
import { initForm } from './form';
import { initColorSelects, initSelects } from './selectStatic';
import { initQuickSearch } from './search';
import { initCharts } from './charts';
import { initHtmx } from './htmx';
import { initTableConfig } from './tableConfig';
import { initButtons } from './buttons';
import { initBootstrap } from './bs';
import { initNavLinks } from './sidenav';
import { initTheme } from './theme';
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
    initSelects,
    initColorSelects,
    initQuickSearch,
    initBootstrap,
    initCharts,
    initHtmx,
    initNavLinks,
    initButtons,
    initTableConfig,
    initTheme,
  ]) {
    init();
  }
}
if (document.readyState !== 'loading') {
  initDocument();
} else {
  document.addEventListener('DOMContentLoaded', initDocument);
}
