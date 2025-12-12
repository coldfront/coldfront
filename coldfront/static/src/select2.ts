// SPDX-FileCopyrightText: (C) ColdFront Authors
//
// SPDX-License-Identifier: AGPL-3.0-or-later

import $ from 'jquery';
import jQuery from 'jquery';
import src from 'select2?raw';

// This sourcery was required to get select2 working:
// see: https://stackoverflow.com/a/79756470
new Function('module', 'require', 'window', 'jQuery', src)(
  {},
  () => jQuery,
  window,
  jQuery
);

export function initSelect2(): void {
  $('.fos-select2').select2({
    placeholder: 'Select a fos',
  });
}
