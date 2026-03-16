// SPDX-FileCopyrightText: (C) ColdFront Authors
//
// SPDX-License-Identifier: Apache-2.0

import './scss/coldfront.scss';
import 'bootstrap';
import 'htmx.org';
import { initDateSelector } from './dateSelector';
import { initForm } from './form';
import { initSelects } from './select';
import { initQuickSearch } from './search';
import { initHtmx } from './htmx';
import { initTableConfig } from './tableConfig';
import { initButtons } from './buttons';
import { initBootstrap } from './bs';
import { initNavLinks } from './sidenav';
import { initTheme } from './theme';
import { initClipboard } from './clipboard';
import { initObjectSelector } from './objectSelector';

function initDocument(): void {
  for (const init of [
    initBootstrap,
    initTheme,
    initDateSelector,
    initForm,
    initSelects,
    initQuickSearch,
    initHtmx,
    initNavLinks,
    initButtons,
    initTableConfig,
    initClipboard,
    initObjectSelector,
  ]) {
    init();
  }
}
if (document.readyState !== 'loading') {
  initDocument();
} else {
  document.addEventListener('DOMContentLoaded', initDocument);
}
