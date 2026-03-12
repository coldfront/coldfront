// SPDX-FileCopyrightText: (C) ColdFront Authors
//
// SPDX-License-Identifier: Apache-2.0

import { initMoveButtons } from './moveOptions';
import { initReslug } from './reslug';
import { initSelectAll } from './selectAll';

export function initButtons(): void {
  for (const func of [initMoveButtons, initReslug, initSelectAll]) {
    func();
  }
}
