// SPDX-FileCopyrightText: (C) ColdFront Authors
//
// SPDX-License-Identifier: AGPL-3.0-or-later

export function initTheme(): void {
  // Toggle dark mode
  const toggle = document.getElementById('theme-toggle');

  if (toggle !== null) {
    toggle.addEventListener('click', function () {
      const body = document.body;
      const isDarkMode = body.getAttribute('data-bs-theme') === 'dark';

      if (isDarkMode) {
        body.setAttribute('data-bs-theme', 'light');
        localStorage.setItem('theme', 'light');
        toggle.title = 'Toggle dark mode';
      } else {
        body.setAttribute('data-bs-theme', 'dark');
        localStorage.setItem('theme', 'dark');
        toggle.title = 'Toggle light mode';
      }
    });
  }

  // Set initial theme based on localStorage or system preference
  document.addEventListener('DOMContentLoaded', function () {
    const savedTheme = localStorage.getItem('theme');
    const prefersDark = window.matchMedia(
      '(prefers-color-scheme: dark)'
    ).matches;

    if (savedTheme) {
      document.body.setAttribute('data-bs-theme', savedTheme);
    } else if (prefersDark) {
      document.body.setAttribute('data-bs-theme', 'dark');
    }
  });
}
