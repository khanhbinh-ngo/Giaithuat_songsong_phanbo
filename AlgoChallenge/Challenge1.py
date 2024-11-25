#
# Rất là mất thời gian với cái challenge này
# #

def count_occurrences(args):
    Si, Bi = args
    if Bi not in Si:
        return -1
    return Si.count(Bi)
def MAIN(filename = "input.txt"):
    with open(filename,'r') as f:
        lines = f.readlines()
    N = int(lines[0].strip())
    pairs = [(lines[i * 2 + 1].strip(), lines[i * 2 + 2].strip()) for i in range(N)]

    with Pool() as pool:
        results = pool.map(count_occurrences, pairs)

    return '\n'.join(map(str, results))
     
