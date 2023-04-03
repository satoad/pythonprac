import calendar


def rest_calendar(year, month):
    # Создаем таблицу reST
    table = ""
    table += "+------+-------+-------+-------+-------+-------+-------+-------+\n"
    table += "|      | Mon   | Tue   | Wed   | Thu   | Fri   | Sat   | Sun   |\n"
    table += "+======+=======+=======+=======+=======+=======+=======+=======+\n"
    
    # Получаем календарь на месяц
    cal = calendar.monthcalendar(year, month)
    
    # Добавляем строки в таблицу для каждой недели
    for week in cal:
        row = "|      "
        for day in week:
            if day == 0:
                row += "|       "
            else:
                row += "| {:>4d} ".format(day)
        row += "|\n"
        table += row
        table += "+------+-------+-------+-------+-------+-------+-------+-------+\n"
    
    return table

# Создаем таблицу для текущего месяца
table = rest_calendar(2023, 4)

# Создаем файл и записываем в него таблицу
with open('rest_calendar.txt', 'w') as f:
    f.write(table)

# Выводим сообщение о завершении работы
print("Таблица успешно создана в файле rest_calendar.txt")
calendar.month()
