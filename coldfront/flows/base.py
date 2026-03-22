# SPDX-FileCopyrightText: (C) DigitalOcean, LLC
#
# SPDX-License-Identifier: Apache-2.0


class ColdFrontFlow(object):
    """
    A base model for all ColdFront worklfow objects. Workflows define a set of
    states and transitions between them using a FSM field.

    - actions is a tuple that lists the valid ObjectActions for the Workflow
    """

    actions = tuple()

    @classmethod
    def get_actions(cls, transitions):
        """
        Return the ObjectActions for the given transitions
        """
        actions = []
        for t in transitions:
            for a in cls.actions:
                if t == a.transition:
                    actions.append(a)

        return actions

    def get_label(self, transition):
        """
        Return the label for the given transition
        """
        if func := getattr(self, transition, None):
            return func.label

        return ""
