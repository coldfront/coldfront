// SPDX-FileCopyrightText: (C) ColdFront Authors
//
// SPDX-License-Identifier: AGPL-3.0-or-later

import { initMoveButtons } from './moveOptions';
import { initReslug } from './reslug';
import { initSelectAll } from './selectAll';

export function initButtons(): void {
  for (const func of [initMoveButtons, initReslug, initSelectAll]) {
    func();
  }
}
