import calendar
import sys

def calend(year, month):
    year = calendar.year = year
    month = calendar.month = month

    cal = calendar.monthcalendar(year, month)

    table_header = "+---+---+---+---+---+---+---+\n|Mon|Tue|Wed|Thu|Fri|Sat|Sun|"

    table_rows = ""
    for week in cal:
        row = "|"
        for day in week:
            if day == 0:
                row += "   |"
            else:
                if day < 10:
                    row += f" {day} |"
                else:
                    row += f" {day}|"
        table_rows += f"+---+---+---+---+---+---+---+\n{row}\n"

    table = f"{table_header}\n{table_rows}{table_header}\n+---+---+---+---+---+---+---+"

    with open("calendar.rst", "w") as file:
        file.write(table)

return "Файл calendar.rst успешно создан!"

if __name__ == "__main__":
    calend(int(sys.argv[1]), int(sys.argv[2]))
