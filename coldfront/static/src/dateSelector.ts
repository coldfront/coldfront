// SPDX-FileCopyrightText: (C) ColdFront Authors
//
// SPDX-License-Identifier: AGPL-3.0-or-later

import flatpickr from 'flatpickr';

export function initDateSelector(): void {
  flatpickr('.datepicker', { allowInput: true });
}
