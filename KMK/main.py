import board
import busio
from kmk.kmk_keyboard import KMKKeyboard
from kmk.keys import KC
from kmk.scanners.keypad import KeysScanner
from kmk.modules.tapdance import TapDance
from kmk.extensions.rgb import RGB, AnimationModes
import adafruit_ssd1306
from adafruit_display_text import label
import terminalio

keyboard = KMKKeyboard()

tapdance = TapDance()
keyboard.modules.append(tapdance)

modes=['1','2','3','4']
current_mode=0

def toggle_mode():
    global current_mode
    current_mode=(current_mode + 1) % len(modes)

rgb = RGB(
    pixel_pin=board.D10,
    num_pixels=4,
    val_limit=150,
    animation_mode=AnimationModes.RAINBOW,
    animation_speed=1,
)
keyboard.extensions.append(rgb)

PINS = [board.D0, board.D1, board.D3, board.D6, board.D7, board.D8]

keyboard.matrix = KeysScanner(
    pins=PINS,
    value_when_pressed=False,
    pull=True
)

if current_mode==0:
    MUTE_MEDIA = KC.TD(KC.AUDIO_MUTE, KC.MEDIA_PLAY_PAUSE)
    VOL_UP = KC.TD(KC.AUDIO_VOL_UP, toggle_mode())
    keyboard.keymap = [
        [
            VOL_UP,
            KC.AUDIO_VOL_DOWN,
            MUTE_MEDIA,
            KC.LALT(KC.TAB),
            KC.LWIN(KC.LCTL(KC.LEFT)),
            KC.LWIN(KC.LCTL(KC.RIGHT)),
        ]
    ]
elif current_mode==1:
    COPY = KC.TD(KC.LCTRL(KC.C), toggle_mode())
    keyboard.keymap = [
        [
            COPY,
            KC.LCTRL(KC.V),
            KC.LCTRL(KC.X),
            KC.LCTRL(KC.Z),
            KC.LCTRL(KC.Y),
            KC.LALT(KC.F4), 
        ]
    ]
elif current_mode==2:
    COPY = KC.TD("TBA", toggle_mode())
    keyboard.keymap = [
        [
            #TBA
        ]
    ]
elif current_mode==3:
    COPY = KC.TD("TBA", toggle_mode())
    keyboard.keymap = [
        [
            #TBA 
        ]
    ]


i2c = busio.I2C(board.D5, board.D6)
oled = adafruit_ssd1306.SSD1306_I2C(128, 32, i2c)

oled.fill(0)
oled.show()

oled.text(f"Current Mode: {modes[current_mode]}", 0, 15, 1)
oled.show()

if __name__ == "__main__":
    keyboard.go()
