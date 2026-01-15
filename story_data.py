# story_data.py
STORIES = {
    "into the woods": {

        # =========================================================
        # START (quick access to Memory Rooms)
        # =========================================================
        "start": {
            "text": (
                "You arrive at the edge of a quiet field.\n"
                "grass sprouts from the ground like ribbons.\n\n"
                "Before you go further, you stop.\n"
                "What kind of day is it?\n\n"
                "Quick access:\n"
                "Hare’s Burrow has three Memory Rooms (Green/Amber/Red)."
            ),
            "choices": [
                ("Sunny day (steady/okay)", "map_sunny"),
                ("Cloudy day (low/heavy)", "map_cloudy"),
                ("Rainy day (sad/tearful)", "map_rainy"),
                ("Windy day (anxious/restless)", "map_windy"),
                ("Daily Check-In", "checkin_intro"),
                ("Quick Access: Memory Rooms (Hare’s Burrow)", "burrow_hare"),
            ],
        },

        # =========================================================
        # MAP HUBS (same world, different weather vibe)
        # =========================================================
        "map_sunny": {
            "text": (
                "MAP — SUNNY DAY\n\n"
                "Sunlight shines softly onto you.\n"
                "The sky is a deep blue. Existing isnt hard.\n\n"
                "Where do you go?"
            ),
            "choices": [
                ("North: Deer Path (panic tools)", "deer_intro"),
                ("East: River (Otter / soothing)", "otter_intro"),
                ("South: Hedge (Hedgehog / shutdown)", "hedgehog_intro"),
                ("West: Stones (Badger / boundaries)", "badger_intro"),
                ("Center: Big Tree (Rabbit, Hare, Robin, fox, owl)", "tree_hub"),
                ("Daily Check-In", "checkin_intro"),
                ("Memory Rooms (Hare’s Burrow)", "burrow_hare"),
                ("Change day/weather", "start"),
            ],
        },

        "map_cloudy": {
            "text": (
                "MAP — CLOUDY DAY\n\n"
                "its darker now.\n"
                "the slow drawl of time sits with you.\n\n"
                "Where do you go?"
            ),
            "choices": [
                ("North: Deer Path (panic tools)", "deer_intro"),
                ("East: River (Otter / soothing)", "otter_intro"),
                ("South: Hedge (Hedgehog / shutdown)", "hedgehog_intro"),
                ("West: Stones (Badger / boundaries)", "badger_intro"),
                ("Center: Big Tree (Rabbit, Hare, Robin, fox, owl)", "tree_hub"),
                ("Daily Check-In", "checkin_intro"),
                ("Memory Rooms (Hare’s Burrow)", "burrow_hare"),
                ("Change day/weather", "start"),
            ],
        },

        "map_rainy": {
            "text": (
                "MAP — RAINY DAY\n\n"
                "Rain sprinkles from the sky .\n"
                "The grass is cool, and you feel a pain in your chest.\n\n"
                "Where do you go?"
            ),
            "choices": [
                ("North: Deer Path (panic tools)", "deer_intro"),
                ("East: River (Otter / soothing)", "otter_intro"),
                ("South: Hedge (Hedgehog / shutdown)", "hedgehog_intro"),
                ("West: Stones (Badger / boundaries)", "badger_intro"),
                ("Center: Big Tree (Rabbit, Hare, Robin, fox, owl)", "tree_hub"),
                ("Daily Check-In", "checkin_intro"),
                ("Memory Rooms (Hare’s Burrow)", "burrow_hare"),
                ("Change day/weather", "start"),
            ],
        },

        "map_windy": {
            "text": (
                "MAP — WINDY DAY\n\n"
                "Wind whispers its cool breath.\n"
                "Your thoughts keep moving, not able to stop.\n\n"
                "Where do you go?"
            ),
            "choices": [
                ("North: Deer Path (panic tools)", "deer_intro"),
                ("East: River (Otter / soothing)", "otter_intro"),
                ("South: Hedge (Hedgehog / shutdown)", "hedgehog_intro"),
                ("West: Stones (Badger / boundaries)", "badger_intro"),
                ("Center: Big Tree (Rabbit, Hare, Robin, fox, owl)", "tree_hub"),
                ("Daily Check-In", "checkin_intro"),
                ("Memory Rooms (Hare’s Burrow)", "burrow_hare"),
                ("Change day/weather", "start"),
            ],
        },

        # =========================================================
        # CENTER HUB: THE BIG TREE (characters)
        # =========================================================
        "tree_hub": {
            "text": (
                "CENTER — THE BIG TREE\n\n"
                "Rabbit sits with calm attention.\n"
                "Hare looks like it’s halfway into tomorrow.\n"
                "A robin watches you with gentle care.\n\n"
                "a fox trail nearby.\n\n"
		    "an owl snoozes on a branch.\n\n"
                "Who do you go to?"
            ),
            "choices": [
                ("Rabbit (feelings + compassion)", "rabbit_intro"),
                ("Hare (overthinking + next step)", "hare_intro"),
                ("Robin (support)", "robin_intro"),
                ("Fox (inner critic)", "fox_intro"),
                ("Return to Map", "Return to Map"),
            ],
        },

        # =========================================================
        # HARE'S BURROW + MEMORY ROOMS (quick access)
        # =========================================================
        "burrow_hare": {
            "text": (
                "HARE’S BURROW\n\n"
                "You duck into a quiet burrow.\n"
                "The air is calm and still.\n\n"
                "Three doors stand in a row:\n"
                "GREEN • AMBER • RED\n\n"
                "Hare whispers:\n"
                "“These are Memory Rooms. Quick to reach when you need them.”"
            ),
            "choices": [
                ("Green Room (steady)", "memory_green"),
                ("Amber Room (early warning)", "memory_amber"),
                ("Red Room (urgent)", "memory_red"),
                ("Back to Start", "start"),
                ("Return to Map", "Return to Map"),
            ],
        },

        "memory_green": {
            "text": (
                "MEMORY ROOM — GREEN\n"
                "Signs you’re doing okay / staying steady.\n\n"
                "GREEN SIGNS (examples):\n"
                "- Sleeping roughly as normal\n"
                "- Eating/drinking enough\n"
                "- Able to focus sometimes\n"
                "- Stress feels manageable\n"
                "- You can reality-check worries\n\n"
                "KEEP IT STEADY (small actions):\n"
                "- Keep a routine (sleep/wake)\n"
                "- Eat something simple + drink water\n"
                "- Take breaks from scrolling\n"
                "- Gentle movement (stretch/walk)\n"
                "- Stay connected to 1 person\n\n"
                "If you notice things shifting, step into AMBER early."
            ),
            "choices": [
                ("Go to Amber Room", "memory_amber"),
                ("Back to Burrow", "burrow_hare"),
                ("Return to Map", "Return to Map"),
            ],
        },

        "memory_amber": {
            "text": (
                "MEMORY ROOM — AMBER\n"
                "Early warning signs (slow down + get support).\n\n"
                "AMBER SIGNS (examples):\n"
                "- Sleep changing (less, broken, very restless)\n"
                "- Feeling unusually anxious, wired, overwhelmed\n"
                "- Finding meanings/patterns everywhere (more than usual)\n"
                "- Feeling suspicious or on-guard\n"
                "- Hearing/seeing things at the edge of perception\n"
                "- Thoughts racing or hard to organise\n"
                "- Withdrawing from people / feeling disconnected\n\n"
                "AMBER PLAN (do these now):\n"
                "1) Reduce stress + stimulation (quiet room, dim lights)\n"
                "2) Prioritise sleep (wind-down, no caffeine late)\n"
                "3) Eat + drink something\n"
                "4) Talk to someone you trust today\n"
                "5) Contact your GP / mental health team if you have one\n\n"
                "If you feel unsafe or things escalate, step into RED."
            ),
            "choices": [
                ("Go to Red Room", "memory_red"),
                ("Back to Green Room", "memory_green"),
                ("Back to Burrow", "burrow_hare"),
                ("Return to Map", "Return to Map"),
            ],
        },

        "memory_red": {
            "text": (
                "MEMORY ROOM — RED\n"
                "Urgent signs (get help now).\n\n"
                "RED SIGNS (examples):\n"
                "- Feeling out of control or unable to keep yourself safe\n"
                "- Strong beliefs others say aren’t real, and you can’t reality-check\n"
                "- Hearing/seeing things that feel very real and distressing\n"
                "- Severe agitation or fear\n"
                "- Not sleeping for a long time + symptoms intensifying\n\n"
                "DO THIS NOW:\n"
                "1) Don’t stay alone if possible — contact someone you trust\n"
                "2) If you have a crisis line / mental health team, call them\n"
                "3) If there’s immediate danger, call emergency services\n\n"
                "UK QUICK INFO:\n"
                "- Immediate danger: call 999\n"
                "- Urgent but not life-threatening: NHS 111\n\n"
                "You deserve support. This is a ‘get help’ moment."
            ),
            "choices": [
                ("Back to Amber Room", "memory_amber"),
                ("Back to Burrow", "burrow_hare"),
                ("Back to Start", "start"),
            ],
        },

        # =========================================================
        # DAILY CHECK-IN
        # =========================================================
        "checkin_intro": {
            "text": (
                "DAILY CHECK-IN\n\n"
                "No judgement. Just noticing.\n\n"
                "How is your mood right now?"
            ),
            "choices": [
                ("Good / okay", "checkin_mood_ok"),
                ("Low / heavy", "checkin_mood_low"),
                ("Anxious / on edge", "checkin_mood_anx"),
                ("Numb / disconnected", "checkin_mood_numb"),
            ],
        },

        "checkin_mood_ok": {
            "text": "Mood: good / okay.\n\nHow’s your energy?",
            "choices": [("High", "checkin_energy_high"), ("Medium", "checkin_energy_mid"), ("Low", "checkin_energy_low")],
        },
        "checkin_mood_low": {
            "text": "Mood: low / heavy.\n\nThat makes sense.\nHow’s your energy?",
            "choices": [("High", "checkin_energy_high"), ("Medium", "checkin_energy_mid"), ("Low", "checkin_energy_low")],
        },
        "checkin_mood_anx": {
            "text": "Mood: anxious / on edge.\n\nYour body is trying to protect you.\nHow’s your energy?",
            "choices": [("High", "checkin_energy_high"), ("Medium", "checkin_energy_mid"), ("Low", "checkin_energy_low")],
        },
        "checkin_mood_numb": {
            "text": "Mood: numb / disconnected.\n\nSometimes numb is coping.\nHow’s your energy?",
            "choices": [("High", "checkin_energy_high"), ("Medium", "checkin_energy_mid"), ("Low", "checkin_energy_low")],
        },

        "checkin_energy_high": {
            "text": "Energy: high.\n\nWhat do you need most?",
            "choices": [("Calm", "checkin_need_calm"), ("Focus", "checkin_need_focus"),
                        ("Connection", "checkin_need_connect"), ("Joy", "checkin_need_joy")],
        },
        "checkin_energy_mid": {
            "text": "Energy: medium.\n\nWhat do you need most?",
            "choices": [("Calm", "checkin_need_calm"), ("Focus", "checkin_need_focus"),
                        ("Connection", "checkin_need_connect"), ("Joy", "checkin_need_joy")],
        },
        "checkin_energy_low": {
            "text": "Energy: low.\n\nLet’s keep it gentle.\nWhat do you need most?",
            "choices": [("Rest", "checkin_need_rest"), ("Calm", "checkin_need_calm"),
                        ("Connection", "checkin_need_connect"), ("Tiny task", "checkin_need_tiny")],
        },

        "checkin_need_calm": {
            "text": (
                "Need: calm.\n\n"
                "Pick one:\n"
                "- Box breathing\n"
                "- 5–4–3–2–1 grounding\n"
                "- Panic tools (Deer)"
            ),
            "choices": [
                ("Box breathing", "breathing_box"),
                ("5–4–3–2–1 grounding", "grounding_54321"),
                ("Visit Deer (panic tools)", "deer_intro"),
                ("Return to Map", "Return to Map"),
            ],
        },

        "checkin_need_focus": {
            "text": (
                "Need: focus.\n\n"
                "Try: 2 minutes only.\n"
                "Pick ONE tiny step.\n"
                "Stop after 2 minutes if you want.\n\n"
                "Progress counts when it’s small."
            ),
            "choices": [
                ("Visit Hare (next step)", "hare_next_step"),
                ("Visit Badger (boundaries)", "badger_intro"),
                ("Return to Map", "Return to Map"),
            ],
        },

        "checkin_need_connect": {
            "text": (
                "Need: connection.\n\n"
                "Pick ONE:\n"
                "- Message someone\n"
                "- Sit near someone\n"
                "- Hold something soft\n\n"
                "Connection can be quiet."
            ),
            "choices": [
                ("Visit Robin (support)", "robin_intro"),
                ("Return to Map", "Return to Map"),
            ],
        },

        "checkin_need_joy": {
            "text": (
                "Need: joy.\n\n"
                "Tiny joy counts.\n"
                "- warm drink\n"
                "- favourite song\n"
                "- step into sunlight"
            ),
            "choices": [
                ("Visit Otter (joy)", "otter_intro"),
                ("Return to Map", "Return to Map"),
            ],
        },

        "checkin_need_rest": {
            "text": (
                "Need: rest.\n\n"
                "Permission slip:\n"
                "“Rest is allowed.”\n\n"
                "One gentle reset:\n"
                "- water\n"
                "- wash face\n"
                "- lie down 10 mins"
            ),
            "choices": [
                ("Visit Hedgehog (shutdown)", "hedgehog_intro"),
                ("Return to Map", "Return to Map"),
            ],
        },

        "checkin_need_tiny": {
            "text": (
                "Need: tiny task.\n\n"
                "Pick one micro-step:\n"
                "- open a window\n"
                "- put one thing away\n"
                "- stretch\n\n"
                "Small wins are real."
            ),
            "choices": [
                ("Visit Hare (next step)", "hare_next_step"),
                ("Return to Map", "Return to Map"),
            ],
        },

        # =========================================================
        # CHARACTERS
        # =========================================================

        # Rabbit = feelings + compassion
        "rabbit_intro": {
            "text": (
                "RABBIT\n\n"
                "“Feelings are like weather,” Rabbit says.\n"
                "“They change. They pass through.”\n\n"
                "What would help?"
            ),
            "choices": [
                ("Name the feeling", "rabbit_name"),
                ("Self-compassion sentence", "rabbit_compassion"),
                ("Grounding 5–4–3–2–1", "grounding_54321"),
                ("Return to Map", "Return to Map"),
            ],
        },

        "rabbit_name": {
            "text": (
                "Pick a word that fits even a little:\n"
                "sad • anxious • angry • tired • lonely • overwhelmed\n\n"
                "Now add:\n"
                "“...and that makes sense.”\n\n"
                "Naming it can soften it."
            ),
            "choices": [
                ("Self-compassion", "rabbit_compassion"),
                ("Return to Map", "Return to Map"),
            ],
        },

        "rabbit_compassion": {
            "text": (
                "Try one kind sentence:\n\n"
                "- “This is hard, and I’m doing my best.”\n"
                "- “One step at a time.”\n"
                "- “I can be imperfect and still worthy.”\n\n"
                "THE END (skill learned)."
            ),
            "choices": [
                ("Return to Map", "Return to Map"),
                ("Change day/weather", "start"),
            ],
        },

        # Hare = overthinking + next step
        "hare_intro": {
            "text": (
                "HARE\n\n"
                "“My brain runs ahead,” Hare admits.\n"
                "“It tries to protect me with worries.”\n\n"
                "Pick a tool:"
            ),
            "choices": [
                ("Thoughts aren’t facts", "hare_thoughts"),
                ("Pick one next step", "hare_next_step"),
                ("Box breathing", "breathing_box"),
                ("Memory Rooms (Burrow)", "burrow_hare"),
                ("Return to Map", "Return to Map"),
            ],
        },

        "hare_thoughts": {
            "text": (
                "Say:\n"
                "“I’m having lots of difficult thoughts.”\n\n"
                "It creates space.\n"
                "You can notice thoughts without obeying them.\n\n"
                "THE END (skill learned)."
            ),
            "choices": [
                ("Return to Map", "Return to Map"),
                ("Change day/weather", "start"),
            ],
        },

        "hare_next_step": {
            "text": (
                "Pick ONE small next step today.\n\n"
                "Not the whole mountain.\n"
                "Just one stone.\n\n"
                "THE END (skill learned)."
            ),
            "choices": [
                ("Return to Map", "Return to Map"),
                ("Change day/weather", "start"),
            ],
        },

        # Robin = mum energy support
        "robin_intro": {
            "text": (
                "ROBIN\n\n"
                "The robin feels like care you can trust.\n"
                "Like your mum noticing you’re not okay.\n\n"
                "“You don’t have to carry this alone.”"
            ),
            "choices": [
                ("Comfort words", "robin_comfort"),
                ("Make a small support plan", "robin_plan"),
                ("Return to Map", "Return to Map"),
            ],
        },

        "robin_comfort": {
            "text": (
                "Comfort words:\n\n"
                "- “I’m here.”\n"
                "- “You matter, even on messy days.”\n"
                "- “Rest is allowed.”\n\n"
                "THE END (comfort found)."
            ),
            "choices": [
                ("Return to Map", "Return to Map"),
                ("Change day/weather", "start"),
            ],
        },

        "robin_plan": {
            "text": (
                "Tiny support plan:\n\n"
                "1) One person/place\n"
                "2) One calming action\n"
                "3) One kind sentence\n\n"
                "THE END (plan made)."
            ),
            "choices": [
                ("Return to Map", "Return to Map"),
                ("Change day/weather", "start"),
            ],
        },

        # Badger = boundaries
        "badger_intro": {
            "text": (
                "WEST — BADGER\n\n"
                "Badger peeks from a burrow near stones.\n"
                "“Boundaries are doors,” it says.\n\n"
                "Pick one:"
            ),
            "choices": [
                ("Boundary sentences", "badger_sentences"),
                ("Guilt vs safety", "badger_guilt"),
                ("Return to Map", "Return to Map"),
            ],
        },

        "badger_sentences": {
            "text": (
                "Boundary sentences:\n\n"
                "- “I can’t do that today.”\n"
                "- “I need time to think.”\n"
                "- “No, thank you.”\n"
                "- “That doesn’t work for me.”\n\n"
                "THE END (skill learned)."
            ),
            "choices": [
                ("Return to Map", "Return to Map"),
                ("Change day/weather", "start"),
            ],
        },

        "badger_guilt": {
            "text": (
                "Badger says:\n\n"
                "“Guilt isn’t always proof you’re wrong.\n"
                "Sometimes it’s proof you’re changing patterns.”\n\n"
                "THE END (skill learned)."
            ),
            "choices": [
                ("Return to Map", "Return to Map"),
                ("Change day/weather", "start"),
            ],
        },

        # Deer = panic tools
        "deer_intro": {
            "text": (
                "NORTH — DEER\n\n"
                "Deer stands in tall grass.\n"
                "“Panic is an alarm,” it says.\n"
                "“Loud, not always accurate.”\n\n"
                "Pick a tool:"
            ),
            "choices": [
                ("Temperature reset", "deer_temp"),
                ("Ride the wave", "deer_wave"),
                ("Box breathing", "breathing_box"),
                ("Return to Map", "Return to Map"),
            ],
        },

        "deer_temp": {
            "text": (
                "Temperature reset:\n\n"
                "- splash cold water\n"
                "- hold something cool\n"
                "- step into fresh air\n\n"
                "THE END (tool learned)."
            ),
            "choices": [
                ("Return to Map", "Return to Map"),
                ("Change day/weather", "start"),
            ],
        },

        "deer_wave": {
            "text": (
                "Ride the wave:\n\n"
                "Panic rises, peaks, falls.\n"
                "Say: “This is a wave. I can float.”\n\n"
                "Anchor: feel feet on ground.\n\n"
                "THE END (tool learned)."
            ),
            "choices": [
                ("Return to Map", "Return to Map"),
                ("Change day/weather", "start"),
            ],
        },

        # Hedgehog = shutdown
        "hedgehog_intro": {
            "text": (
                "SOUTH — HEDGEHOG\n\n"
                "Hedgehog is curled in a shady hedge.\n"
                "“Shutdown happens when it’s too much,” it whispers.\n\n"
                "Pick one:"
            ),
            "choices": [
                ("Gentle restart steps", "hedgehog_restart"),
                ("Permission to go slow", "hedgehog_slow"),
                ("Return to Map", "Return to Map"),
            ],
        },

        "hedgehog_restart": {
            "text": (
                "Gentle restart:\n\n"
                "1) sip water\n"
                "2) change temperature (blanket / air)\n"
                "3) one tiny task (1 min)\n\n"
                "THE END (tool learned)."
            ),
            "choices": [
                ("Return to Map", "Return to Map"),
                ("Change day/weather", "start"),
            ],
        },

        "hedgehog_slow": {
            "text": (
                "Hedgehog says:\n\n"
                "“Slow is still moving.\n"
                "Small is still progress.\n"
                "Rest is still valid.”\n\n"
                "THE END (comfort found)."
            ),
            "choices": [
                ("Return to Map", "Return to Map"),
                ("Change day/weather", "start"),
            ],
        },

        # Otter = soothing / joy
        "otter_intro": {
            "text": (
                "EAST — OTTER\n\n"
                "Water glittering in sunlight.\n"
                "Otter floats on its back.\n\n"
                "“Joy isn’t a reward,” it says.\n"
                "“It’s fuel.”\n\n"
                "Pick one:"
            ),
            "choices": [
                ("Two-minute nice thing", "otter_nice"),
                ("Soothing senses", "otter_senses"),
                ("Return to Map", "Return to Map"),
            ],
        },

        "otter_nice": {
            "text": (
                "Two-minute kindness:\n\n"
                "- warm drink\n"
                "- favourite song\n"
                "- step into sunlight\n"
                "- stretch\n\n"
                "THE END (joy fuel)."
            ),
            "choices": [
                ("Return to Map", "Return to Map"),
                ("Change day/weather", "start"),
            ],
        },

        "otter_senses": {
            "text": (
                "Soothing senses:\n\n"
                "Choose one sense:\n"
                "- touch (soft fabric)\n"
                "- sound (gentle music)\n"
                "- smell (tea, soap)\n\n"
                "THE END (soothing found)."
            ),
            "choices": [
                ("Return to Map", "Return to Map"),
                ("Change day/weather", "start"),
            ],
        },

        # Fox = inner critic
        "fox_intro": {
            "text": (
                "FOX TRAIL\n\n"
                "Fox sits in a clearing with sharp eyes.\n"
                "“That inner critic tries to motivate with fear,” it says.\n\n"
                "Pick one:"
            ),
            "choices": [
                ("Name the critic voice", "fox_name"),
                ("Rewrite the thought kindly", "fox_rewrite"),
                ("Return to Map", "Return to Map"),
            ],
        },

        "fox_name": {
            "text": (
                "Give the critic a nickname.\n"
                "When it appears, say:\n"
                "“Oh, it’s YOU again.”\n\n"
                "Distance helps.\n\n"
                "THE END (tool learned)."
            ),
            "choices": [
                ("Return to Map", "Return to Map"),
                ("Change day/weather", "start"),
            ],
        },

        "fox_rewrite": {
            "text": (
                "Kind rewrite:\n\n"
                "Critic: “I’m failing.”\n"
                "Rewrite: “I’m struggling and learning.”\n\n"
                "Critic: “I can’t cope.”\n"
                "Rewrite: “I can cope in small chunks.”\n\n"
                "THE END (tool learned)."
            ),
            "choices": [
                ("Return to Map", "Return to Map"),
                ("Change day/weather", "start"),
            ],
        },

        # =========================================================
        # SHARED SKILLS
        # =========================================================
        "grounding_54321": {
            "text": (
                "Grounding: 5–4–3–2–1\n\n"
                "Name:\n"
                "5 things you can see\n"
                "4 things you can feel\n"
                "3 things you can hear\n"
                "2 things you can smell\n"
                "1 thing you can taste\n\n"
                "THE END (skill learned)."
            ),
            "choices": [
                ("Return to Map", "Return to Map"),
                ("Change day/weather", "start"),
            ],
        },

        "breathing_box": {
            "text": (
                "Box breathing (4–4–4–4)\n\n"
                "In 4\n"
                "Hold 4\n"
                "Out 4\n"
                "Hold 4\n\n"
                "Repeat 3–5 rounds.\n\n"
                "THE END (skill learned)."
            ),
            "choices": [
                ("Return to Map", "Return to Map"),
                ("Change day/weather", "start"),
            ],
        },
    }
}
