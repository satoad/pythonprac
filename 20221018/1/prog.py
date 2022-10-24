a = input().lower()

let = set()
for i in range(len(a)):
    if a[i].isalpha():
        let.add(a[i])

print(int((len(let) * (len(let) - 1)) / 2))