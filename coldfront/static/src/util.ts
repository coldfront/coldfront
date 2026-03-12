// SPDX-FileCopyrightText: (C) ColdFront Authors
//
// SPDX-License-Identifier: Apache-2.0

/**
 * Generator that yields HTML elements by CSS query selector
 * @param query - CSS query selector string
 * @param container - Optional container to search within (defaults to document)
 * @yields HTMLElement - HTML elements (never null)
 */
export function* getElementsByQueryGenerator(
  query: string,
  container: Document | HTMLElement = document
): Generator<HTMLElement, void, undefined> {
  const elements = container.querySelectorAll(query);
  for (let i = 0; i < elements.length; i++) {
    yield elements[i] as HTMLElement;
  }
}
