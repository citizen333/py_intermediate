import sys

stairs_height = int(sys.argv[1])

for step in range(1, stairs_height + 1):
    free_space = stairs_height - step
    print(' ' * free_space + '#' * step )