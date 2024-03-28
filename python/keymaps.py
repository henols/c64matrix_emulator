# !/usr/bin/env python
# -*- coding: utf-8 -*-

from readchar import key

ESCAPE_ESCAPE = "\x1b\x1b" # Dubble escape
ESCAPE_BACKTICK = "\x1b\x60" # Escape + `
ESCAPE_BACKSLASH = "\x1b\x5c" # Escape + \
TAB_SHIFT = "\x1b\x5b\x5a"

LINE_PREFIX = "CommadLine:"
LOAD_8_1 = LINE_PREFIX + "load"+("{CURSOR_RIGHT}")*19+",8,1:"
LOAD_DIR = LINE_PREFIX + "load\"$\",8:{RETURN}"

alt_keys = {'COMMODORE', 'CTRL'}

matrix_map = {
    '1': 0x00, 'LEFT_ARROW': 0x01, 'CTRL': 0x02, 'RUN_STOP': 0x03, 'SPACE': 0x04, 'COMMODORE': 0x05, 'q': 0x06, '2': 0x07,
    '3': 0x08, 'w': 0x09, 'a': 0x0a, 'SHIFT_LEFT': 0x0b, 'z': 0x0c, 's': 0x0d, 'e': 0x0e, '4': 0x0f,
    '5': 0x10, 'r': 0x11, 'd': 0x12, 'x': 0x13, 'c': 0x14, 'f': 0x15, 't': 0x16, '6': 0x17,
    '7': 0x18, 'y': 0x19, 'g': 0x1a, 'v': 0x1b, 'b': 0x1c, 'h': 0x1d, 'u': 0x1e, '8': 0x1f,
    '9': 0x20, 'i': 0x21, 'j': 0x22, 'n': 0x23, 'm': 0x24, 'k': 0x25, 'o': 0x26, '0': 0x27,
    '+': 0x28, 'p': 0x29, 'l': 0x2a, ',': 0x2b, '.': 0x2c, ':': 0x2d, '@': 0x2e, '-': 0x2f,
    '£': 0x30, '*': 0x31, ';': 0x32, '/': 0x33, 'SHIFT_RIGHT': 0x34, '=': 0x35, 'UP_ARROW': 0x36, 'HOME': 0x37,
    'DEL': 0x38, 'RETURN': 0x39, 'CURSOR_RIGHT': 0x3a, 'CURSOR_DOWN': 0x3b, 'F1': 0x3c, 'F3': 0x3d, 'F5': 0x3e, 'F7': 0x3f,
}

matrix_map_sv = {
    '1': 0x00, 'LEFT_ARROW': 0x01, 'CTRL': 0x02, 'RUN_STOP': 0x03, 'SPACE': 0x04, 'COMMODORE': 0x05, 'q': 0x06, '2': 0x07,
    '3': 0x08, 'w': 0x09, 'a': 0x0a, 'SHIFT_LEFT': 0x0b, 'z': 0x0c, 's': 0x0d, 'e': 0x0e, '4': 0x0f,
    '5': 0x10, 'r': 0x11, 'd': 0x12, 'x': 0x13, 'c': 0x14, 'f': 0x15, 't': 0x16, '6': 0x17,
    '7': 0x18, 'y': 0x19, 'g': 0x1a, 'v': 0x1b, 'b': 0x1c, 'h': 0x1d, 'u': 0x1e, '8': 0x1f,
    '9': 0x20, 'i': 0x21, 'j': 0x22, 'n': 0x23, 'm': 0x24, 'k': 0x25, 'o': 0x26, '0': 0x27,
    '-': 0x28, 'p': 0x29, 'l': 0x2a, ',': 0x2b, '.': 0x2c, 'ö': 0x2d, 'å': 0x2e, '=': 0x2f,
    ':': 0x30, '@': 0x31, 'ä': 0x32, '/': 0x33, 'SHIFT_RIGHT': 0x34, ';': 0x35, 'UP_ARROW': 0x36, 'HOME': 0x37,
    'DEL': 0x38, 'RETURN': 0x39, 'CURSOR_RIGHT': 0x3a, 'CURSOR_DOWN': 0x3b, 'F1': 0x3c, 'F3': 0x3d, 'F5': 0x3e, 'F7': 0x3f,
}

special_keys = {
    'RESTORE':0x00,
    'WARM_RESET':0x01, 
    'COLD_RESET':0x02
}


# Filling the following slowly for my Mac as needed :)
# User-supplied keymaps are necessary -- To Do
key_map = {
                key.ENTER: "RETURN",  
                key.ESC: "RUN_STOP",  
                ESCAPE_ESCAPE: "RUN_STOP", # Dubble escape
                ESCAPE_BACKTICK: "SHIFT_LEFT+RUN_STOP", # Escape + `
                ESCAPE_BACKSLASH: "RUN_STOP+RESTORE", # Escape + \
                key.SPACE: "SPACE",  
                '!': "SHIFT_LEFT+1", 
                '"': "SHIFT_LEFT+2", 
                '#': "SHIFT_LEFT+3", 
                '$': "SHIFT_LEFT+4", 
                '%': "SHIFT_LEFT+5", 
                '&': "SHIFT_LEFT+6", 
                "'": "SHIFT_LEFT+7", 
                '(': "SHIFT_LEFT+8", 
                ')': "SHIFT_LEFT+9", 
                '`': "LEFT_ARROW", 
                '~': "SHIFT_LEFT+LEFT_ARROW", 
                '+': "SHIFT_LEFT+;", 
                '<': "SHIFT_LEFT+,", 
                '>': "SHIFT_LEFT+.", 
                '?': "SHIFT_LEFT+/", 
                '^': "UP_ARROW", 
                '*': "SHIFT_LEFT+:", 
                '\\': "RESTORE",  
                "_" : "COMMODORE+p",
                key.BACKSPACE: "DEL", 
                key.F1: "F1",  
                key.F2: "SHIFT_LEFT+F1",
                key.F3: "F3",  
                key.F4: "SHIFT_LEFT+F3",
                key.F5: "F5",  
                key.F6: "SHIFT_LEFT+F5",
                key.F7: "F7",  
                key.F8: "SHIFT_LEFT+F7",
                key.DOWN: "CURSOR_DOWN",  
                key.UP: "SHIFT_LEFT+CURSOR_DOWN",  
                key.RIGHT: "CURSOR_RIGHT",  
                key.LEFT: "SHIFT_LEFT+CURSOR_RIGHT",  
                key.TAB: "COMMODORE",  
                TAB_SHIFT: "CTRL",  
                key.INSERT: "SHIFT_LEFT+DEL",  
                key.HOME: "HOME",  
                key.DELETE: "SHIFT_LEFT+HOME",  
                key.CTRL_W: 'WARM_RESET', 
                key.CTRL_R:'COLD_RESET',
                key.CTRL_D: LOAD_DIR,
                key.CTRL_L: LOAD_8_1,
              }