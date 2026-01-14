

StoryPico – Pico W Choose‑Your‑Own‑Adventure Engine

Overview

StoryPico is a choose‑your‑own‑adventure engine running on a Raspberry Pi Pico W.

Story text is displayed on a 320×240 ST7789 LCD

A phone connects to the Pico’s Wi‑Fi access point

A small web UI provides large, touch‑friendly buttons

Button presses are converted into events that drive the story


This design cleanly separates content, logic, UI, and hardware drivers.


---

File Structure

StoryPico/
├── main.py          # Application logic & event loop
├── story_data.py    # Story graph (content only)
├── wifi_buttons.py  # Phone web UI + HTTP server
└── st7789.py        # LCD display driver


---

High‑Level Architecture

Phone (Safari/Browser)
        │
        ▼
  HTTP Requests (/c, /page, /back)
        │
        ▼
 wifi_buttons.poll()
        │   (returns event dict)
        ▼
     main.py
  ├─ StoryEngine (node + history)
  ├─ Pager (text paging)
  └─ Renderer (LCD)
        │
        ▼
  ST7789 LCD Display


---

story_data.py – Story Content

Purpose

Contains only story data, no logic.

Structure

STORIES = {
  "Story Name": {
    "start": {
      "text": "You stand at the edge of a forest...",
      "choices": [
        ("Enter the woods", "map_forest"),
        ("Walk away", "end")
      ]
    },
    "map_forest": {
      "text": "Paths stretch in all directions...",
      "choices": [
        ("Go north", "north_path"),
        ("Return to Map", "Return to Map")
      ]
    }
  }
}

Concepts

Node: a story state (text + choices)

Choice: (label, next_node_id)

Nodes whose IDs start with map_ are treated as hubs

A choice labeled "Return to Map" jumps back to the last visited map node



---

st7789.py – LCD Driver

Purpose

Low‑RAM SPI driver for the ST7789 LCD.

Key Characteristics

No full‑screen framebuffer

Draws directly to the display

Efficient for Pico’s limited RAM


Important Methods

fill(color) – clear screen

fill_rect(x, y, w, h, color) – draw rectangles (core primitive)

text(str, x, y, color) – small text drawing

show() – usually a no‑op (no framebuffer)



---

wifi_buttons.py – Phone Web UI

Purpose

Turns the Pico W into:

A Wi‑Fi access point

A tiny HTTP server

A button‑to‑event bridge


Public API (used by main.py)

wifi.set_choices(["Go left", "Go right"])
wifi.set_paging(page, pages)
wifi.set_screen_info(title, subtitle, can_back)

HTTP Endpoints

URL	Meaning	Event Returned

/	Show control UI	None
/c?i=N	Choice button	{type:"choice", index:N}
/page?dir=-1	Previous page	{type:"page", dir:-1}
/page?dir=1	Next page	{type:"page", dir:1}
/back	Back	{type:"back"}
/refresh	Restart	{type:"refresh"}


Key Idea

The web page is stateless UI. All real state lives in main.py.


---

main.py – Application Logic

Responsibilities

Hardware setup (SPI, LCD)

Story navigation

Text wrapping and paging

Rendering to LCD

Handling web events


Core Components

StoryEngine

Tracks current node_id

Maintains history stack for Back

Remembers last map_ node


Pager

Wraps text into lines

Groups lines into pages

Tracks current page index


Renderer

Draws header, story text, footer

Uses scaled text for readability



---

Event Loop (Core Logic)

while True:
    ev = wifi.poll()
    if ev:
        handle_event(ev)
        render(engine, pager)
        sync_web()

Event Handling

Event	Action

choice	Move to next node
page	Change page
back	Pop history
refresh	Reset story



---

Text Rendering & Paging

Text is wrapped by character count, not pixels

Wrapped lines are chunked into pages

Pager resets automatically when node changes


This guarantees:

Large readable text

Consistent paging across LCD and web UI



---

Common Debug Notes

Buttons don’t respond → check poll() parsing

Need two taps → browser refresh timing

Prev/Next missing → page count is 1

Back missing → history stack empty



---

One‑Sentence Summary

> “StoryPico is an event‑driven story engine where phone button presses are turned into events that update a paged story rendered on an ST7789 LCD.”




---

Author Notes

This project demonstrates:

Event‑driven design on microcontrollers

Low‑RAM graphics techniques

Separation of content and logic

Practical embedded web UI design