import sys

a = sys.stdin.buffer.read().decode('utf-8') 
sys.stdout.buffer.write(a.encode('latin1', errors='replace').decode('cp1251', errors='replace').encode('utf-8'))