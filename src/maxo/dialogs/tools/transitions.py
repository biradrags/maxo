import os.path
from collections.abc import Iterable, Sequence
from typing import TYPE_CHECKING

from diagrams import Cluster, Diagram, Edge
from diagrams.custom import Custom

from maxo.dialogs.api.internal import WindowProtocol
from maxo.dialogs.setup import collect_dialogs
from maxo.dialogs.widgets.kbd import (
    Back,
    Cancel,
    Group,
    Next,
    Start,
    SwitchTo,
)
from maxo.fsm import State
from maxo.routing.interfaces import BaseRouter

if TYPE_CHECKING:
    from maxo.dialogs import Dialog

ICON_PATH = os.path.join(os.path.dirname(__file__), "calculator.png")


def widget_edges(
    nodes: dict[State, Custom],
    dialog: "Dialog",
    starts: list[tuple[State, State]],
    current_state: State,
    kbd: Back | Cancel | Next | Start | SwitchTo | Group,
) -> None:
    states = dialog.states()
    if isinstance(kbd, Start):
        nodes[current_state] >> Edge(color="#338a3e") >> nodes[kbd.state]
    elif isinstance(kbd, SwitchTo):
        nodes[current_state] >> Edge(color="#0086c3") >> nodes[kbd.state]
    elif isinstance(kbd, Next):
        new_state = states[states.index(current_state) + 1]
        nodes[current_state] >> Edge(color="#0086c3") >> nodes[new_state]
    elif isinstance(kbd, Back):
        new_state = states[states.index(current_state) - 1]
        nodes[current_state] >> Edge(color="grey") >> nodes[new_state]
    elif isinstance(kbd, Cancel):
        for from_, to_ in starts:
            if to_.group == current_state.group:
                (
                    nodes[current_state]
                    >> Edge(color="grey", style="dashed")
                    >> nodes[from_]
                )


def walk_keyboard(
    nodes: dict[State, Custom],
    dialog: "Dialog",
    starts: list[tuple[State, State]],
    current_state: State,
    keyboards: Sequence,
) -> None:
    for kbd in keyboards:
        if isinstance(kbd, Group):
            walk_keyboard(nodes, dialog, starts, current_state, kbd.buttons)
        else:
            widget_edges(nodes, dialog, starts, current_state, kbd)


def find_starts(
    current_state: State,
    keyboards: Sequence,
) -> Iterable[tuple[State, State]]:
    for kbd in keyboards:
        if isinstance(kbd, Group):
            yield from find_starts(current_state, kbd.buttons)
        elif isinstance(kbd, Start):
            yield current_state, kbd.state


def render_window(
    nodes: dict[State, Custom],
    dialog: "Dialog",
    starts: list[tuple[State, State]],
    window: WindowProtocol,
) -> None:
    walk_keyboard(
        nodes,
        dialog,
        starts,
        window.get_state(),
        [window.keyboard],
    )
    preview_add_transitions = getattr(
        window,
        "preview_add_transitions",
        None,
    )
    if preview_add_transitions:
        walk_keyboard(
            nodes,
            dialog,
            starts,
            window.get_state(),
            preview_add_transitions,
        )


def render_transitions(
    router: BaseRouter,
    title: str = "Maxo Dialog",
    filename: str = "maxo_dialog",
    format: str = "png",
) -> None:
    dialogs = list(collect_dialogs(router))
    with Diagram(title, filename=filename, outformat=format, show=False):
        nodes = {}
        for dialog in dialogs:
            with Cluster(dialog.states_group_name()):
                for window in dialog.windows.values():
                    nodes[window.get_state()] = Custom(
                        icon_path=ICON_PATH,
                        label=window.get_state()._state,
                    )

        starts = []
        for dialog in dialogs:
            for window in dialog.windows.values():
                starts.extend(
                    find_starts(window.get_state(), [window.keyboard]),
                )

        for dialog in dialogs:
            for window in dialog.windows.values():
                render_window(
                    nodes=nodes,
                    dialog=dialog,
                    window=window,
                    starts=starts,
                )
