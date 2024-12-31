import os
import readline
import atexit

histfile = os.path.join(os.path.expanduser("~"), ".mal_history")

try:
    readline.read_history_file(histfile)
    # default history len is -1 (infinite), which may grow unruly
    readline.set_history_length(1000)
except FileNotFoundError:
    pass

atexit.register(readline.write_history_file, histfile)

def m_input(*args, **kwargs):
    return input(*args, **kwargs)
