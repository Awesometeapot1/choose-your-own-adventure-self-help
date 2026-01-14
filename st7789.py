# st7789.py (LOW-RAM)
# Direct-to-display ST7789 driver (no full-screen framebuffer)
#
# Constructor matches your previous file:
#   ST7789(spi, cs, dc, rst, bl, width=240, height=320, rotation=1)
#
# Provides:
#   fill(color), fill_rect(x,y,w,h,color), rect(x,y,w,h,color), text(s,x,y,color), show()

from machine import Pin
import framebuf
import time

class ST7789:
    def __init__(self, spi, cs, dc, rst, bl, width=240, height=320, rotation=1):
        self.spi = spi
        self.width = width
        self.height = height

        self.cs = Pin(cs, Pin.OUT, value=1)
        self.dc = Pin(dc, Pin.OUT, value=0)
        self.rst = Pin(rst, Pin.OUT, value=1)
        self.bl = Pin(bl, Pin.OUT, value=1)

        self.reset()
        self.init_display(rotation)
        self.bl.value(1)

        # small reusable line buffer (bytes)
        self._line_buf = None

    # -------------------------
    # Low-level helpers
    # -------------------------
    def reset(self):
        self.rst.value(0)
        time.sleep_ms(50)
        self.rst.value(1)
        time.sleep_ms(50)

    def _cmd(self, c):
        self.cs.value(0)
        self.dc.value(0)
        self.spi.write(bytearray([c]))
        self.cs.value(1)

    def _data(self, d):
        self.cs.value(0)
        self.dc.value(1)
        self.spi.write(d)
        self.cs.value(1)

    def init_display(self, rotation):
        # MADCTL
        self._cmd(0x36)
        # Your previous driver used 0x00 for rotation==0 else 0x60
        self._data(bytearray([0x00 if rotation == 0 else 0x60]))

        # COLMOD = 16-bit
        self._cmd(0x3A)
        self._data(bytearray([0x55]))

        self._cmd(0x11)  # Sleep out
        time.sleep_ms(120)
        self._cmd(0x29)  # Display on

    def _set_window(self, x0, y0, x1, y1):
        # Column addr set
        self._cmd(0x2A)
        self._data(bytearray([x0 >> 8, x0 & 0xFF, x1 >> 8, x1 & 0xFF]))
        # Row addr set
        self._cmd(0x2B)
        self._data(bytearray([y0 >> 8, y0 & 0xFF, y1 >> 8, y1 & 0xFF]))
        # Memory write
        self._cmd(0x2C)

    def _ensure_line_buf(self, w):
        # Allocate once and reuse; 2 bytes per pixel
        needed = w * 2
        if self._line_buf is None or len(self._line_buf) < needed:
            self._line_buf = bytearray(needed)

    # -------------------------
    # Drawing API
    # -------------------------
    def show(self):
        # No framebuffer, so nothing to "flush"
        pass

    def fill(self, c):
        self.fill_rect(0, 0, self.width, self.height, c)

    def fill_rect(self, x, y, w, h, c):
        if w <= 0 or h <= 0:
            return
        # clip
        if x < 0:
            w += x
            x = 0
        if y < 0:
            h += y
            y = 0
        if x + w > self.width:
            w = self.width - x
        if y + h > self.height:
            h = self.height - y
        if w <= 0 or h <= 0:
            return

        hi = (c >> 8) & 0xFF
        lo = c & 0xFF

        self._ensure_line_buf(w)
        lb = self._line_buf
        # fill one line worth of pixels
        for i in range(0, w * 2, 2):
            lb[i] = hi
            lb[i + 1] = lo

        self._set_window(x, y, x + w - 1, y + h - 1)

        # Stream h lines
        self.cs.value(0)
        self.dc.value(1)
        for _ in range(h):
            self.spi.write(lb[: w * 2])
        self.cs.value(1)

    def rect(self, x, y, w, h, c):
        # outline rectangle
        self.fill_rect(x, y, w, 1, c)
        self.fill_rect(x, y + h - 1, w, 1, c)
        self.fill_rect(x, y, 1, h, c)
        self.fill_rect(x + w - 1, y, 1, h, c)

    def text(self, s, x, y, c):
        # Render text into a small temporary framebuffer and blit it
        # Each char is 8x8 in framebuf's built-in font
        if not s:
            return

        w = len(s) * 8
        h = 8

        # Clip quickly if completely off-screen
        if x >= self.width or y >= self.height or x + w <= 0 or y + h <= 0:
            return

        # Create a small RGB565 buffer for the text line
        buf = bytearray(w * h * 2)
        fb = framebuf.FrameBuffer(buf, w, h, framebuf.RGB565)
        fb.fill(0)          # background = black/transparent-ish (we won't blend)
        fb.text(s, 0, 0, c) # draw text

        # Blit it: we just write the whole block (no alpha)
        # If you want background matching, draw a fill_rect first in main.py.
        x0 = x
        y0 = y
        x1 = x + w - 1
        y1 = y + h - 1

        # clip (simple left/top clipping by trimming buffer is expensive; instead just clamp window)
        # We'll do basic clamp and rely on your UI keeping x/y on-screen.
        if x0 < 0:
            x0 = 0
        if y0 < 0:
            y0 = 0
        if x1 >= self.width:
            x1 = self.width - 1
        if y1 >= self.height:
            y1 = self.height - 1

        # If clipped, easiest safe behavior is: don't draw (keeps code simple + stable)
        if (x1 - x0 + 1) != w or (y1 - y0 + 1) != h:
            return

        self._set_window(x0, y0, x1, y1)
        self._data(buf)
