// SPDX-FileCopyrightText: (C) ColdFront Authors
// SPDX-FileCopyrightText: (C) DigitalOcean, LLC
//
// SPDX-License-Identifier: AGPL-3.0-or-later AND Apache-2.0

import Clipboard from 'clipboard';
import { getElementsByQueryGenerator } from './util';

export function initClipboard(): void {
  for (const element of getElementsByQueryGenerator('.copy-content')) {
    new Clipboard(element);
  }
}
