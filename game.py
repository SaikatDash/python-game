"""A small text-based choose-your-own-adventure game set on a space station."""

from dataclasses import dataclass
from typing import Callable, Optional


InputFn = Callable[[str], str]
OutputFn = Callable[[str], None]


@dataclass
class GameState:
    """Track the discoveries that affect the station's escape route."""

    power_restored: bool = False
    keycard_found: bool = False
    distress_signal_sent: bool = False
    score: int = 0


POWER_POINTS = 25
KEYCARD_POINTS = 25
DISTRESS_SIGNAL_POINTS = 25
RESCUE_POINTS = 25


def ask_choice(
    prompt: str,
    choices: dict[str, str],
    input_fn: InputFn,
    output_fn: OutputFn,
) -> str:
    """Return a valid choice, repeating the prompt when input is invalid."""

    while True:
        answer = input_fn(prompt).strip().lower()
        if answer in choices:
            return answer

        output_fn(
            "Please choose one of: "
            + ", ".join(f"{key} ({description})" for key, description in choices.items())
        )


def play_game(
    input_fn: InputFn = input,
    output_fn: OutputFn = print,
) -> Optional[str]:
    """Run the adventure and return the ending identifier."""

    state = GameState()
    output_fn("=== ECHOES OF ORBITAL-9 ===")
    output_fn(
        "You wake in the dark aboard Orbital-9. The station is drifting, "
        "and the emergency lights are fading."
    )

    while True:
        output_fn("\nYou are in the central hub. What will you do?")
        choice = ask_choice(
            "[e] Engineering  [q] Crew quarters  [b] Observation bridge  [x] Escape pod\n> ",
            {
                "e": "visit Engineering",
                "q": "search the crew quarters",
                "b": "visit the Observation bridge",
                "x": "launch the escape pod",
            },
            input_fn,
            output_fn,
        )

        if choice == "e":
            if state.power_restored:
                output_fn("The reactor hums steadily. Engineering is already secure.")
                continue

            output_fn(
                "Sparks leap from the reactor console. A manual reset could restore power, "
                "but one wrong switch may overload the station."
            )
            action = ask_choice(
                "[r] Reset the reactor  [l] Leave it alone\n> ",
                {"r": "reset the reactor", "l": "leave Engineering"},
                input_fn,
                output_fn,
            )
            if action == "r":
                state.power_restored = True
                state.score += POWER_POINTS
                output_fn(
                    "You hold your breath and pull the reset lever. The station shudders, "
                    f"then comes alive. Power is restored! (+{POWER_POINTS} points)"
                )
            else:
                output_fn("You return to the hub before the unstable reactor gets worse.")

        elif choice == "q":
            if state.keycard_found:
                output_fn("The quarters are empty except for the quiet sound of ventilation.")
                continue

            output_fn(
                "In the captain's cabin, you find a station keycard beneath a star chart. "
                f"It should open the emergency escape pod. (+{KEYCARD_POINTS} points)"
            )
            state.keycard_found = True
            state.score += KEYCARD_POINTS

        elif choice == "b":
            if not state.power_restored:
                output_fn(
                    "The bridge door will not open without power. You can see a blinking "
                    "distress beacon through its window."
                )
                continue

            if state.distress_signal_sent:
                output_fn("The distress signal is repeating. A rescue ship should hear it soon.")
                continue

            output_fn(
                "From the bridge, you spot a rescue ship just beyond the debris field. "
                "The communications console can send one message."
            )
            action = ask_choice(
                "[s] Send a distress signal  [l] Return to the hub\n> ",
                {"s": "send the distress signal", "l": "leave the bridge"},
                input_fn,
                output_fn,
            )
            if action == "s":
                state.distress_signal_sent = True
                state.score += DISTRESS_SIGNAL_POINTS
                output_fn(
                    "Your signal reaches the rescue ship. "
                    f"Help is on the way! (+{DISTRESS_SIGNAL_POINTS} points)"
                )
            else:
                output_fn("You return to the hub with the rescue ship in sight.")

        else:
            if not state.keycard_found:
                output_fn(
                    "The escape pod rejects you. A keycard is required to launch it."
                )
                continue

            if not state.power_restored:
                output_fn(
                    "The escape pod has a keycard slot, but the launch systems have no power."
                )
                continue

            if state.distress_signal_sent:
                output_fn(
                    "You launch safely and the rescue ship guides your pod through the debris."
                )
                state.score += RESCUE_POINTS
                output_fn("ENDING: RESCUED")
                output_fn(f"SCORE: {state.score} (+{RESCUE_POINTS} rescue bonus)")
                return "rescued"

            output_fn(
                "The pod launches, but without a distress signal the debris field hides you "
                "from the nearby rescue ship."
            )
            output_fn("ENDING: LOST IN ORBIT")
            output_fn(f"SCORE: {state.score}")
            return "lost"


if __name__ == "__main__":
    play_game()
