// SPDX-FileCopyrightText: (C) ColdFront Authors
//
// SPDX-License-Identifier: AGPL-3.0-or-later

import { initBootstrap } from './bs';
import { initColorSelects, initSelects } from './selectStatic';

function initDepedencies(): void {
  initBootstrap();
  initColorSelects();
  initSelects();
}

/**
 * Hook into HTMX's event system to reinitialize specific native event listeners when HTMX swaps
 * elements.
 */
export function initHtmx(): void {
  document.addEventListener('htmx:afterSettle', initDepedencies);
}
