// SPDX-FileCopyrightText: (C) ColdFront Authors
//
// SPDX-License-Identifier: AGPL-3.0-or-later

import DataTable from 'datatables.net-bs4';

export function initDataTable(): void {
  const dtables = document.querySelectorAll<HTMLDivElement>(
    'div.table-responsive > table.datatable'
  );
  for (const element of dtables) {
    if (element !== null) {
      new DataTable(element, {
        pageLength: 10,
        orderClasses: false,
        order: [[1, 'desc']],
      });
    }
  }

  const dtablesLong = document.querySelectorAll<HTMLDivElement>(
    'div.table-responsive > table.datatable-long'
  );
  for (const element of dtablesLong) {
    if (element !== null) {
      new DataTable(element, {
        pageLength: 50,
        orderClasses: false,
        order: [[1, 'desc']],
      });
    }
  }
}
