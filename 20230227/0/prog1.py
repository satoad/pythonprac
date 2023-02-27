import shlex
import readline

while inp := input():
    print(shlex.join(shlex.split(inp)))
