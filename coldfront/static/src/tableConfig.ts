// SPDX-FileCopyrightText: (C) DigitalOcean, LLC
// SPDX-FileCopyrightText: (C) ColdFront Authors
//
// SPDX-License-Identifier: Apache-2.0

import { getElementsByQueryGenerator } from './util';

/**
 * Add columns to the table config select element.
 */
function addColumns(event: Event): void {
  for (const optionElement of getElementsByQueryGenerator(
    '#id_available_columns > option'
  )) {
    const selectedOption = optionElement as HTMLOptionElement;
    if (selectedOption.selected) {
      for (const selectedElement of getElementsByQueryGenerator(
        '#id_columns'
      )) {
        const selected = selectedElement as HTMLSelectElement;
        selected.appendChild(selectedOption.cloneNode(true));
      }
      selectedOption.remove();
    }
  }
  event.preventDefault();
}

/**
 * Remove columns from the table config select element.
 */
function removeColumns(event: Event): void {
  for (const optionElement of getElementsByQueryGenerator(
    '#id_columns > option'
  )) {
    const selectedOption = optionElement as HTMLOptionElement;
    if (selectedOption.selected) {
      for (const availableElement of getElementsByQueryGenerator(
        '#id_available_columns'
      )) {
        const available = availableElement as HTMLSelectElement;
        available.appendChild(selectedOption.cloneNode(true));
      }
      selectedOption.remove();
    }
  }
  event.preventDefault();
}

/**
 * Initialize table configuration elements.
 */
export function initTableConfig(): void {
  for (const element of getElementsByQueryGenerator('#add_columns')) {
    element.addEventListener('click', addColumns);
  }
  for (const element of getElementsByQueryGenerator('#remove_columns')) {
    element.addEventListener('click', removeColumns);
  }
}
