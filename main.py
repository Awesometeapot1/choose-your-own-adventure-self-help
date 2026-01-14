# main.py
# Story Pico W + ST7789 2" LCD (320x240 landscape)
# OLED: big, paged story text (choices only on website)
# Website: choices + Prev/Next page + back/refresh
#
# Text is rendered at TRUE SCALE using a scaled mono font draw
# to avoid the "tiny text" problem.

from machine import Pin, SPI
import time
import framebuf

from wifi_buttons import WiFiButtons
from story_data import STORIES
from st7789 import ST7789

# -------------------------
# PINS
# -------------------------
SPI_ID = 0
SCK  = 18
MOSI = 19

LCD_CS  = 17
LCD_DC  = 20
LCD_RST = 21
LCD_BL  = 22

# -------------------------
# DISPLAY
# -------------------------
W, H = 320, 240

spi = SPI(
    SPI_ID,
    baudrate=40_000_000,
    polarity=0,
    phase=0,
    sck=Pin(SCK),
    mosi=Pin(MOSI),
    miso=None,
)

lcd = ST7789(
    spi,
    LCD_CS,
    LCD_DC,
    LCD_RST,
    LCD_BL,
    width=W,
    height=H,
    rotation=1,
)

# -------------------------
# COLOURS (RGB565) - nicer palette
# -------------------------
BG      = 0x0861   # very dark blue-grey
PANEL   = 0x10A2   # header/footer panel
PANEL2  = 0x18E3   # slightly lighter panel strip
TEXT    = 0xFFFF   # white
MUTED   = 0xBDF7   # light grey
ACCENT  = 0x07FF   # cyan (calm, accessible)
LINE    = 0x4208   # subtle divider

# -------------------------
# TEXT SCALE (bigger!)
# -------------------------
SCALE_STORY  = 2  # try 3; if you want even bigger, set to 4 (fewer words per page)
SCALE_HEADER = 2

FONT_W = 8
FONT_H = 8

# margins
MARGIN_X = 12
MARGIN_Y = 10

def safe_show():
    # framebuffer drivers need show(); direct drivers can ignore it
    try:
        lcd.show()
    except:
        pass

# -------------------------
# Fix "grey boxes" (unicode -> ASCII)
# -------------------------
def safe_ascii(s):
    if s is None:
        return ""
    s = str(s)
    rep = {
        "“": '"', "”": '"', "„": '"',
        "‘": "'", "’": "'", "‚": "'",
        "–": "-", "—": "-",
        "…": "...",
        "\u00A0": " ",
    }
    for a, b in rep.items():
        s = s.replace(a, b)
    return "".join(ch if ord(ch) < 128 else "?" for ch in s)

# -------------------------
# Wrap + paging
# -------------------------
def wrap_text(s, max_chars):
    out = []
    for para in s.split("\n"):
        if para.strip() == "":
            out.append("")
            continue
        words = para.split(" ")
        line = ""
        for w in words:
            if not line:
                line = w
            elif len(line) + 1 + len(w) <= max_chars:
                line += " " + w
            else:
                out.append(line)
                line = w
        if line:
            out.append(line)
    return out

def chunk_pages(lines, lines_per_page):
    if lines_per_page < 1:
        lines_per_page = 1
    pages = []
    for i in range(0, len(lines), lines_per_page):
        pages.append(lines[i:i + lines_per_page])
    if not pages:
        pages = [[""]]
    return pages

class Pager:
    def __init__(self):
        self.node = None
        self.pages = [[""]]
        self.page_i = 0

    def rebuild_for_node(self, node_id, text, max_chars, lines_per_page):
        # reset to page 0 when node changes
        if self.node != node_id:
            self.node = node_id
            self.page_i = 0

        lines = wrap_text(text, max_chars)
        self.pages = chunk_pages(lines, lines_per_page)

        if self.page_i >= len(self.pages):
            self.page_i = len(self.pages) - 1
        if self.page_i < 0:
            self.page_i = 0

    def page_count(self):
        return len(self.pages)

    def page_num(self):
        return self.page_i + 1

    def current_lines(self):
        return self.pages[self.page_i]

    def next(self):
        if self.page_i < len(self.pages) - 1:
            self.page_i += 1

    def prev(self):
        if self.page_i > 0:
            self.page_i -= 1

# -------------------------
# TRUE scaled text renderer (fast-ish)
# -------------------------
def draw_text_scaled(s, x, y, color, scale):
    """
    Renders text using framebuf's built-in 8x8 font into a MONO buffer,
    then draws it scaled up by 'scale' using filled rectangles.
    Uses horizontal run batching to reduce fill_rect calls.
    """
    s = safe_ascii(s)
    if not s:
        return

    # Render to mono buffer first
    w = len(s) * FONT_W
    h = FONT_H
    stride = (w + 7) // 8
    buf = bytearray(stride * h)
    fb = framebuf.FrameBuffer(buf, w, h, framebuf.MONO_HLSB)
    fb.fill(0)
    fb.text(s, 0, 0, 1)

    # Draw scaled runs
    for yy in range(h):
        run_start = -1
        for xx in range(w):
            px = fb.pixel(xx, yy)
            if px and run_start < 0:
                run_start = xx
            elif (not px) and run_start >= 0:
                run_w = xx - run_start
                lcd.fill_rect(x + run_start * scale, y + yy * scale, run_w * scale, scale, color)
                run_start = -1
        if run_start >= 0:
            run_w = w - run_start
            lcd.fill_rect(x + run_start * scale, y + yy * scale, run_w * scale, scale, color)

# -------------------------
# STORY ENGINE (node history + Return-to-Map memory)
# -------------------------
class StoryEngine:
    def __init__(self, stories_dict):
        self.stories = stories_dict
        self.story_names = list(stories_dict.keys())
        self.story_index = 0

        self.node_id = "start"
        self.history = []
        self.last_map_node = "start"

    def story_title(self):
        return self.story_names[self.story_index]

    def current_story(self):
        return self.stories[self.story_title()]

    def current_node(self):
        story = self.current_story()
        return story.get(self.node_id, story.get("start", {"text": "Missing node", "choices": []}))

    def _track_map_if_needed(self):
        if isinstance(self.node_id, str) and self.node_id.startswith("map_"):
            self.last_map_node = self.node_id

    def reset(self):
        self.node_id = "start"
        self.history = []
        self.last_map_node = "start"
        self._track_map_if_needed()

    def can_back(self):
        return len(self.history) > 0

    def go_back(self):
        if self.history:
            self.node_id = self.history.pop()
            self._track_map_if_needed()

    def goto(self, node_id, push_history=True):
        if push_history:
            self.history.append(self.node_id)
        self.node_id = node_id
        self._track_map_if_needed()

    def choose(self, idx):
        node = self.current_node()
        choices = node.get("choices", [])
        if idx < 0 or idx >= len(choices):
            return

        label, next_id = choices[idx]

        if label == "Return to Map":
            target = self.last_map_node if self.last_map_node else "start"
            self.goto(target, push_history=True)
            return

        self.goto(next_id, push_history=True)

# -------------------------
# RENDER (nicer UI + paging)
# -------------------------
def render(engine, pager):
    lcd.fill(BG)

    node = engine.current_node()
    title = safe_ascii(engine.story_title())
    text = safe_ascii(node.get("text", ""))

    header_h = 42
    footer_h = 22

    # Header
    lcd.fill_rect(0, 0, W, header_h, PANEL)
    lcd.fill_rect(0, header_h - 2, W, 2, PANEL2)

    max_title_chars = (W - 2 * MARGIN_X) // (FONT_W * SCALE_HEADER)
    if max_title_chars < 1:
        max_title_chars = 1
    draw_text_scaled(title[:max_title_chars], MARGIN_X, 10, TEXT, SCALE_HEADER)

    story_scale = SCALE_STORY
    char_w = FONT_W * story_scale
    line_h = FONT_H * story_scale

    max_chars = (W - 2 * MARGIN_X) // char_w
    if max_chars < 8:
        max_chars = 8

    y0 = header_h + 10
    usable_h = H - y0 - footer_h - 8
    lines_per_page = usable_h // line_h
    if lines_per_page < 1:
        lines_per_page = 1

    pager.rebuild_for_node(engine.node_id, text, max_chars, lines_per_page)

    lcd.fill_rect(8, y0 - 6, W - 16, usable_h + 12, BG)

    y = y0
    for ln in pager.current_lines():
        draw_text_scaled(ln, MARGIN_X, y, TEXT, story_scale)
        y += line_h

    # Footer
    lcd.fill_rect(0, H - footer_h, W, footer_h, PANEL)
    lcd.fill_rect(0, H - footer_h, W, 1, LINE)

    # Page indicator
    page_str = "Page %d/%d" % (pager.page_num(), pager.page_count())
    px = W - MARGIN_X - (len(page_str) * 8)
    if px < MARGIN_X:
        px = MARGIN_X
    lcd.text(page_str, px, H - footer_h + 7, ACCENT)

    safe_show()

# -------------------------
# WIFI + APP LOOP
# -------------------------
wifi = WiFiButtons(ssid="StoryPico", password="12345678")
engine = StoryEngine(STORIES)
engine._track_map_if_needed()
pager = Pager()

def sync_web():
    """
    Push current choices + paging state to the phone webpage.

    Works with both older and newer wifi_buttons.py:
      - set_choices(labels)
      - set_paging(page, pages)   (positional or keyword)
      - set_screen_info(title, subtitle, can_back)  (extra kwargs ignored if supported)
    """
    node = engine.current_node()
    choices = node.get("choices", [])
    wifi.set_choices([safe_ascii(c[0]) for c in choices])

    p = pager.page_num()
    pc = pager.page_count()

    # Always update paging if available
    try:
        wifi.set_paging(p, pc)
    except:
        pass

    # Basic screen info (safe everywhere); pass extras if supported
    try:
        wifi.set_screen_info(
            title=safe_ascii(engine.story_title()),
            subtitle=safe_ascii(engine.node_id),
            can_back=engine.can_back(),
            page=p, pages=pc,
            can_prev=(p > 1), can_next=(p < pc),
        )
    except TypeError:
        wifi.set_screen_info(
            safe_ascii(engine.story_title()),
            safe_ascii(engine.node_id),
            engine.can_back()
        )

# Initial: build pager via render first, then sync website
render(engine, pager)
sync_web()

while True:
    ev = wifi.poll()
    if ev:
        t = ev.get("type")

        if t == "choice":
            engine.choose(ev.get("index", -1))

        elif t == "back":
            engine.go_back()

        elif t == "refresh":
            engine.reset()

        elif t == "page":
            d = ev.get("dir", 0)
            if d > 0:
                pager.next()
            elif d < 0:
                pager.prev()

        render(engine, pager)
        sync_web()

    time.sleep_ms(20)
