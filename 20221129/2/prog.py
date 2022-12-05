import inspect
import types

class check(type):
    def __new__(cls, clsname, bases, attrs, **kwds):
        def check_annotations(self):
            #at = inspect.signature(self)
            at = inspect.get_annotations(self.__class__)
       #     print(at)
            flag = True
            for i, j in at.items():
               # print(i, j)
                if not hasattr(self, str(i)):
                    flag = False
                    break
                elif isinstance(j, types.GenericAlias):
                    if not isinstance(getattr(self, i), j.__origin__):
                        flag = False
                        break
                    else:
                        continue
                elif not isinstance(getattr(self, i), j):
                    flag = False
                    break

            return flag

        attrs["check_annotations"] = check_annotations
        return type(clsname, bases, attrs)