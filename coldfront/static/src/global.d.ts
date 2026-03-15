// SPDX-FileCopyrightText: (C) DigitalOcean, LLC
// SPDX-FileCopyrightText: (C) ColdFront Authors
//
// SPDX-License-Identifier: Apache-2.0

/* eslint-disable @typescript-eslint/no-unnecessary-type-constraint */
type Dict<T extends unknown = unknown> = Record<string, T>;

type Nullable<T> = T | null;
