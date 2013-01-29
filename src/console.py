# -*- coding: utf-8 -*-
'''
InteractiveConsole class is raw_input() re-implementation.

Usage:
  con = InteractiveConsole()
  print con('> ')

Created on 26-12-2012

@author: Karol Tomala
@todo: Unicode characters deletion
'''

import sys
from getch import getch

UNICODE_ESCAPE = range(194,244)

class InteractiveConsole(object):
    def __init__(self):
        self.unicode_term = True if sys.stdout.encoding == 'UTF-8' else False
        self.buf = ''
        self.bufpos = 0
    
    def clear_buf(self):
        self.buf = ''
    
    def handle_escape(self, key):
        """Handle escape sequences.
        Can be overloaded in custom implementations.
        """
        if key == 'C':
            if self.bufpos < len(self.buf):
                sys.stdout.write(self.buf[self.bufpos])
                self.bufpos += 1
        if key == 'D':
            if self.bufpos > 0:
                sys.stdout.write('\b')
                self.bufpos -= 1
#        if key == 'A':
#            print self.bufpos
#            print self.buf[:self.bufpos] if self.bufpos > 0 else ''
#        if key == 'B':
#            print self.bufpos
#            print self.buf[self.bufpos:] if self.bufpos <= len(self.buf) else ''
    
    def line_input(self, prompt=''):
        """Line input method.
        """
        self.bufpos = 0
        self.clear_buf()
        sys.stdout.write(prompt)
        sys.stdout.flush()
        
        escape = False
        probable_escape = False
        while True:
            deleted = 0
            key = getch()
            if probable_escape:
                if key == '[':
                    escape = True
                    probable_escape = False
                    continue
            if escape:
                self.handle_escape(key)
                escape = False
                continue
            if ord(key) == 13:
                sys.stdout.write('\n')
                break
            elif ord(key) == 126:
                if self.bufpos < len(self.buf):
                    left = self.buf[:self.bufpos]
                    right = self.buf[self.bufpos+1:] if self.bufpos+1 < len(self.buf) else ''
                    self.buf = left + right
                    deleted = 1
            elif ord(key) == 127:
                if self.bufpos > 0:
#                    if self.unicode_term:
#                        try:
#                            if ord(self.buf[self.bufpos-2]) in UNICODE_ESCAPE:
#                                buf = self.buf[:self.bufpos-1] + self.buf[self.bufpos+1:]
#                        except IndexError:
#                            pass
#                    print self.bufpos
                    if self.bufpos > 0:
                        left = self.buf[:self.bufpos-1]
                    else:
                        left = ''
                    if self.bufpos < len(self.buf):
                        right = self.buf[self.bufpos:]
                    else:
                        right = ''
                    self.buf = left + right
                    self.bufpos -= 1
                    deleted = 1
            elif key == '\x1b':
                probable_escape = True
                continue
            else:
                left = self.buf[:self.bufpos] if self.bufpos > 0 else ''
                right = self.buf[self.bufpos:] if self.bufpos < len(self.buf) else ''
                self.buf = left + key + right
                self.bufpos += 1

            cursor = (len(prompt) + len(self.buf) - self.bufpos - (2 - deleted)) * '\b'
            line = '\r' + prompt + self.buf + deleted * ' ' + cursor
            sys.stdout.write(line)
            

        buf = self.buf
        self.clear_buf()
        return buf
    
    def __call__(self, prompt=''):
        return self.line_input(prompt)
    