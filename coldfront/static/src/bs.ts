import { Collapse, Tooltip, Popover } from 'bootstrap';
import { getElementsByQueryGenerator } from './util';

export function initTooltips() {
  for (const tooltip of getElementsByQueryGenerator(
    '[data-bs-toggle="tooltip"]'
  )) {
    new Tooltip(tooltip, { container: 'body' });
  }
}

export function initPopovers() {
  for (const popover of getElementsByQueryGenerator(
    '[data-bs-toggle="popover"]'
  )) {
    new Popover(popover);
  }
}

export function initCollapse() {
  for (const collapse of getElementsByQueryGenerator(
    '[data-bs-toggle="collapse"]'
  )) {
    new Collapse(collapse);
  }
}

export function initBootstrap(): void {
  for (const func of [initTooltips, initPopovers]) {
    func();
  }
}
