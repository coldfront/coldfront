// SPDX-FileCopyrightText: (C) ColdFront Authors
//
// SPDX-License-Identifier: AGPL-3.0-or-later

import $ from 'jquery';

export function initForm(): void {
  $(document).on('click', '#form_reset_button', function () {
    resetForm($('#filter_form'));
  });

  $('#expand_button').click(function () {
    $('#collapseOne').collapse();
    const icon = $('#plus_minus');
    icon.toggleClass('fa-plus fa-minus');
  });

  const forms = [
    ['selectAll', 'attributeform-'],
    ['selectAllAllocations', 'allocationform-'],
    ['selectAll', 'userform-'],
    ['selectAll', 'users'],
    ['selectAll', 'noteform-'],
    ['selectAll', 'grantform-'],
    ['selectAll', 'pubform-'],
    ['selectAll', 'grantdownloadform-'],
  ];
  for (const f of forms) {
    $('#' + f[0]).click(function () {
      $("input[name^='" + f[1] + "']").prop('checked', $(this).prop('checked'));
    });

    $("input[name^='" + f[1] + "']").click(function () {
      const id = $(this).attr('id');
      if (id != f[0]) {
        $('#' + f[0]).prop('checked', false);
      }
    });
  }
}

/* eslint-disable @typescript-eslint/no-explicit-any */
function resetForm($form: any) {
  $form
    .find('input:text, input:password, input:file, select, textarea')
    .val('');
  $form
    .find('input:radio, input:checkbox')
    .removeAttr('checked')
    .removeAttr('selected');
}
