a = input()

w = len(a)
gas = 0
liq = 0
h = 0

while (tmp := input()) != a:
    if tmp[1] == '.':
        gas += w - 2

    if tmp[1] == '~':
        liq += w - 2

    h += 1

new_liq = liq // h
if liq - new_liq * h > 0:
    new_liq += 1

print("#" * (h + 2))
for i in range(0, w - new_liq - 2):
    print('#' + '.' * h + '#')

for i in range(0, new_liq):
    print('#' + '~' * h + '#')
print("#" * (h + 2))

sum = liq + gas

if liq > gas:
    liq_d = 20
    gas_d = round(gas * 20 / liq)
    print(f"{'.' * gas_d} {' ' * (liq_d - gas_d)} {gas}/{sum}")
    print(f"{'~' * liq_d} {liq}/{sum}")

else:
    gas_d = 20
    liq_d = round(liq * 20 / gas)
    print(f"{'.' * gas_d} {gas} / {sum}")
    print(f"{'~' * liq_d} {' ' * (gas_d - liq_d)} {liq}/{sum}")
