import os
import sys
import zlib

def print_info(branch):
    with open(branch) as br_file:
        inside = br_file.read().strip()

    commit_path = '/Users/toad/PycharmProjects/pythonprac/pythonprac/.git/objects'
    commit_path = os.path.join(commit_path, inside[:2], inside[2:])

    with open(commit_path, 'rb') as commit_info:
        commit = zlib.decompress(commit_info.read()).partition(b'\x00')

    print(commit)


branch_path = '/Users/toad/PycharmProjects/pythonprac/pythonprac/.git/refs/heads'

if len(sys.argv) == 1:
    for br in os.listdir(branch_path):
        print(br)
else:
    print_info(branch_path + '/' + sys.argv[1])

