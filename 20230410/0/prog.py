import gettext
import os

popath = os.path.join(os.path.dirname(__file__), "po")
translation = gettext.translation("prog", popath, fallback=True)
_, ngettext = translation.gettext, translation.ngettext


while words := input().split():
    print(ngettext("{} word entered", "{} words entered", len(words)).format(len(words)))
