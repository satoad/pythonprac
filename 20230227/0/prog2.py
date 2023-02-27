import shlex
import readline

name = shlex.join(shlex.split(input('Введите ФИО: ')))
place = shlex.join(shlex.split(input('Введите место рождения: ')))
print(shlex.join(['register', name, place]))
