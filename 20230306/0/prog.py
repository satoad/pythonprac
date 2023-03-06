import cmd

class ech(cmd.Cmd):
    dump = None
    
    def do_echo(self, arg):
        """echo [parameters] -- print parameters"""
        print(arg)
        
    def do_dump(self, arg):
        print(self.dump)
    
    def complete_echo(self, prefix, line, start, end):
        variants = "qwe", "qwa", "qqdsfg", "qwulop", "nooo!"
        self.dump = prefix, line, start, end
        return [s for s in variants if s.startswith(prefix)]
        
    def do_quit(self, arg):
        """Quit program"""
        
    def do_EOF(self, arg):
        return 1
        
ech().cmdloop()
