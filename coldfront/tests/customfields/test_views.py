# SPDX-FileCopyrightText: (C) ColdFront Authors
# SPDX-FileCopyrightText: (C) DigitalOcean, LLC
#
# SPDX-License-Identifier: AGPL-3.0-or-later AND Apache-2.0

from coldfront.core.models import CustomFieldChoiceSet
from coldfront.utils.testing import ViewTestCases


class CustomFieldChoiceSetTestCase(ViewTestCases.PrimaryObjectViewTestCase):
    model = CustomFieldChoiceSet

    @classmethod
    def setUpTestData(cls):

        choice_sets = (
            CustomFieldChoiceSet(name="Choice Set 1", choices=["A1:Choice 1", "A2:Choice 2", "A3:Choice 3"]),
            CustomFieldChoiceSet(name="Choice Set 2", choices=["B1:Choice 1", "B2:Choice 2", "B3:Choice 3"]),
            CustomFieldChoiceSet(name="Choice Set 3", choices=["C1:Choice 1", "C2:Choice 2", "C3:Choice 3"]),
            CustomFieldChoiceSet(name="Choice Set 4", choices=["D1:Choice 1", "D2:Choice 2", "D3:Choice 3"]),
        )
        CustomFieldChoiceSet.objects.bulk_create(choice_sets)

        cls.form_data = {
            "name": "Choice Set X",
            "choices": '["X1:Choice 1", "X2:Choice 2", "X3:Choice 3"]',
        }

        cls.csv_data = (
            "name,choices",
            'Choice Set 5,"D1,D2,D3"',
            'Choice Set 6,"E1,E2,E3"',
            'Choice Set 7,"F1,F2,F3"',
            'Choice Set 8,"F1:L1,F2:L2,F3:L3"',
        )

        cls.csv_update_data = (
            "id,choices",
            f'{choice_sets[0].pk},"A,B,C"',
            f'{choice_sets[1].pk},"A,B,C"',
            f'{choice_sets[2].pk},"A,B,C"',
            f'{choice_sets[3].pk},"A:L1,B:L2,C:L3"',
        )

        cls.bulk_edit_data = {
            "description": "New description",
        }
