import os
import sys
import zlib


def print_info(hash, parent_flag=False):
    commit_info_path = '../../.git/objects'
    commit_path = os.path.join(commit_info_path, hash[:2], hash[2:])

    if not os.path.exists(commit_path):
        return

    with open(commit_path, 'rb') as commit_info:
        commit = zlib.decompress(commit_info.read()).partition(b'\x00')

    commit_body = commit[2].decode()
    if not parent_flag:
        print(commit_body)
    else:
        print("TREE for commit", hash)

    commit_body = commit_body.replace('\n', ' ').split('tree')[1].split()

    tree_hash = commit_body[0]
    tree_path = os.path.join(commit_info_path, tree_hash[:2], tree_hash[2:])

    with open(tree_path, 'rb') as tree_info:
        tree = zlib.decompress(tree_info.read()).partition(b'\x00')

    tree_body = tree[2]
    while tree_body:
        head, _, tree_body = tree_body.partition(b'\x00')
        head = head.split()
        git_id, tree_body = tree_body[:20].hex(), tree_body[20:]
        if head[0].decode() == '40000':
            print('tree', git_id, head[1].decode())
        if head[0].decode() == '100644':
            print('blob', git_id, head[1].decode())

    parent_hash = commit_body[2]
    if parent_hash != -1:
        print_info(parent_hash, True)

branch_path = '../../.git/refs/heads'

if len(sys.argv) == 1:
    for br in os.listdir(branch_path):
        print(br)
else:
    with open(branch_path + '/' + sys.argv[1]) as br_file:
        hash = br_file.read().strip()
    print_info(hash)

