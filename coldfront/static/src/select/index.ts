// SPDX-FileCopyrightText: (C) ColdFront Authors
//
// SPDX-License-Identifier: Apache-2.0

import { initColorSelects, initStaticSelects } from './static';

export function initSelects(): void {
  for (const func of [initColorSelects, initStaticSelects]) {
    func();
  }
}
