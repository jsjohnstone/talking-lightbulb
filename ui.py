import urwid
import sounddevice as sd
import numpy
import pyenttec as dmx
import sys

motd = """
  ..---..  
 /       \      ／￣￣￣￣￣￣￣￣ ￣ ￣
|         |    <   MasterBulb v0.1
:         ;     ＼＿＿＿＿＿＿ ＿
 \  \~/  /
  `, Y ,'
   |_|_|
   |===|
   |===|
    \_/
"""
print(motd)

def print_sound(indata, frames, time, status):
    global outputbar
    volume = numpy.linalg.norm(indata)*10
    dmx_value = int(max(min(255, ((volume / 1000) * 255)), 0))
    port.dmx_frame[5] = dmx_value
    port.render()
    bargraph = dmx_value / 8
    percentage = int(dmx_value / 2.55)
	#sys.stdout.write(("\rListening: {0:0=2d}% - [" + ("#" * int(bargraph)).ljust(32," ")).format(percentage) + "]")
	#sys.stdout.flush()
    outputbar.set_completion(percentage)

# Setup DMX Connection
print("------------------------------------------------------------")
print ("Let's do some setup...")
print("------------------------------------------------------------")
print("SOUND SETUP:")
sound_input = None
while sound_input == None:
	print("Available sound devices:")
	print(sd.query_devices())
	sound_input = int(input("Which device is your input? "))

print("Selected Device {}".format(sound_input))
print("------------------------------------------------------------")
print("DMX SETUP:")
port = dmx.select_port()
print("------------------------------------------------------------")
print (" (v)   I'm ready to speak now...")
print ("  =    Press Ctrl+C to kill me at any time.")
print("------------------------------------------------------------")




palette = [
        ('footer_green', 'black', 'dark cyan', 'standout'),
        ('key', 'yellow', 'dark blue', 'bold'),
        ('listbox', 'light gray', 'black' ),
        ('body',         'black',      'light gray', 'standout'),
        ('footer_red',       'white',      'dark red',   'bold'),
        ('screen edge',  'light blue', 'dark cyan'),
        ('main shadow',  'dark gray',  'black'),
        ('line',         'black',      'light gray', 'standout'),
        ('bg background','light gray', 'black'),
        ('bg 1',         'black',      'dark blue', 'standout'),
        ('bg 1 smooth',  'dark blue',  'black'),
        ('bg 2',         'black',      'dark cyan', 'standout'),
        ('bg 2 smooth',  'dark cyan',  'black'),
        ('button normal','light gray', 'dark gray', 'standout'),
        ('button select','white',      'dark blue'),
        ('line',         'black',      'light gray', 'standout'),
        ('pg normal',    'white',      'black', 'standout'),
        ('pg complete',  'white',      'dark magenta'),
        ('pg smooth',     'dark magenta','black')
        ]

def button(t, fn):
    w = urwid.Button(t, fn)
    w = urwid.AttrWrap(w, 'button normal', 'button select')
    return w

def nullfunction():
    return

def start(w):
    try:
	    while True:
	    	with sd.InputStream(callback=print_sound, device=sound_input):
	    		sd.sleep(100000)
    except KeyboardInterrupt:
        port.dmx_frame[5] = 0
        port.render()
        port.close()
        print("\rTerminated with Ctrl+C. See you tomorrow night!")
        pass

footer = urwid.Text("[CTRL+C] Exit   [CTRL+I] Change Input    [CTRL+D] Change DMX     [CTRL+L] Change Fixture     [CTRL+P] Pause/Unpause")
footer = urwid.AttrWrap(footer,'footer_red')

header = urwid.Padding(
                urwid.BigText(('body', "Lightbulb"), urwid.HalfBlock5x4Font()),width='clip')

log_messages = [urwid.Text("Press Enter when done"), urwid.Text("Prfff when done"), urwid.Text("Press Eddder when done"), urwid.Text("Predddter when done")]
walker = urwid.SimpleFocusListWalker(contents=log_messages)
logger_box = urwid.ListBox(walker)


settings_l = [urwid.Text("Input Device: 2 Soundflower"),
            button("[CTRL+I] Change Input Device", nullfunction),
            urwid.Divider(),
            urwid.Text("DMX Device: 3"),
            button("[CTRL+D] Change DMX Device", nullfunction),
            button("[CTRL+D] Start", start)
            ]
settings = urwid.ListBox(urwid.SimpleListWalker(settings_l))

logger_widget = urwid.LineBox(logger_box, title="Logs", title_align='left')
settings_widget = urwid.LineBox(settings,title="Settings", title_align='left')

main_columns = urwid.Columns([
            settings_widget,
            logger_widget
        ])

outputbar = urwid.ProgressBar('pg normal', 'pg complete', current=20, done=100, satt=None)
progress = urwid.LineBox(outputbar, title="Output", title_align='left')

main_app = urwid.Frame(main_columns,progress)

### main framing/styling
w = urwid.Frame(main_app, header, footer)

bg = urwid.AttrWrap(urwid.SolidFill(u"\u2592"), 'screen edge')
shadow = urwid.AttrWrap(urwid.SolidFill(u" "), 'main shadow')

w = urwid.Padding(w,('fixed left',1),('fixed right',0))
w = urwid.AttrWrap(w,'body')
w = urwid.LineBox(w)
w = urwid.AttrWrap(w,'line')

bg = urwid.Overlay( shadow, bg,
    ('fixed left', 3), ('fixed right', 1),
            ('fixed top', 2), ('fixed bottom', 1))
w = urwid.Overlay( w, bg,
    ('fixed left', 2), ('fixed right', 3),
    ('fixed top', 1), ('fixed bottom', 2))

loop = urwid.MainLoop(w, palette)
loop.run()