# could these be abstracted away from their hardcoded numbers? yes.
# is it worth it? no. DRY only applies after you repeat yourself twice.
def is_packet_marker(chars: str) -> bool:
    assert len(chars) == 4, "stream window must be 4 characters"
    return len(set(chars)) == 4


def is_message_marker(chars: str) -> bool:
    assert len(chars) == 14, "stream window must be 14 characters"
    return len(set(chars)) == 14


def find_packet_marker_offset(stream: str) -> int:
    for offset in range(0, len(stream) - 4 + 1):
        start, end = offset, offset + 4
        if is_packet_marker(stream[start:end]):
            return end

    raise ValueError("stream did not include marker")


def find_message_marker_offset(stream: str) -> int:
    for offset in range(0, len(stream) - 14 + 1):
        start, end = offset, offset + 14
        if is_message_marker(stream[start:end]):
            return end

    raise ValueError("stream did not include marker")


TEST_DATA = dict(
    mjqjpqmgbljsphdztnvjfqwrcgsmlb=(7, 19),
    bvwbjplbgvbhsrlpgdmjqwftvncz=(5, 23),
    nppdvjthqldpwncqszvftbrmjlhg=(6, 23),
    nznrnfrfntjfmvfwmzdfjlvtqnbhcprsg=(10, 29),
    zcfzfwzzqfrljwzlrfnpqdbhtmscgvjw=(11, 26),
)
"Maps stream to packet marker offset and message marker offset"


def part1():
    with open("inputs/day6.txt") as f:
        stream = f.read().strip()

    print(find_packet_marker_offset(stream))


def part2():
    with open("inputs/day6.txt") as f:
        stream = f.read().strip()

    print(find_message_marker_offset(stream))
