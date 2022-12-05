from __future__ import annotations
import enum
import functools
import sys
from typing import Iterable, NamedTuple


@functools.total_ordering
class RPS(enum.IntEnum):
    ROCK = (1,)
    PAPER = (2,)
    SCISSORS = (3,)

    def __init__(self, score: int):
        self.score = score

    @property
    def succ(self):
        """
        Succession in the order (e.g. what beats it / is higher)
        """
        if self == ROCK:
            return PAPER
        elif self == PAPER:
            return SCISSORS
        elif self == SCISSORS:
            return ROCK
        else:
            raise Exception()

    @property
    def prev(self):
        """
        Previous in the order (e.g. what does it beat / is lower)
        """
        if self == ROCK:
            return SCISSORS
        elif self == PAPER:
            return ROCK
        elif self == SCISSORS:
            return PAPER
        else:
            raise Exception()

    def __lt__(self, other: RPS) -> bool:
        if not isinstance(other, RPS):
            return NotImplemented

        return (self, other) in {(ROCK, PAPER), (PAPER, SCISSORS), (SCISSORS, ROCK)}


ROCK = RPS.ROCK
PAPER = RPS.PAPER
SCISSORS = RPS.SCISSORS

STRATEGY_MAPPING = dict(A=ROCK, B=PAPER, C=SCISSORS, X=ROCK, Y=PAPER, Z=SCISSORS)


class Outcome(enum.IntEnum):
    LOSS = 0
    DRAW = 3
    WIN = 6


OUTCOME_MAPPING = dict(X=Outcome.LOSS, Y=Outcome.DRAW, Z=Outcome.WIN)


class ChoiceDrivenMatch(NamedTuple):
    their_choice: RPS
    your_choice: RPS

    def _outcome_points(self) -> Outcome:
        your_choice, their_choice = self.your_choice, self.their_choice

        if your_choice < their_choice:
            return Outcome.LOSS
        elif your_choice == their_choice:
            return Outcome.DRAW
        else:
            return Outcome.WIN

    def play(self) -> int:
        outcome = self._outcome_points()
        return outcome + self.your_choice.score


def values() -> Iterable[tuple[str, str]]:
    for line in open(sys.argv[1]):
        line = line.strip()
        left, right = line.split()
        yield (left, right)


def day1_choices() -> Iterable[ChoiceDrivenMatch]:
    for theirs, ours in values():
        yield ChoiceDrivenMatch(STRATEGY_MAPPING[theirs], STRATEGY_MAPPING[ours])


def day1():
    print(sum(match.play() for match in day1_choices()))


class OutcomeBasedMatch(NamedTuple):
    their_choice: RPS
    target_outcome: Outcome

    def _find_choice(self) -> RPS:
        match self.target_outcome:
            case Outcome.LOSS:
                return self.their_choice.prev
            case Outcome.DRAW:
                return self.their_choice
            case Outcome.WIN:
                return self.their_choice.succ

    def play(self) -> int:
        our_choice = self._find_choice()
        return ChoiceDrivenMatch(self.their_choice, our_choice).play()


def day2_info() -> Iterable[OutcomeBasedMatch]:
    for theirs, outcome in values():
        yield OutcomeBasedMatch(STRATEGY_MAPPING[theirs], OUTCOME_MAPPING[outcome])


def day2():
    print(sum(match.play() for match in day2_info()))


if __name__ == "__main__":
    day2()
