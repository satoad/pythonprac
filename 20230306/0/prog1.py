import cmd
from calendar import TextCalendar as tc

class cal(cmd.Cmd):

    def do_prmonth(self, arg):
        """Print a month’s calendar as returned by formatmonth()."""
        arg = arg.split()
        tc().prmonth(int(arg[0]), int(arg[1]))
        
    def complete_month(self, prefix, line, start, end):
    return [str(m) for m in range(1, 13) if str(m).startswith(prefix)]
    
    def do_pryear(self, arg):
        """Print the calendar for an entire year as returned by formatyear()."""
        tc().pryear(int(arg))

cal().cmdloop()

