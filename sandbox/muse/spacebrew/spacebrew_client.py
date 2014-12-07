__author__ = 'marion'

#!/usr/bin/python


import locale
import curses

from sandbox.muse.spacebrew.spacebrew import Spacebrew




# set the encoding to use for the terminal string
locale.setlocale(locale.LC_ALL, '')
code = locale.getpreferredencoding()

# initialize the terminal display
stdscr = curses.initscr()
stdscr.keypad(1)
curses.noecho()  # turn off echo
curses.curs_set(0)  # turn off cursor

# get app name and server from query string
name = "cloudbrain"
server = "localhost"

# configure the spacebrew client
brew = Spacebrew(name, server=server)
brew.addSubscriber("CloudBrain", "string")

def handleString(value):
    global pos, code, stdscr
    stdscr.addstr(pos_in, 0, "incoming: ".encode(code), curses.A_BOLD)
    stdscr.addstr(pos_in, pos_msg, (" " * pos_max).encode(code))
    stdscr.addstr(pos_in, pos["x"] + pos_msg, value.encode(code))
    stdscr.refresh()
    pos["y"] += 1


brew.subscribe("CloudBrain", handleString)

# set-up a variables to hold current position
pos = {"x": 0, "y": 0}

# line positions
pos_type = 0
pos_in = 0
pos_out = 0

# column positions
pos_msg = 10
pos_max = 60
pos_con = pos_msg + pos_max + 5

try:
    brew.start()
    stdscr.addstr(pos_type, 0, "new msg: ".encode(code), curses.A_BOLD)
    stdscr.refresh()

    column_str = stdscr.getyx()[1]
    cur_line = ""

    while 1:
        c = stdscr.getch()

        if (c == 10 or c == 13) and len(cur_line) > 0:
            brew.publish('chat outgoing', cur_line)
            stdscr.addstr(pos_type, pos_con, " cur_line sent      ".encode(code), curses.A_STANDOUT)
            stdscr.addstr(pos_out, 0, "outgoing: ".encode(code), curses.A_BOLD)
            stdscr.addstr(pos_out, pos_msg, (" " * pos_max).encode(code))
            stdscr.addstr(pos_out, pos_msg, cur_line.encode(code))

            cur_line = ""
            stdscr.addstr(pos_type, pos_msg, (" " * pos_max).encode(code))

        elif (c == 10 or c == 13) and len(cur_line) == 0:
            stdscr.addstr(pos_type, pos_con, " no message to send ".encode(code), curses.A_STANDOUT)

        elif c == curses.KEY_DC or c == curses.KEY_BACKSPACE or c == 127:
            cur_line = cur_line[0:-1]
            stdscr.addstr(pos_type, (pos["x"] + pos_msg + len(cur_line)), " ".encode(code))
            stdscr.addstr(pos_type, pos_con, "                     ".encode(code))

        elif len(cur_line) >= (pos_max):
            stdscr.addstr(pos_type, pos_con, " your at my limit   ".encode(code), curses.A_STANDOUT)

        elif c < 256 and c > 0:
            cur_line += chr(c)
            stdscr.addstr(pos_type, pos["x"] + pos_msg, cur_line.encode(code))
            stdscr.addstr(pos_type, pos_con, "                     ".encode(code))

        stdscr.refresh()

# closing out the app and returning terminal to old settings
finally:
    brew.stop()
    curses.nocbreak()
    stdscr.keypad(0)
    curses.echo()
    curses.endwin()