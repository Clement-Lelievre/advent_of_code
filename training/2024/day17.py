"""https://adventofcode.com/2024/day/17"""

# today I won't be parsing the input, as it's really short so I'll hardcode it
# after all it's not like this code will be re-used
# I'll also shamelessly use global variables for easy and lazy scope sharing


#combos = {0: 0, 1: 1, 2: 2, 3: 3, 4: 729, 5: 0, 6: 0}
output = []
#sequence = [0, 1, 5, 4, 3, 0]
combos = {0: 0, 1: 1, 2: 2, 3: 3, 4: 22817223, 5: 0, 6: 0}
sequence=[2,4,1,2,7,5,4,5,0,3,1,7,5,5,3,0]

def ops(opcode: int, operand: int):
    if opcode == 0:
        combos[4] = int(combos[4] / (2 ** combos[operand]))
    elif opcode == 1:
        combos[5] ^= operand
    elif opcode == 2:
        combos[5] = combos[operand] % 8
    elif opcode == 3:
        ...
    elif opcode == 4:
        combos[5] ^= combos[6]
    elif opcode == 5:
        output.append(combos[operand] % 8)
    elif opcode == 6:
        combos[5] = int(combos[4] / (2 ** combos[operand]))
    elif opcode == 7:
        combos[6] = int(combos[4] / (2 ** combos[operand]))
    else:
        raise Exception(f"found {opcode=}")


def solve_p1():
    pointer = 0

    while pointer < len(sequence)-1:
        opcode, operand = sequence[pointer], sequence[pointer + 1]
        #print(combos, f"{opcode=} {operand=} {pointer=} {output}")
        ops(opcode, operand)
        if opcode == 3 and combos[4]:
            pointer = operand
        else:
            pointer +=2

    ans = ",".join(map(str, output))
    print(ans)
    return ans

solve_p1()

debug = True
if debug:
    ...
    # assert combos[4]==729
    # ops(0, 2)
    # assert combos[4]==round(729/4)

    # ops(0, 5)
    # assert combos[4]==729/(2**combos[5])

    # combos = {0: 0, 1: 1, 2: 2, 3: 3, 4: 729, 5: 0, 6: 9}
    # sequence=[2,6]
    # assert combos[5]==0

    # combos = {0: 0, 1: 1, 2: 2, 3: 3, 4: 10, 5: 0, 6: 9}
    # sequence=[5,0,5,1,5,4]
    # assert solve_p1()=="0,1,2"

    # combos = {0: 0, 1: 1, 2: 2, 3: 3, 4: 2024, 5: 0, 6: 0}
    # sequence = [0, 1, 5, 4, 3, 0]
    # output=[]
    # assert solve_p1() == "4,2,5,6,7,7,7,7,3,1,0"
    # assert combos[4] == 0

    # combos = {0: 0, 1: 1, 2: 2, 3: 3, 4: 10, 5: 29, 6: 9}
    # sequence=[1,7]
    # solve_p1()
    # assert combos[5]==26
    
    # combos = {0: 0, 1: 1, 2: 2, 3: 3, 4: 10, 5: 2024, 6: 43690}
    # sequence=[4,0]
    # solve_p1()
    # assert combos[5]==44354

    # ex= solve_p1
    # assert ex==",".join(map(str, [4,6,3,5,6,3,5,2,1,0])), f"found {ex}"
    #solve_p1()