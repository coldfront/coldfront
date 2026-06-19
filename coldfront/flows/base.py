# SPDX-FileCopyrightText: (C) DigitalOcean, LLC
#
# SPDX-License-Identifier: Apache-2.0

import logging

logger = logging.getLogger(__name__)


class ColdFrontFlow(object):
    """
    A base model for all ColdFront worklfow objects. Workflows define a set of
    states and transitions between them using a FSM field.

    - actions is a tuple that lists the valid ObjectActions for the Workflow
    """

    actions = tuple()

    # Registry mapping target_state -> list of callbacks
    # Callbacks are invoked when a transition successfully reaches the target state.
    # Callback signature: callback(obj, *, source=source, target=target)
    _target_callbacks: dict = {}

    @classmethod
    def register_target_callback(cls, target_state, callback):
        """
        Register a callback to run when a transition reaches target_state.

        Args:
            target_state: The target state value (e.g., AllocationStatusChoices.STATUS_APPROVED)
            callback: A callable with signature callback(obj, *, source, target)
        """
        cls._target_callbacks.setdefault(target_state, []).append(callback)

    def _dispatch_target_callbacks(self, obj, source, target):
        """
        Call all registered callbacks for the given target state.

        Each callback is wrapped in a try-except so that a failure in one
        callback does not prevent other callbacks from running or, more
        importantly, does not break the core state transition.
        """
        for callback in self._target_callbacks.get(target, []):
            try:
                callback(obj, source=source, target=target)
            except Exception:
                logger.exception(
                    "Error in callback %r for target state %r",
                    callback.__name__ if hasattr(callback, "__name__") else callback,
                    target,
                )

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
