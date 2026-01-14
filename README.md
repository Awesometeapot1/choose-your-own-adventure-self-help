

# **StoryPico – Pico W Choose‑Your‑Own‑Adventure Engine**

## **Overview**

**StoryPico** is a choose‑your‑own‑adventure engine designed for the **Raspberry Pi Pico W**.  
It displays story content on a **320×240 ST7789 LCD** while a phone connects to a Pico‑hosted Wi‑Fi access point to control the story through a simple touch‑friendly web UI.

**Key Features**
- Story text shown on ST7789 LCD  
- Phone connects to Pico’s Wi‑Fi AP  
- Web UI provides large choice buttons  
- Button presses produce events that drive the story engine  
- Clean separation of **content**, **logic**, **UI**, and **hardware drivers**

---

# **File Structure**

```
StoryPico/
├── main.py          # Application logic & event loop
├── story_data.py    # Story graph (content only)
├── wifi_buttons.py  # Phone web UI + HTTP server
└── st7789.py        # LCD display driver
```

---

# **High‑Level Architecture**

```
Phone (Safari/Browser)
        │
        ▼
  HTTP Requests (/c, /page, /back)
        │
        ▼
  wifi_buttons.poll()
        │     (returns event dict)
        ▼
      main.py
   ├─ StoryEngine (node + history)
   ├─ Pager (text paging)
   └─ Renderer (LCD)
        │
        ▼
  ST7789 LCD Display
```

---

# **story_data.py — Story Content**

## **Purpose**
Holds **only story data**—no logic.

## **Structure**
```python
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
```

## **Concepts**
- **Node:** a story state containing `text` + `choices`
- **Choice:** tuple `(label, next_node_id)`
- Node IDs starting with **map_** act as navigation hubs  
- The special choice label **"Return to Map"** jumps back to the most recently visited map node

---

# **st7789.py — LCD Driver**

## **Purpose**
RAM‑efficient SPI driver for the **ST7789 LCD**, optimized for the Pico’s limited memory.

## **Key Characteristics**
- No full‑screen framebuffer  
- Draws directly to hardware  
- Very low RAM usage  

## **Important Methods**
- `fill(color)` — clear the screen  
- `fill_rect(x, y, w, h, color)` — draw rectangles  
- `text(str, x, y, color)` — draw small text  
- `show()` — typically a no‑op (no framebuffer)

---

# **wifi_buttons.py — Phone Web UI**

## **Purpose**
Provides:
- A **Wi‑Fi access point**
- A **minimal HTTP server**
- A bridge converting **web button taps → events**

## **Public API (used by main.py)**
```python
wifi.set_choices(["Go left", "Go right"])
wifi.set_paging(page, pages)
wifi.set_screen_info(title, subtitle, can_back)
```

## **HTTP Endpoints**

| URL           | Meaning            | Event Returned |
|---------------|--------------------|----------------|
| `/`           | Show control UI    | None |
| `/c?i=N`      | Choice button      | `{type:"choice", index:N}` |
| `/page?dir=-1`| Previous page      | `{type:"page", dir:-1}` |
| `/page?dir=1` | Next page          | `{type:"page", dir:1}` |
| `/back`       | Back               | `{type:"back"}` |
| `/refresh`    | Restart            | `{type:"refresh"}` |

### **Key Idea**
The browser UI is **stateless**;  
all real state exists in **main.py**.

---

# **main.py — Application Logic**

## **Responsibilities**
- Configure hardware (SPI, LCD)
- Navigate story nodes
- Wrap and paginate text
- Render story to LCD
- Handle all web events

## **Core Components**

### **StoryEngine**
- Tracks current node  
- Maintains history for *Back*  
- Remembers last `map_` node  

### **Pager**
- Wraps text lines  
- Splits into pages  
- Tracks page index  

### **Renderer**
- Draws header, body, footer  
- Uses enlarged text for readability  

---

# **Event Loop (Core Logic)**

```python
while True:
    ev = wifi.poll()
    if ev:
        handle_event(ev)
        render(engine, pager)
        sync_web()
```

## **Event Handling**

| Event | Action |
|-------|---------|
| `choice` | Move to next node |
| `page` | Change page |
| `back` | Pop history |
| `refresh` | Reset story |

---

# **Text Rendering & Paging**

- Wraps text by **character count**, not pixels  
- Lines grouped into pages  
- Pager resets when node changes  

### This ensures:
- Large, readable text  
- Consistent paging between LCD and web UI  

---

# **Common Debug Tips**

- **Buttons unresponsive** → check `poll()` parsing  
- **Requires two taps** → browser refresh timing issue  
- **Prev/Next missing** → only one page  
- **Back missing** → history stack is empty  

---

# **One‑Sentence Summary**

> **“StoryPico is an event‑driven story engine where phone button presses become events that update a paged narrative on an ST7789 LCD.”**

---

# **Author Notes**

This project highlights:
- Event‑driven microcontroller design  
- Low‑RAM graphics rendering  
- Strong separation of content & logic  
- Lightweight, practical embedded web UI  

---