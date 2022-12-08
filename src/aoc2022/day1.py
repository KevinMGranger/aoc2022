import sys

elves_to_weights: list[int] = [0]

elf = 0
for line in open(sys.argv[1]):
    line = line.strip()

    if not line:
        elves_to_weights.append(0)
        elf += 1
        continue

    elves_to_weights[elf] += int(line)

# print(max(elves_to_weights)) # p1

elves_to_weights.sort(reverse=True)
print(sum(elves_to_weights[:3]))