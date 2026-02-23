// SPDX-FileCopyrightText: (C) ColdFront Authors
//
// SPDX-License-Identifier: AGPL-3.0-or-later

import { getElementsByQueryGenerator } from './util';

/**
 * Expand the top level side menu group for the current page
 */
export function initNavLinks(): void {
  for (const element of getElementsByQueryGenerator('nav.nav .collapse')) {
    const divMenu = element as HTMLDivElement;
    for (const link of divMenu.querySelectorAll<HTMLAnchorElement>('a')) {
      const href = new RegExp(link.href, 'gi');
      if (window.location.href.match(href)) {
        divMenu.classList.add('show');
        return;
      }
    }
  }
}
