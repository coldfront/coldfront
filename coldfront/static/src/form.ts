// SPDX-FileCopyrightText: (C) ColdFront Authors
//
// SPDX-License-Identifier: Apache-2.0

export function initForm(): void {
  // Initialize any reset buttons so that when clicked, the page is reloaded without query parameters.
  const resetButton =
    document.querySelector<HTMLButtonElement>('button[data-reset]');
  if (resetButton !== null) {
    resetButton.addEventListener('click', () => {
      window.location.assign(window.location.origin + window.location.pathname);
    });
  }
}
