# wifi_buttons.py
# Pico W AP + tiny HTTP server (phone-friendly).
#
# API expected by main.py:
#   wifi.set_screen_info(title, subtitle="", can_back=False, **kwargs)  # tolerant
#   wifi.set_choices([label1, label2, ...])
#   wifi.set_paging(page=1, pages=1)   # positional OR keyword, tolerant
#   ev = wifi.poll() -> dict event or None
#
# poll() events:
#   {"type":"choice","index":i}
#   {"type":"back"}
#   {"type":"refresh"}
#   {"type":"page","dir":-1 or +1}

import network
import socket
import time


def _esc(s):
    if s is None:
        return ""
    s = str(s)
    return (s.replace("&", "&amp;")
             .replace("<", "&lt;")
             .replace(">", "&gt;")
             .replace('"', "&quot;")
             .replace("'", "&#39;"))


class WiFiButtons:
    def __init__(self, ssid="StoryPico", password="12345678", port=80):
        self._title = "Story Pico"
        self._subtitle = ""
        self._can_back = False
        self._choices = []
        self._page = 1
        self._pages = 1
        self._can_prev = False
        self._can_next = False

        # --- Start Access Point ---
        ap = network.WLAN(network.AP_IF)
        ap.active(True)

        # MicroPython varies across builds; try both config styles.
        try:
            if password and len(password) >= 8:
                ap.config(essid=ssid, password=password)
            else:
                ap.config(essid=ssid)  # open if password invalid/empty
        except TypeError:
            if password and len(password) >= 8:
                ap.config(ssid=ssid, password=password)
            else:
                ap.config(ssid=ssid)

        time.sleep_ms(300)

        self._ip = "192.168.4.1"
        try:
            self._ip = ap.ifconfig()[0]
        except:
            pass

        # --- HTTP socket ---
        addr = socket.getaddrinfo("0.0.0.0", port)[0][-1]
        s = socket.socket()
        try:
            s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        except:
            pass
        s.bind(addr)
        s.listen(2)
        s.setblocking(False)
        self.sock = s

        print("AP ready:", ssid)
        print("Open on phone: http://%s/" % self._ip)

    # =========================================================
    # Public API (called by main.py)
    # =========================================================

    def set_screen_info(self, title, subtitle="", can_back=False, **kwargs):
        # Tolerant: accept extra keyword args used by some main.py versions
        # (page, pages, can_prev, can_next) without crashing.
        self._title = title or ""
        self._subtitle = subtitle or ""
        self._can_back = bool(can_back)

        # Optional paging info
        if "page" in kwargs or "pages" in kwargs:
            self.set_paging(page=kwargs.get("page", self._page),
                            pages=kwargs.get("pages", self._pages))

        # Optional explicit prev/next enable flags
        if "can_prev" in kwargs:
            self._can_prev = bool(kwargs.get("can_prev"))
        if "can_next" in kwargs:
            self._can_next = bool(kwargs.get("can_next"))

    def set_choices(self, choices):
        self._choices = list(choices) if choices else []

    def set_paging(self, *args, **kwargs):
        # Accept any calling style without crashing:
        #   set_paging(1, 3)
        #   set_paging(page=1, pages=3)
        #   set_paging(page=1, pages=3, whatever=...)
        page = 1
        pages = 1

        if len(args) >= 1:
            page = args[0]
        if len(args) >= 2:
            pages = args[1]

        if "page" in kwargs:
            page = kwargs["page"]
        if "pages" in kwargs:
            pages = kwargs["pages"]

        try:
            page = int(page)
            pages = int(pages)
        except:
            page, pages = 1, 1

        if pages < 1:
            pages = 1
        if page < 1:
            page = 1
        if page > pages:
            page = pages

        self._page = page
        self._pages = pages

        # default enable based on bounds if caller didn't set can_prev/can_next
        self._can_prev = (self._page > 1)
        self._can_next = (self._page < self._pages)

    # =========================================================
    # Poll for web events (non-blocking)
    # =========================================================

    def poll(self):
        try:
            cl, _ = self.sock.accept()
        except:
            return None

        try:
            req = cl.recv(1024).decode("utf-8", "ignore")
        except:
            req = ""

        path = self._parse_path(req)

        # Always serve the control page
        try:
            cl.send(self._http(self._html()))
        except:
            pass

        try:
            cl.close()
        except:
            pass

        # Ignore browser noise
        if not path or path == "/" or path.startswith("/favicon"):
            return None

        # Choice click: /c?i=N
        if path.startswith("/c"):
            idx = self._qint(path, "i", -1)
            if 0 <= idx < len(self._choices):
                return {"type": "choice", "index": idx}
            return None

        # Page: /page?dir=-1 or +1
        if path.startswith("/page"):
            d = self._qint(path, "dir", 0)
            if d < 0:
                return {"type": "page", "dir": -1}
            if d > 0:
                return {"type": "page", "dir": 1}
            return None

        # Back: /back
        if path.startswith("/back"):
            if self._can_back:
                return {"type": "back"}
            return None

        # Refresh: /refresh
        if path.startswith("/refresh"):
            return {"type": "refresh"}

        return None

    # =========================================================
    # Internal helpers
    # =========================================================

    def _parse_path(self, req):
        # "GET /path HTTP/1.1"
        try:
            line = req.split("\r\n", 1)[0]
            parts = line.split(" ")
            if len(parts) >= 2 and parts[0] == "GET":
                return parts[1]
        except:
            pass
        return None

    def _qint(self, path, key, default=0):
        # parse query string int key=value
        try:
            if "?" not in path:
                return default
            qs = path.split("?", 1)[1]
            for kv in qs.split("&"):
                if "=" in kv:
                    k, v = kv.split("=", 1)
                    if k == key:
                        return int(v)
        except:
            pass
        return default

    def _http(self, html):
        return (
            "HTTP/1.0 200 OK\r\n"
            "Content-Type: text/html; charset=utf-8\r\n"
            "Cache-Control: no-store\r\n"
            "Connection: close\r\n"
            "\r\n" + html
        )

    # =========================================================
    # HTML page
    # =========================================================

    def _html(self):
        title = _esc(self._title)
        sub = _esc(self._subtitle)

        # Choices as big buttons
        choices_html = ""
        for i, lbl in enumerate(self._choices):
            choices_html += (
                f'<a class="link" href="/c?i={i}">'
                f'<button class="btn choice">{_esc(lbl)}</button></a>'
            )

        if not choices_html:
            choices_html = '<div class="empty">No choices on this screen.</div>'

        # Paging controls only shown if pages > 1
        paging_html = ""
        if self._pages > 1:
            prev_dis = "disabled" if (self._page <= 1 or (hasattr(self, "_can_prev") and not self._can_prev)) else ""
            next_dis = "disabled" if (self._page >= self._pages or (hasattr(self, "_can_next") and not self._can_next)) else ""
            paging_html = f"""
            <div class="row">
              <a class="link" href="/page?dir=-1"><button class="btn small" {prev_dis}>◀ Prev</button></a>
              <div class="page">{self._page} / {self._pages}</div>
              <a class="link" href="/page?dir=1"><button class="btn small" {next_dis}>Next ▶</button></a>
            </div>
            """

        back_html = ""
        if self._can_back:
            back_html = '<a class="link" href="/back"><button class="btn small">↩ Back</button></a>'
        else:
            back_html = "<div></div>"

        refresh_html = '<a class="link" href="/refresh"><button class="btn small">⟲ Refresh</button></a>'

        return f"""<!doctype html>
<html>
<head>
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<style>
  body {{
    font-family: system-ui, -apple-system, Segoe UI, Roboto, Arial, sans-serif;
    margin: 16px;
    background: #0b0f14;
    color: #e8eef6;
  }}
  .card {{
    max-width: 560px;
    margin: 0 auto;
    padding: 14px;
    background: #121926;
    border-radius: 16px;
    box-shadow: 0 8px 30px rgba(0,0,0,.35);
  }}
  h1 {{
    font-size: 20px;
    margin: 0 0 6px 0;
    line-height: 1.2;
  }}
  .sub {{
    font-size: 14px;
    opacity: .85;
    margin-bottom: 12px;
  }}
  .row {{
    display: flex;
    gap: 10px;
    align-items: center;
    justify-content: space-between;
    margin: 10px 0;
  }}
  .page {{
    flex: 1;
    text-align: center;
    opacity: .9;
    font-size: 14px;
  }}
  .btn {{
    width: 100%;
    border: 0;
    border-radius: 14px;
    padding: 16px 14px;
    font-size: 18px;
    font-weight: 650;
    background: #20314a;
    color: #e8eef6;
    box-shadow: inset 0 0 0 1px rgba(255,255,255,.08);
  }}
  .btn.small {{
    padding: 12px 12px;
    font-size: 16px;
    background: #162033;
  }}
  .btn.choice {{
    margin: 10px 0;
    background: #20314a;
    text-align: left;
  }}
  .btn[disabled] {{
    opacity: .45;
  }}
  .link {{
    display: block;
    text-decoration: none;
  }}
  .empty {{
    opacity: .8;
    font-size: 14px;
    padding: 10px 0;
  }}
  .footer {{
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 10px;
    margin-top: 12px;
  }}
</style>
</head>
<body>
  <div class="card">
    <h1>{title}</h1>
    <div class="sub">{sub}</div>

    {paging_html}

    <div class="choices">
      {choices_html}
    </div>

    <div class="footer">
      {back_html}
      {refresh_html}
    </div>
  </div>
</body>
</html>
"""
