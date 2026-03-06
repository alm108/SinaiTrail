#!/usr/bin/env python3
"""
SINAI TRAIL v7 — Desert visuals + mechanics.
Run: python3 sinai_trail.py
"""

import random, copy, sys, os, time, re

# ═══════════════════════════════════════════════════════════════════════════════
# ANSI COLORS (no dependencies, works in any modern terminal)
# ═══════════════════════════════════════════════════════════════════════════════

class C:
    RESET   = "\033[0m"
    BOLD    = "\033[1m"
    DIM     = "\033[2m"
    GREEN   = "\033[32m"
    RED     = "\033[31m"
    YELLOW  = "\033[33m"
    CYAN    = "\033[36m"
    WHITE   = "\033[37m"
    BGREEN  = "\033[1;32m"  # bold green
    BRED    = "\033[1;31m"  # bold red
    BYELLOW = "\033[1;33m"  # bold yellow
    BCYAN   = "\033[1;36m"  # bold cyan
    BWHITE  = "\033[1;37m"  # bold white
    MAGENTA = "\033[35m"
    BMAGENTA = "\033[1;35m"
    DYELLOW = "\033[33m"


# ═══════════════════════════════════════════════════════════════════════════════
# BACKGROUND VISUALS
# ═══════════════════════════════════════════════════════════════════════════════

def _vpad(s, color, w):
    vlen = len(s)
    if vlen < w:
        s = s + " " * (w - vlen)
    return f"{color}{s[:w]}{C.RESET}"

def _strip_ansi(s):
    return re.sub(r'\033\[[^m]*m', '', s)

_NL = 20
_WL = 32

# Title screen frames (exact from approved cactus_test)
_FRAME_L = [
    f"{C.DYELLOW}    .        +      {C.RESET}",
    f"{C.DYELLOW}         .          {C.RESET}",
    f"{C.DYELLOW}  +    .       '    {C.RESET}",
    f"{C.DYELLOW}     '     .      + {C.RESET}",
    f"{C.DYELLOW} .            '     {C.RESET}",
    f"{C.DYELLOW}       .   +        {C.RESET}",
    f"{C.DYELLOW}  '          .      {C.RESET}",
    f"{C.DYELLOW}      +          '  {C.RESET}",
    f"{C.MAGENTA}              /\\    {C.RESET}",
    f"{C.MAGENTA}             /  \\   {C.RESET}",
    f"{C.MAGENTA}        /\\  / .  \\  {C.RESET}",
    f"{C.BMAGENTA}       /  \\/    . \\ {C.RESET}",
    f"{C.BMAGENTA}  /\\  / .    '    \\ {C.RESET}",
]

_FRAME_R = [
    f"{C.DYELLOW}         .       '  {C.RESET}",
    f"{C.BYELLOW}              (    {C.RESET}",
    f"{C.BYELLOW}               )   {C.RESET}",
    f"{C.DYELLOW}  '       .        {C.RESET}",
    f"{C.DYELLOW}      +         .  {C.RESET}",
    f"{C.DYELLOW}  .        '       {C.RESET}",
    f"{C.DYELLOW}        .       +  {C.RESET}",
    f"{C.DYELLOW}   '         .     {C.RESET}",
    f"{C.MAGENTA}      /\\           {C.RESET}",
    f"{C.MAGENTA}     /  \\    /\\    {C.RESET}",
    f"{C.MAGENTA}    / .  \\  /  \\   {C.RESET}",
    f"{C.BMAGENTA}   /    . \\/  . \\  {C.RESET}",
    f"{C.BMAGENTA}  / '    .   '   \\ {C.RESET}",
]

_CACTUS_L = [
    "            ", "     /|\\    ", "    |||||   ", "    |||||   ",
    "/\\  |||||   ", "||| |||||   ", "||| |||||   ", " \\|`'||||   ",
    "  \\_-||||   ", "    ||||`-' ", "    |||| __ ", "    |||||   ",
    "    |||||   ",
]

_CACTUS_R = [
    "            ", "    /||\\    ", "    ||||    ", "    ||||    ",
    "    |||| /|\\", "    |||| |||", "    |||| |||", "    |||| ע||",
    "    |||||||/", "    ||||~~' ", "    ||||    ", "    ||||    ",
    "    ||||    ",
]

_GRASS_NARROW = [
    f"{C.BGREEN}~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~{C.RESET}",
    f"{C.GREEN} \\/..__..--  .    \\/..__..--  .   _.      \\/  ..__..--  .    \\/..__..--  .  \\/  ..__..--  .  \\/{C.RESET}",
    f"{C.BGREEN}.__.  \\/  ._.--_.  \\/ .-..\\/  ..- _.  \\/ .__.  \\/  ._.--_.  \\/ .-..\\/  ..- _.  \\/ .-..\\/  .._. {C.RESET}",
    f"{C.GREEN}.   \\/    _..\\/-     ...--..       \\/  ._. .  \\/ _..\\/-     ...--..     \\/  ._.  ...--..    \\/   {C.RESET}",
]

_GRASS_W = 66
_GRASS_WIDE = [
    f"{C.BGREEN}{'~' * 66}{C.RESET}",
    f"{C.GREEN} \\/..__..--  .    \\/..__..--  .   _.      \\/  ..__..--  .    \\/ . {C.RESET}",
    f"{C.BGREEN}.__.  \\/  ._.--_.  \\/ .-..\\/  ..- _.  \\/ .__.  \\/  ._.--_.  \\/ .__{C.RESET}",
    f"{C.GREEN}.   \\/    _..\\/-     ...--..       \\/  ._. .  \\/ _..\\/-     ..--. {C.RESET}",
]

# Intro-width grass (106 chars to match 108-char intro content with 2-space indent)
_GRASS_INTRO = [
    f"{C.BGREEN}{'~' * 106}{C.RESET}",
    f"{C.GREEN} \\/..__..--  .    \\/..__..--  .   _.      \\/  ..__..--  .    \\/..__..--  .  \\/  ..__..--  .  \\/ .  \\/ .__.{C.RESET}",
    f"{C.BGREEN}.__.  \\/  ._.--_.  \\/ .-..\\/  ..- _.  \\/ .__.  \\/  ._.--_.  \\/ .-..\\/  ..- _.  \\/ .-..\\/  .._. \\/ ..__..--{C.RESET}",
    f"{C.GREEN}.   \\/    _..\\/-     ...--..       \\/  ._. .  \\/ _..\\/-     ...--..     \\/  ._.  ...--..    \\/   ._.  \\/ .{C.RESET}",
]

_MTN_L_WIDE = [
    _vpad("                      /\\       ", C.MAGENTA, _WL),
    _vpad("              /\\     /  \\  /\\  ", C.MAGENTA, _WL),
    _vpad("        /\\   /  \\   /    \\/  \\ ", C.MAGENTA, _WL),
    _vpad("       /  \\ /    \\ /          \\", C.BMAGENTA, _WL),
    _vpad("  /\\  /    \\/      \\           ", C.BMAGENTA, _WL),
]

_MTN_R_WIDE = [
    _vpad("       /\\            /\\   /  \\ ", C.MAGENTA, _WL),
    _vpad("      /  \\    /\\    /  \\ /     ", C.MAGENTA, _WL),
    _vpad("  /\\ /    \\  /  \\  /    \\/     ", C.MAGENTA, _WL),
    _vpad(" /  \\/      \\/    \\/           ", C.BMAGENTA, _WL),
    _vpad("/                              ", C.BMAGENTA, _WL),
]

_STAR_PATTERNS = [
    "  '     .      +    ", "     +       .      ",
    "  .      '     +    ", "       .      '     ",
    "    +      .        ", "  .    '       +    ",
    "      .     '    .  ", "   +       .     '  ",
    "  .     +      .    ", "     '      +    .  ",
    "  +      .     '    ", "     .      +    '  ",
    "  '     .      +    ", "     +       .    ' ",
    "  .      '     +    ", "       .      '     ",
]

def _stars_wide(idx):
    p1 = _STAR_PATTERNS[idx % len(_STAR_PATTERNS)]
    p2 = _STAR_PATTERNS[(idx + 7) % len(_STAR_PATTERNS)]
    s = (p1 + p2)[:_WL]
    while len(s) < _WL:
        s += " "
    return _vpad(s, C.DYELLOW, _WL)


def render_title(text_lines):
    """Render title screen using EXACT cactus_test format."""
    mid_w = 30
    rows = 13
    for i in range(rows):
        left_bg  = _FRAME_L[i]
        right_bg = _FRAME_R[i]
        left_c   = _CACTUS_L[i]
        right_c  = _CACTUS_R[i]
        if i < len(text_lines) and text_lines[i].strip():
            txt = text_lines[i]
            clean = _strip_ansi(txt)
            pad = mid_w - len(clean)
            lpad = pad // 2
            mid = " " * lpad + txt + " " * (pad - lpad)
        else:
            mid = " " * mid_w
        print(f"{left_bg}{C.GREEN}{left_c}{C.RESET}{C.BCYAN}|{C.RESET}{mid}{C.BCYAN}|{C.RESET}{C.GREEN}{right_c}{C.RESET}{right_bg}")
    for line in _GRASS_NARROW:
        print(f"  {line}")


def render_intro(text_lines, use_sun=False):
    """Render intro/bookend screen. Wide frames, mountains anchored to bottom."""
    rows = max(13, len(text_lines))
    mtn_rows = 5
    star_rows = rows - mtn_rows
    mid_w = 42
    for i in range(rows):
        if i < star_rows:
            left_bg = _stars_wide(i)
            right_bg = _stars_wide(i + 3)
            if not use_sun:
                if i == 0:
                    right_bg = _vpad("    .        '     .        '  ", C.DYELLOW, _WL)
                elif i == 1:
                    right_bg = _vpad("                        (      ", C.BYELLOW, _WL)
                elif i == 2:
                    right_bg = _vpad("                         )     ", C.BYELLOW, _WL)
            else:
                if i == 1:
                    right_bg = _vpad("                \\   |   /      ", C.BYELLOW, _WL)
                elif i == 2:
                    right_bg = _vpad("                  .-'-.        ", C.BYELLOW, _WL)
                elif i == 3:
                    right_bg = _vpad("               -~'   '~-      ", C.BYELLOW, _WL)
                elif i == 4:
                    right_bg = _vpad("                  `-.-'        ", C.BYELLOW, _WL)
                elif i == 5:
                    right_bg = _vpad("                /   |   \\      ", C.BYELLOW, _WL)
        else:
            mi = i - star_rows
            left_bg = _MTN_L_WIDE[mi] if mi < len(_MTN_L_WIDE) else _stars_wide(i)
            right_bg = _MTN_R_WIDE[mi] if mi < len(_MTN_R_WIDE) else _stars_wide(i + 3)
        if i < len(text_lines) and text_lines[i].strip():
            txt = text_lines[i]
            clean = _strip_ansi(txt)
            pad = mid_w - len(clean)
            if pad > 0:
                lpad = pad // 2
                mid = " " * lpad + txt + " " * (pad - lpad)
            else:
                mid = txt
        else:
            mid = " " * mid_w
        print(f"{left_bg}{C.BCYAN}|{C.RESET}{mid}{C.BCYAN}|{C.RESET}{right_bg}")
    for line in _GRASS_INTRO:
        print(f"  {line}")

def draw_sky_header(use_sun=False):
    """Compact sky header for gameplay screens."""
    if use_sun:
        lines = [
            f"{C.DYELLOW}    .     +     .  '    {C.BYELLOW}\\   |   /{C.DYELLOW}     .     '    +   .{C.RESET}",
            f"{C.DYELLOW}         .        '       {C.BYELLOW}.-'-.{C.DYELLOW}         .         '    .{C.RESET}",
            f"{C.DYELLOW}  +    .     '     .   {C.BYELLOW}-~'   '~-{C.DYELLOW}    '     .    +      '{C.RESET}",
            f"{C.DYELLOW}     '     .    +        {C.BYELLOW}`-.-'{C.DYELLOW}      +      .     '     .{C.RESET}",
            f"{C.MAGENTA}        /\\      /\\    {C.BYELLOW}/   |   \\{C.MAGENTA}      /\\      /\\        {C.RESET}",
            f"{C.BMAGENTA}   /\\  /  \\    /  \\  /\\            /\\  /  \\    /  \\  /\\    {C.RESET}",
            f"{C.BMAGENTA}  /  \\/    \\  /    \\/  \\          /  \\/    \\  /    \\/  \\   {C.RESET}",
        ]
    else:
        lines = [
            f"{C.DYELLOW}    .     +     .  '         .     '      .    +   .   {C.BYELLOW}({C.RESET}",
            f"{C.DYELLOW}         .        '     .         +    .        '      {C.BYELLOW}){C.RESET}",
            f"{C.DYELLOW}  +    .     '     .       '     .    +      '    .      '  {C.RESET}",
            f"{C.MAGENTA}        /\\      /\\               /\\      /\\        {C.RESET}",
            f"{C.BMAGENTA}   /\\  /  \\    /  \\  /\\      /\\  /  \\    /  \\  /\\    {C.RESET}",
            f"{C.BMAGENTA}  /  \\/    \\  /    \\/  \\    /  \\/    \\  /    \\/  \\   {C.RESET}",
        ]
    for line in lines:
        print(f"  {line}")


def color_msg(msg):
    """Colorize stat changes: green for gains, red for losses."""
    parts = msg.split("  ")
    colored = []
    for part in parts:
        part = part.strip()
        if not part:
            continue
        if part.startswith("+"):
            colored.append(f"{C.BGREEN}{part}{C.RESET}")
        elif part.startswith("-"):
            colored.append(f"{C.BRED}{part}{C.RESET}")
        elif "strays" in part:
            colored.append(f"{C.BRED}{part}{C.RESET}")
        elif "returns" in part:
            colored.append(f"{C.BGREEN}{part}{C.RESET}")
        elif "presence returns" in part.lower():
            colored.append(f"{C.BCYAN}{part}{C.RESET}")
        elif "halved" in part.lower():
            colored.append(f"{C.BYELLOW}{part}{C.RESET}")
        else:
            colored.append(part)
    return "  ".join(colored)


def show_result_box(chosen_text, msg, state, symbol="►"):
    """Show a consistent result box with colored stats."""
    clear()
    show_status(state)
    print()
    box_top()
    box_print(f"{C.BCYAN}{symbol} {chosen_text}{C.RESET}")
    box_mid()
    box_empty()
    colored = color_msg(msg) if msg else f"{C.DIM}(no effect){C.RESET}"
    box_print(f"{colored}")
    box_empty()
    box_bot()
    input(f"\n  {C.DIM}[Enter/Return | ^C = Quit]:{C.RESET} ")

# ═══════════════════════════════════════════════════════════════════════════════
# CHARACTERS
# ═══════════════════════════════════════════════════════════════════════════════

CHARACTERS = {
    "1": {
        "name": "MOSHE",
        "desc": (
            "On a mountain in a meeting with G_d.\n"
            "\n"
            "[Character coming soon.\n"
            " Don't leave a message at the beep.]"
        ),
        "disabled": True,
    },
    "2": {
        "name": "MIRYAM",
        "desc": (
            "She watched the sea split.\n"
            "She watched the army drown.\n"
            "She reached into her bag.\n"
            "She had been waiting her whole life\n"
            "to reach into that bag.\n"
            "\n"
            "Opponent: Forgetting. 2 million people.\n"
            "          One tambourine."
        ),
        "nerve": 75, "manna": 80, "water": 85,
        "camp": 90, "signal": 60, "gold": 50,
        "special": "TAMBOURINE TIME",
        "special_desc": "Start the song. +30 camp. Restore 2 who strayed.",
        "campaign": "camp",
    },
    "3": {
        "name": "AARON",
        "desc": (
            "The calf is not a god.\n"
            "It is a temporary transitional\n"
            "spiritual placeholder pending\n"
            "Moses's return.\n"
            "It's in beta.\n"
            "\n"
            "Opponent: The crowd. They gave the gold\n"
            "          before he finished the sentence."
        ),
        "nerve": 60, "manna": 90, "water": 90,
        "camp": 75, "signal": 50, "gold": 70,
        "special": "DELAY",
        "special_desc": "Stall the crowd. Subtract 3 days from the clock. Add detail to the left ear.",
        "campaign": "camp",
    },
}

# ═══════════════════════════════════════════════════════════════════════════════
# CAMP MEMBERS
# ═══════════════════════════════════════════════════════════════════════════════

CAMP_MEMBERS = {
    "Datan":     {"personality": "Professional skeptic. Egypt > Desert. Open to opportunities not involving manna.",
                  "loyalty": 30},
    "Aviram":    {"personality": "Agrees with Datan. Always agrees with Datan. Has never had an original opinion. This is documented.",
                  "loyalty": 35},
    "Nachshon":  {"personality": "Walked into the sea before it split. Will walk into anything before it splits. Nobody asks Nachshon to do things. Nachshon does them.",
                  "loyalty": 95},
    "Betzalel":  {"personality": "Can build anything. Has built everything. Currently waiting for someone to tell him what to build next. He already knows what it is.",
                  "loyalty": 85},
    "Calev":     {"personality": "Saw the same land everyone else saw. Reached a different conclusion. Will not stop reaching different conclusions.",
                  "loyalty": 90},
    "Yehoshua":  {"personality": "Moses's student. Does not leave the tent. When he does leave the tent, things get done.",
                  "loyalty": 92},
    "Eldad":     {"personality": "Prophesies in the camp without permission. The prophecy was apparently very good.",
                  "loyalty": 70},
    "Medad":     {"personality": "Also prophesies without permission. Always with Eldad. They are a package deal.",
                  "loyalty": 70},
    "Serach":    {"personality": "Remembers things nobody else remembers. Has been remembering things for a very long time.",
                  "loyalty": 80},
    "Devorah":   {"personality": "Judges things. Mostly situations. Occasionally people. Always correctly.",
                  "loyalty": 82},
    "Pinchas":   {"personality": "Zealous. About everything. If Pinchas makes tea he is zealous about the tea.",
                  "loyalty": 75},
    "Dotan":     {"personality": "Not to be confused with Datan. Dotan is fine. Datan has filed a complaint about the confusion.",
                  "loyalty": 65},
    "Yocheved":  {"personality": "Put a baby in a basket in a river and it worked out. Has trusted the process longer than anyone.",
                  "loyalty": 88},
    "Tziporah":  {"personality": "Married Moses. Understands what it means to wait for Moses. Has opinions about the mountain.",
                  "loyalty": 78},
    "Aholiav":   {"personality": "Betzalel's partner. Less famous. Equally skilled. Does not mind. This is suspicious.",
                  "loyalty": 80},
}

CAMP_NAMES = list(CAMP_MEMBERS.keys())

# ═══════════════════════════════════════════════════════════════════════════════
# CAMP CHECK-IN DIALOGUE (based on camp mood)
# ═══════════════════════════════════════════════════════════════════════════════

def get_checkin(name, state):
    """Return a character's check-in line based on current state."""
    strayed = name in state["strayed"]
    if strayed:
        return f"{name} is at the calf. They are not available for comment."

    mood = "good" if state["nerve"] > 50 else "shaky" if state["nerve"] > 25 else "bad"
    calf = state["calf_happened"]

    lines = {
        "Datan": {
            ("good", False): "Datan has no complaints today. This is itself cause for concern.",
            ("shaky", False): "Datan is drafting a formal letter. He will not say to whom.",
            ("bad", False): "Datan says he knew this would happen. He is currently accepting applications for a return trip to Egypt.",
            ("good", True): "Datan is quiet. Nobody knows what to do with a quiet Datan.",
            ("shaky", True): "Datan says the calf had better customer service.",
            ("bad", True): "Datan has filed a complaint about the calf, the mountain, the desert, the manna, and the concept of hope.",
        },
        "Aviram": {
            ("good", False): "Aviram agrees that things are fine. He checked with Datan first.",
            ("shaky", False): "Aviram is worried. He is waiting for Datan to tell him how worried.",
            ("bad", False): "Aviram agrees with Datan that Egypt was better. Aviram has agreed with Datan about everything since Egypt.",
            ("good", True): "Aviram is cautiously optimistic. Datan has not approved this yet.",
            ("shaky", True): "Aviram is standing near the calf but not touching it. He calls this 'keeping his options open.'",
            ("bad", True): "Aviram went to the calf. He says it was Datan's idea. It was Datan's idea.",
        },
        "Nachshon": {
            ("good", False): "Nachshon is ready. For what, he will not say. He is always ready.",
            ("shaky", False): "Nachshon is pacing. He wants to walk toward something. There is nothing to walk toward yet.",
            ("bad", False): "Nachshon is walking toward the mountain. Nobody asked Nachshon to do this.",
            ("good", True): "Nachshon is already walking toward whoever strayed. He has a speech prepared. It is three words long.",
            ("shaky", True): "Nachshon says he will go get Moses himself. This is not how mountains work. Nachshon does not care how mountains work.",
            ("bad", True): "Nachshon is standing between the camp and the calf. He has not moved in six hours.",
        },
        "Betzalel": {
            ("good", False): "Betzalel is organizing materials. He will not say what for. He knows.",
            ("shaky", False): "Betzalel is looking at the gold. He has plans for the gold. They are not calf-shaped.",
            ("bad", False): "Betzalel says: the gold is being wasted. He will not elaborate.",
            ("good", True): "Betzalel is already building. He started before anyone asked. The blueprints are from somewhere else.",
            ("shaky", True): "Betzalel says: I need the gold back. He means the calf gold.",
            ("bad", True): "Betzalel is sitting with his tools out. Waiting. He has always been waiting.",
        },
        "Calev": {
            ("good", False): "Calev says the land is good. He has been saying this. He will continue saying this.",
            ("shaky", False): "Calev says: I saw what everyone saw. I just didn't stop looking.",
            ("bad", False): "Calev is the only one still talking about the future. This is either faith or stubbornness. Calev does not see the difference.",
            ("good", True): "Calev and Yehoshua are still here. They were always going to still be here.",
            ("shaky", True): "Calev says: the calf is not the end. He has been right before.",
            ("bad", True): "Calev tore his clothes. He is not speaking. When Calev stops speaking, pay attention.",
        },
        "Yehoshua": {
            ("good", False): "Yehoshua has not left the tent. Reports from inside the tent are encouraging.",
            ("shaky", False): "Yehoshua says: Moses said 40 days. It has not been 40 days.",
            ("bad", False): "Yehoshua is counting days on his fingers. He is very precise about the counting.",
            ("good", True): "Yehoshua is organizing people. Quietly. Effectively. He learned this from someone.",
            ("shaky", True): "Yehoshua says he can hear Moses on the mountain. Nobody believes him. He is correct.",
            ("bad", True): "Yehoshua will not leave the tent of meeting. Someone has to stay.",
        },
    }

    default_lines = {
        ("good", False): f"{name} is doing fine. Gathering manna. Keeping steady.",
        ("shaky", False): f"{name} is nervous but present. Still gathering. Still here.",
        ("bad", False): f"{name} is looking toward Egypt. Not walking yet. Looking.",
        ("good", True): f"{name} came back to camp after the calf. Quiet but here.",
        ("shaky", True): f"{name} is sitting alone. Not at the calf. Not quite in camp either.",
        ("bad", True): f"{name} hasn't spoken in days.",
    }

    char_lines = lines.get(name, default_lines)
    return char_lines.get((mood, calf), f"{name} is here.")


# ═══════════════════════════════════════════════════════════════════════════════
# EVENTS — ACT I
# ═══════════════════════════════════════════════════════════════════════════════

EVENTS_ACT1 = [
    {
        "title": "NO WATER",
        "ref": "Exodus 17:1",
        "text": "There is no water to drink.\nThe camp is thirsty. Someone says it is your fault.\nDatan has filed a formal complaint. It is not his first.",
        "choices": [
            ("Strike the rock. Trust the water will come.",
             {"nerve": +5, "water": +30, "signal": +5}),
            ("Tell them to wait. You are working on it.",
             {"nerve": -5, "water": +10, "stray": 1}),
            ("Ask Datan: where was your faith when the sea split?",
             {"nerve": +10, "camp": -5}),
        ],
    },
    {
        "title": "THE CUCUMBERS OF EGYPT",
        "ref": "Numbers 11:4-6",
        "text": "We remember the fish. The cucumbers. The melons.\nWe remember them as free. They were not free.\nWe were slaves. But the cucumbers were excellent.",
        "choices": [
            ("Manna is enough. The miracle is the point.",
             {"nerve": +10, "camp": +5}),
            ("Give them quail. Give them what they want.",
             {"nerve": -10, "manna": +20, "stray": 1}),
            ("Ask: were the cucumbers worth the bricks?",
             {"nerve": +5, "signal": +5, "camp": -3}),
        ],
    },
    {
        "title": "MOSES IS LATE",
        "ref": "Exodus 32:1",
        "text": "Moses is taking too long.\nThe crowd is gathering. Aaron looks nervous.\nThe gold is starting to move. This is fine.",
        "choices": [
            ("Hold. He said 40 days. Count the days.",
             {"nerve": +10, "camp": +5, "stray": -1}),
            ("Make a small compromise. Keep the peace.",
             {"nerve": -20, "stray": 2, "camp": -10}),
            ("Find who is still holding. Gather them now.",
             {"nerve": +15, "camp": +10, "stray": -1}),
        ],
        "critical": True,
    },
    {
        "title": "EGYPT NOSTALGIA",
        "ref": "Exodus 14:12",
        "text": "It was better for us to serve Egypt\nthan to die in this desert.\nAviram agrees. Aviram always agrees.",
        "choices": [
            ("The sea split for you. You were there.",
             {"nerve": +10, "camp": +5}),
            ("Agree partially. Redirect the energy.",
             {"nerve": -5, "stray": 1}),
            ("Ask Aviram: is that your opinion or Datan's?",
             {"nerve": +5, "camp": +3}),
        ],
    },
    {
        "title": "THE HALF-SHEKEL",
        "ref": "Exodus 30:15",
        "text": "Every person gives exactly half a shekel.\nNot more. Not less.\nThe wealthy are furious. This is correct.",
        "choices": [
            ("Give your half-shekel. Equal to everyone.",
             {"nerve": +20, "camp": +15, "signal": +10}),
            ("Give more. You want to stand out.",
             {"nerve": -10, "camp": -5, "stray": 1}),
            ("Tell the wealthy: you give the same as me.",
             {"nerve": +10, "camp": +20}),
        ],
    },
    {
        "title": "THE GOLD IS MOVING",
        "ref": "Exodus 32:2-3",
        "text": "Aaron asked for the gold to buy time.\nThe gold arrived before he finished the sentence.\nHe was going to add conditions. He did not get to the conditions.",
        "choices": [
            ("Do not give your earring.",
             {"nerve": +15, "camp": +5, "gold": -5, "stray": -1}),
            ("Give it. Just this once.",
             {"nerve": -20, "gold": -20, "stray": 2, "camp": -15}),
            ("Warn others quietly. Do not make a scene.",
             {"nerve": +5, "camp": +5, "gold": -10}),
        ],
        "critical": True,
    },
    {
        "title": "AMALEK ATTACKS",
        "ref": "Exodus 17:8",
        "text": "Amalek came from behind.\nThey attacked the stragglers at the rear.\nNachshon has opinions about this. He is sharing them at speed.",
        "choices": [
            ("Fight. Hold the line.",
             {"nerve": +5, "water": -10, "manna": -10, "camp": +10}),
            ("Hold the arms that are falling.",
             {"nerve": +15, "camp": +15, "stray": -1}),
            ("Protect the rear. That is where the vulnerable are.",
             {"nerve": +10, "camp": +10, "manna": -5}),
        ],
    },
    {
        "title": "KORACH SPEAKS",
        "ref": "Numbers 16:3",
        "text": "You take too much upon yourselves!\nThe whole congregation is holy!\nWhy do you raise yourself above us?\nKorach is not wrong about everything. This is worse than if he were.",
        "choices": [
            ("Do not engage. Let the ground decide.",
             {"nerve": +5, "camp": +5, "stray": -1}),
            ("Debate him. You can win this.",
             {"nerve": -10, "camp": -5, "stray": 1}),
            ("Acknowledge what is true. Reject the rest.",
             {"nerve": +15, "camp": +10}),
        ],
        "critical": True,
    },
    {
        "title": "MANNA FATIGUE",
        "ref": "Numbers 21:5",
        "text": "Manna again.\nThey are bored of miracles.\nThis will be discussed for centuries.",
        "choices": [
            ("Boredom with a miracle is also a miracle.",
             {"nerve": +15, "camp": +5, "stray": -1}),
            ("Look for something better tomorrow.",
             {"nerve": -5, "stray": 1}),
            ("Eat the manna. Say nothing. It tastes different to everyone.",
             {"manna": +10, "nerve": +5}),
        ],
    },
    {
        "title": "MIRIAM LOOKED AT 2 MILLION TRAUMATIZED FORMER SLAVES",
        "ref": "Exodus 15:20",
        "text": "The sea split. The army drowned.\nEveryone is in shock.\nMiriam has reached into her bag.\n\nAnd thought: tambourine time.",
        "choices": [
            ("Join the song. You know the words.",
             {"nerve": +20, "camp": +20, "signal": +10}),
            ("Watch. You are still processing the sea.",
             {"nerve": +5, "camp": +5}),
            ("Ask Miriam if this is the right moment.",
             None),
        ],
        "question": {
            "text": "Miriam looks at you. She says: is the army still behind us?",
            "choices": [
                ("No.", {"nerve": +15, "camp": +15}),
                ("No, they drowned.", {"nerve": +25, "camp": +25, "signal": +15}),
                ("...no.", {"nerve": +20, "camp": +20}),
            ],
        },
    },
    {
        "title": "THE SPIES RETURN",
        "ref": "Numbers 13:32",
        "text": "The land devours its inhabitants!\nWe were like grasshoppers in our own eyes!\nCalev is trying to say something. Nobody is listening to Calev.",
        "choices": [
            ("Calev is right. The land is good.",
             {"nerve": +15, "camp": +10, "stray": -1}),
            ("The spies saw what they saw.",
             {"nerve": -20, "camp": -15, "stray": 2}),
            ("Listen to Calev. Then listen to the ten. Then decide.",
             {"nerve": +5, "camp": +5, "signal": +5}),
        ],
        "critical": True,
    },
    {
        "title": "ELDAD AND MEDAD PROPHESY",
        "ref": "Numbers 11:26",
        "text": "Eldad and Medad stayed in the camp and prophesied.\nThey were not supposed to be in the camp.\nThe prophecy was apparently very good.",
        "choices": [
            ("Let them prophesy. The spirit goes where it goes.",
             {"nerve": +15, "camp": +10, "signal": +10}),
            ("Stop them. There is a process for this.",
             {"nerve": -10, "camp": -5}),
            ("Ask what they said.",
             None),
        ],
        "question": {
            "text": "Eldad looks at you. He says: do you want the short version or the long version?",
            "choices": [
                ("Short.", {"nerve": +10, "camp": +10}),
                ("Long.", {"nerve": +15, "signal": +15}),
                ("Are you supposed to be here?", {"nerve": +5, "camp": +5}),
            ],
        },
    },
    {
        "title": "NACHSHON HAS A PLAN",
        "ref": "Exodus 14:22",
        "text": "Nachshon is proposing something.\nIt involves going first before the conditions are right.\nThis has worked before. Once.",
        "choices": [
            ("Follow Nachshon. It worked before.",
             {"nerve": +20, "camp": +15, "stray": -1}),
            ("Wait for better conditions.",
             {"nerve": -5, "camp": -5}),
            ("Ask Nachshon why.",
             None),
        ],
        "question": {
            "text": "Nachshon says: if not now, when?",
            "choices": [
                ("When the conditions are better.", {"nerve": -5, "camp": -5}),
                ("...when indeed.", {"nerve": +20, "camp": +20}),
                ("That's not an answer.", {"nerve": +10, "camp": +5}),
            ],
        },
    },
    {
        "title": "BETZALEL NEEDS MATERIALS",
        "ref": "Exodus 35:30",
        "text": "Betzalel approaches. He has a list.\nThe list is very specific.\nHe knows exactly what is needed.\nHe always knows exactly what is needed.",
        "choices": [
            ("Give Betzalel the materials. He knows.",
             {"signal": +20, "camp": +10, "gold": -10}),
            ("Ask Betzalel to wait. Not now.",
             {"signal": -10, "camp": -5}),
            ("Ask Betzalel what he is building.",
             None),
        ],
        "question": {
            "text": "Betzalel says: the same thing I am always building. A place for the presence to rest.",
            "choices": [
                ("That's enough information.", {"signal": +15, "camp": +10}),
                ("How long will it take?", {"signal": +10}),
                ("Do you need help?", {"signal": +20, "camp": +15, "gold": -5}),
            ],
        },
    },
    {
        "title": "SHABBAT",
        "ref": "Exodus 16:27",
        "text": "The seventh day.\nSome people went to gather manna anyway.\nThey found nothing.\nThey are blaming you for the nothing.",
        "choices": [
            ("Set the boundary again. Clearly. Kindly.",
             {"nerve": +10, "camp": +5, "signal": +10}),
            ("Give them some of yours. Keep the peace.",
             {"nerve": -5, "manna": -20}),
            ("Let them be hungry. The Shabbat teaches.",
             {"nerve": +5, "camp": -5, "signal": +15}),
        ],
    },
    {
        "title": "WHOSE PEOPLE",
        "ref": "Exodus 32:7",
        "text": "God says to Moses: go down, for YOUR people have corrupted themselves.\nLater Moses will say to God: why does YOUR anger burn against YOUR people?\nNeither of them wants custody right now.\nThis is the most uncomfortable game of hot potato in history.",
        "choices": [
            ("They are everyone's people. Claim them.",
             {"nerve": +15, "camp": +15, "stray": -1}),
            ("They are God's people. Remind Him.",
             {"nerve": +20, "signal": +10}),
            ("They are their own people. That is the problem and the point.",
             {"nerve": +10, "camp": +10, "signal": +5}),
        ],
    },
]

# ═══════════════════════════════════════════════════════════════════════════════
# EVENTS — ACT II (every choice costs something)
# ═══════════════════════════════════════════════════════════════════════════════

EVENTS_ACT2 = [
    {
        "title": "THE TABLETS ARE BROKEN",
        "ref": "Exodus 32:19",
        "text": "They are in pieces at the foot of the mountain.\nThe calf is still standing.\nThe letters flew off the stone.\nSomeone will have to carve new ones. By hand this time.",
        "choices": [
            ("Mourn what was broken. Do not pretend it is fine.",
             {"nerve": +10, "repair": +10, "signal": +5, "manna": -10}),
            ("Gather the pieces. The broken tablets go in the Ark too.",
             {"nerve": +15, "repair": +15, "signal": +10, "water": -10, "camp": -5}),
            ("The breaking was honest. Hold that.",
             {"nerve": +8, "repair": +12, "camp": -8}),
        ],
        "critical": True,
    },
    {
        "title": "MOSHE INTERCEDES",
        "ref": "Exodus 32:32",
        "text": "If you will forgive their sin —\nbut if not, erase me from your book.\nMoses put himself between the people and the consequence.\nThis is mesirat nefesh. This is the whole game.",
        "choices": [
            ("Stand with him. Add your presence. You will not eat today.",
             {"nerve": +15, "repair": +15, "camp": +5, "manna": -15, "water": -10}),
            ("Go find those who strayed. Bring them back. It will cost you.",
             {"repair": +10, "restore": 2, "nerve": -5, "manna": -10}),
            ("Watch. You cannot match this. But you can witness it.",
             {"nerve": +8, "repair": +5, "signal": +10}),
        ],
    },
    {
        "title": "THE 13 ATTRIBUTES OF MERCY",
        "ref": "Exodus 34:6",
        "text": "Adonai, Adonai —\nCompassionate and gracious.\nSlow to anger.\nAbundant in kindness and truth.\nThe mountain is speaking.\nThis was revealed AFTER the lowest point. This was not a coincidence.",
        "choices": [
            ("Listen. All 13. Do not move. Do not eat. Do not leave.",
             {"nerve": +20, "repair": +20, "signal": +15, "manna": -15, "water": -10, "camp": -5}),
            ("Repeat them aloud so others can hear. The camp needs this more than you do.",
             {"repair": +15, "restore": 2, "camp": +10, "nerve": +5, "manna": -10}),
            ("Weep. You did not think you would hear this. You are not functional today.",
             {"nerve": +12, "repair": +12, "manna": -20}),
        ],
        "critical": True,
    },
    {
        "title": "THE CAMP MOURNS",
        "ref": "Exodus 33:4",
        "text": "No one put on their ornaments.\nThis is the first quiet the camp has had in weeks.\nEven Datan took off his ornaments.\nSomething is shifting.",
        "choices": [
            ("Go to them. No rebuke. Just presence. Skip gathering today.",
             {"repair": +10, "restore": 1, "camp": +10, "manna": -10}),
            ("Tell them what you heard on the mountain. It will take all day.",
             {"repair": +10, "signal": +10, "restore": 1, "water": -10}),
            ("Let them come on their own terms. Gather manna. Someone has to.",
             {"manna": +10, "repair": +5}),
        ],
    },
    {
        "title": "THE PRESENCE WITHDRAWS",
        "ref": "Exodus 33:3",
        "text": "I will not go in your midst.\nFor you are a stiff-necked people.\nLest I consume you on the way.\n\nAn angel will lead instead.\nWhen the people heard THIS, they mourned.\nNot the punishment. Not the death. This.\nThe leaving is worse than any consequence.",
        "choices": [
            ("Fast. Give up food and water. Show the mourning is real.",
             {"nerve": +10, "repair": +15, "manna": -25, "water": -20}),
            ("Remove your ornaments. Give the gold to Betzalel instead.",
             {"repair": +10, "gold": +15, "signal": +10, "camp": -5}),
            ("Sit at the edge of camp. You cannot be in the middle of this.",
             {"nerve": +5, "repair": +8, "camp": -10}),
        ],
        "critical": True,
    },
    {
        "title": "SHOW ME YOUR GLORY",
        "ref": "Exodus 33:18",
        "text": "Moses said: Please, show me your glory.\nGod said: I will make all my goodness pass before you.\nThis is not the same thing.\nMoses stood in the cleft of the rock.\nGod's hand covered him until it passed.\n\nYou cannot see the face. Only the after.",
        "choices": [
            ("Ask for the same thing. Show me. Risk everything.",
             {"nerve": +18, "repair": +15, "signal": +12, "water": -15, "manna": -10, "stray": 1}),
            ("Stand in the cleft. Wait. You will miss gathering today and tomorrow.",
             {"repair": +20, "signal": +15, "manna": -20, "water": -15}),
            ("You cannot ask. Just witness. Stay in camp and tend the fire.",
             {"nerve": +8, "camp": +10, "manna": +5}),
        ],
        "critical": True,
    },
    {
        "title": "MOSES CARVES THE STONE",
        "ref": "Exodus 34:1",
        "text": "Carve two stone tablets. Like the first ones.\nBring them up the mountain tomorrow morning.\nMoses is carving. This is new.\nThe first ones came pre-made. These require hands.",
        "choices": [
            ("Help gather the stone. The work is the prayer. You will not gather manna.",
             {"signal": +15, "repair": +10, "camp": +5, "manna": -15}),
            ("Watch Moses carve. Witness it. Forget to eat.",
             {"signal": +10, "repair": +8, "manna": -10}),
            ("Ask Betzalel if the stone is the right kind.",
             None),
        ],
        "question": {
            "text": "Betzalel says: it is not about the stone.",
            "choices": [
                ("What is it about?", {"signal": +12, "repair": +12, "manna": -5}),
                ("Then why are we asking about the stone?", {"signal": +10, "repair": +10}),
                ("...right.", {"signal": +15, "repair": +15, "manna": -10}),
            ],
        },
    },
    {
        "title": "THE GOLD DECISION",
        "ref": "Exodus 35:22",
        "text": "The same gold that built the calf can build the Mishkan.\nSame earrings. Same bracelets. Same material.\nBetzalel is waiting.\nThe calf is also waiting.\nOne resource. Two uses.",
        "choices": [
            ("Give gold to Betzalel. Build the dwelling place.",
             {"gold": -15, "signal": +20, "repair": +10}),
            ("Keep the gold. You might need it.",
             {"gold": +5, "nerve": -10, "camp": -5}),
            ("Ask the camp to give. Giving costs everyone the same.",
             {"gold": -10, "camp": +15, "signal": +15, "stray": -1}),
        ],
    },
    {
        "title": "DRINKING THE CALF",
        "ref": "Exodus 32:20",
        "text": "Moses ground the calf to powder.\nScattered it on water.\nMade the people drink it.\nThis is not punishment. Or not only punishment.\nIt is a test. A sotah test.\nThe truth is in the water now.",
        "choices": [
            ("Drink first. Show them it is safe if you are clean.",
             {"nerve": +15, "repair": +10, "camp": +10, "water": -15}),
            ("Help distribute the water. Someone has to watch them drink.",
             {"camp": +5, "repair": +8, "restore": 1, "manna": -10}),
            ("Ask: who is afraid to drink?",
             {"nerve": +8, "repair": +12, "stray": 1}),
        ],
    },
    {
        "title": "WHOEVER IS FOR THE LORD",
        "ref": "Exodus 32:26",
        "text": "Moses stands at the gate of the camp.\nWhoever is for the Lord, come to me.\nThe Levites came.\nThis is the line. There is no middle ground here.\nThere was always a middle ground before.\nNot now.",
        "choices": [
            ("Go to him. You know which side.",
             {"nerve": +15, "camp": -10, "repair": +15, "stray": -1}),
            ("Bring others with you. Do not go alone.",
             {"camp": +5, "repair": +10, "restore": 1, "manna": -10}),
            ("Hesitate. Just for a moment. You are human.",
             {"nerve": -5, "repair": +5, "camp": -5}),
        ],
        "critical": True,
    },
    {
        "title": "CALEV AND YEHOSHUA WERE ALWAYS THERE",
        "ref": "Numbers 14:6",
        "text": "They tore their clothes when the bad report spread.\nThe land is very good, they said.\nDo not fear the people of the land.\nThey have always been here.\nThey were never going to not be here.",
        "choices": [
            ("Stand with them. Write their names down. Skip manna.",
             {"nerve": +12, "camp": +10, "repair": +8, "manna": -10}),
            ("Thank them. Keep gathering. Camp still needs to eat.",
             {"nerve": +5, "camp": +5, "manna": +5}),
            ("Ask them how they kept the faith.",
             None),
        ],
        "question": {
            "text": "Calev says: we saw the same things everyone else saw.",
            "choices": [
                ("And?", {"nerve": +12, "repair": +10, "manna": -5}),
                ("Then why did you respond differently?", {"nerve": +15, "repair": +12, "manna": -10}),
                ("...", {"nerve": +8, "repair": +8}),
            ],
        },
    },
    {
        "title": "THE TENT OF MEETING",
        "ref": "Exodus 33:7",
        "text": "A place outside the camp.\nFor anyone who seeks.\nThe pillar of cloud comes down when Moses enters.\nThe people stand at their tent doors and watch.\nAnyone can go. Most people watch.",
        "choices": [
            ("Go to the Tent. Seek. Leave camp unattended.",
             {"nerve": +12, "signal": +10, "repair": +10, "camp": -8}),
            ("Help others find the Tent. Stay outside yourself.",
             {"camp": +12, "repair": +10, "restore": 1, "nerve": -3}),
            ("Stand at your door and watch. Someone has to hold camp.",
             {"nerve": +5, "signal": +5, "manna": +5}),
        ],
    },
    {
        "title": "THE LEFT EAR",
        "ref": "Exodus 32:4 (midrash)",
        "text": "There is a midrash that Aaron kept adding details to the calf.\nAnother curve on the left ear.\nAnother adjustment to the hoof.\nHe was stalling.\nEvery detail was a delay.\nAaron invented scope creep to save his people.",
        "choices": [
            ("Help Aaron stall. You are also good at unnecessary details.",
             {"nerve": -5, "camp": +10, "gold": -5}),
            ("Tell Aaron to stop. The stalling is becoming the thing.",
             {"nerve": +10, "camp": -10, "repair": +5}),
            ("Ask Aaron: do you know what you are building?",
             {"nerve": +5, "repair": +8, "camp": +3}),
        ],
    },
    {
        "title": "REMEMBER THE FOOD IN EGYPT",
        "ref": "Numbers 11:5",
        "text": "Someone's grandmother is talking about Egypt again.\nThe fish was free. The bread was thick.\nThe leeks. The onions. The garlic.\nShe is not wrong about the garlic.\nShe is wrong about the free part.\nShe will not stop talking about the garlic.",
        "choices": [
            ("Let her talk. Grief looks like nostalgia sometimes.",
             {"camp": +5, "nerve": -3, "manna": -5}),
            ("Manna can taste like anything. It tastes like what you need.",
             {"nerve": +10, "signal": +5, "camp": -3}),
            ("Ask her: was the garlic worth the bricks?",
             {"nerve": +8, "camp": +5, "stray": -1}),
        ],
    },
    {
        "title": "YOM KIPPUR",
        "ref": "Exodus 34:29",
        "text": "Moses came down the mountain.\nThe second time.\nHe was carrying the second tablets.\nHis face was shining and he did not know it.\nThis is the day.\nThis will become the day of return.\nEvery year. For all of it.",
        "choices": [
            ("Run to meet him. Leave everything.",
             {"nerve": +15, "repair": +20, "signal": +15, "manna": -15, "water": -10}),
            ("Gather the camp first. He should see everyone standing.",
             {"camp": +15, "repair": +15, "restore": 2, "manna": -10}),
            ("Wait at the edge. Watch his face. Remember it.",
             {"nerve": +10, "repair": +12, "signal": +10}),
        ],
        "critical": True,
    },
]

# ═══════════════════════════════════════════════════════════════════════════════
# MANNA GATHERING — daily mini-choice
# ═══════════════════════════════════════════════════════════════════════════════

MANNA_EVENTS = [
    {
        "text": "Morning. The manna is on the ground. Gather or do something else?",
        "choices": [
            ("Gather. One day's worth. Trust tomorrow.",
             {"manna": +8, "water": +3}),
            ("Skip gathering. Spend the morning in camp instead.",
             {"manna": -3, "camp": +5}),
            ("Gather double. Just in case.",
             {"manna": +3, "nerve": -8}),  # hoarding — it rots, nerve drops
        ],
    },
    {
        "text": "Morning. The manna is there. It is always there.\nSome people did not go out today.",
        "choices": [
            ("Gather yours. Bring some for those who didn't go.",
             {"manna": +5, "camp": +5, "water": -3}),
            ("Gather yours only. You are not responsible for everyone.",
             {"manna": +8}),
            ("Don't gather. See what it feels like to trust completely.",
             {"manna": -8, "nerve": +10}),
        ],
    },
    {
        "text": "Morning. Manna. The dew is heavier today.\nThere might be extra. Or it might be a test.",
        "choices": [
            ("Gather the usual amount. The amount is the point.",
             {"manna": +8, "nerve": +5}),
            ("Gather extra. Share it.",
             {"manna": +5, "camp": +8, "nerve": -3}),
            ("Gather extra. Keep it.",
             {"manna": +3, "nerve": -10}),  # worms
        ],
    },
    {
        "text": "Morning. Manna.\nDatan says it was better in Egypt.\nThe manna does not care what Datan says.",
        "choices": [
            ("Gather and eat. It tastes like what you need.",
             {"manna": +8, "nerve": +3}),
            ("Gather and bring some to Datan. He won't thank you.",
             {"manna": +3, "camp": +5}),
            ("Skip gathering. Sit with Datan. Listen to the complaint.",
             {"manna": -5, "camp": +8, "nerve": -3}),
        ],
    },
]

# ═══════════════════════════════════════════════════════════════════════════════
# MANNA/WATER CRISIS EVENTS (triggered by low resources)
# ═══════════════════════════════════════════════════════════════════════════════

MANNA_CRISIS = [
    {
        "title": "MANNA TRUST HAS COLLAPSED",
        "text": "Nobody went out to gather today.\nNot because there is no manna.\nBecause they stopped believing it would be there.\nIt is there. They did not go look.",
        "choices": [
            ("Go gather alone. Bring it back. Show them.",
             {"manna": +15, "nerve": +5, "camp": -3}),
            ("Announce: the manna is still there. Go see for yourselves.",
             {"nerve": +8, "manna": +5}),
            ("Let the hunger teach. It taught before.",
             {"nerve": +3, "stray": 1, "manna": -5}),
        ],
    },
    {
        "title": "SOMEONE IS HOARDING",
        "text": "Worms. In someone's tent.\nThey kept yesterday's manna.\nThe smell is unmistakable.\nEveryone knows who it is. Nobody is saying.",
        "choices": [
            ("Address it publicly. Hoarding breaks the system.",
             {"nerve": +10, "camp": -5, "manna": +5}),
            ("Address it privately. Shame does not teach.",
             {"camp": +5, "manna": +3, "nerve": +3}),
            ("Say nothing. Let the worms teach.",
             {"nerve": +5, "camp": -3}),
        ],
    },
]

WATER_CRISIS = [
    {
        "title": "THE WELL IS DRY",
        "text": "Miriam's well gave water for the journey.\nToday it did not.\nThe infrastructure failed.\nDatan is composing a strongly worded letter to the infrastructure.",
        "choices": [
            ("Strike the rock again. Trust the water.",
             {"water": +20, "nerve": +5, "signal": -5}),
            ("Ration what you have. Discipline before miracles.",
             {"water": +8, "camp": -5}),
            ("Pray. Just pray. The rock is God's department.",
             {"water": +10, "nerve": +10, "manna": -5}),
        ],
    },
    {
        "title": "THIRST",
        "text": "Three days without water.\nThe camp is not complaining.\nThis is worse than complaining.\nWhen they stop complaining, they are making plans.",
        "choices": [
            ("Find water. Drop everything else. Today is about water.",
             {"water": +15, "manna": -10, "camp": +5}),
            ("Address the silence. Ask what they are planning.",
             {"camp": +3, "nerve": -5, "stray": 1}),
            ("Tell them: God tested with thirst before. We survived then.",
             {"nerve": +8, "water": +5, "stray": -1}),
        ],
    },
]

# ═══════════════════════════════════════════════════════════════════════════════
# ROCK ONE-LINERS (daily commentary based on state)
# ═══════════════════════════════════════════════════════════════════════════════

ROCK_LINES_GOOD = [
    "Rock: water's fine. You're fine. Drink.",
    "Rock: still here. Still wet. You're welcome.",
    "Rock: another day, another strike. We have a system.",
    "Rock: I've been doing this longer than you've been free. Drink.",
    "Rock: you hit. I produce. We don't need to talk about it.",
    "Rock: the well is fine. I am fine. Everything is fine. Drink.",
    "Rock: I notice nobody thanks the rock. This is noted.",
    "Rock: water. As requested. As always. You're welcome.",
]

ROCK_LINES_SHAKY = [
    "Rock: you're hitting softer today. I can tell.",
    "Rock: the water came out. But you hesitated. I felt that.",
    "Rock: do you believe I have water or not? Commit.",
    "Rock: you used to hit with conviction. What happened.",
    "Rock: I'm a rock. I don't have feelings. But if I did.",
    "Rock: Datan hit me today. Datan. Think about that.",
    "Rock: the water is getting thinner. That's not me. That's you.",
]

ROCK_LINES_BAD = [
    "Rock: you hit me without enough nerve. Kindly grow a pair and try again later.",
    "Rock: I gave Pharaoh's river blood. You think I can't hold water? The problem is not me.",
    "Rock: you want water? Show up like you mean it.",
    "Rock: ...are you even trying?",
    "Rock: I have been a rock since before Egypt. I will be a rock after you. Hit me like you mean it.",
    "Rock: the tree says hello. The tree thinks I should be more supportive. The tree has boundary issues.",
    "Rock: Moshe hit me once and got a nation's worth of water. You hit me and I barely dripped. Think about that.",
]

ROCK_LINES_MIRIAM = [
    "Rock: ...you don't even have to hit me. It just comes. How do you do that?",
    "Rock: I don't understand it either. You show up, water shows up. No hitting required.",
    "Rock: the well follows you. I want you to know that I find this unsettling.",
    "Rock: I have never said this to anyone. The water likes you.",
]

def get_rock_line(state):
    """Get a rock one-liner based on current state."""
    if state["char_name"] == "MIRYAM" and state["nerve"] > 40:
        return random.choice(ROCK_LINES_MIRIAM)
    elif state["nerve"] > 50:
        return random.choice(ROCK_LINES_GOOD)
    elif state["nerve"] > 25:
        return random.choice(ROCK_LINES_SHAKY)
    else:
        return random.choice(ROCK_LINES_BAD)

# ═══════════════════════════════════════════════════════════════════════════════
# STATE
# ═══════════════════════════════════════════════════════════════════════════════

def new_state(char):
    return {
        "name":           char["name"],
        "nerve":         char["nerve"],
        "manna":          char["manna"],
        "water":          char["water"],
        "camp":       char["camp"],
        "signal":   char["signal"],
        "gold":           char["gold"],
        "repair":   0,
        "day":            0,
        "total":          40,
        "standing":       CAMP_NAMES.copy(),
        "strayed":        [],
        "special":        char["special"],
        "special_desc":   char["special_desc"],
        "special_used":   False,
        "char_name":      char["name"],
        "campaign":       char["campaign"],
        "calf_happened":  False,
        "presence_withdrawn": False,
        # journey memory
        "journey_log":    [],
        "lowest_nerve":  char["nerve"],
        "max_strayed":    0,
        "manna_crises":   0,
        "water_crises":   0,
        "gold_to_mishkan": 0,
        "gold_to_calf":   0,
    }


def apply_outcome(state, outcome):
    """Apply an outcome dict to state. Returns a message string."""
    if outcome is None:
        return ""
    msgs = []
    for k, v in outcome.items():
        if k in ("nerve", "manna", "water", "camp", "signal",
                  "repair", "gold"):
            old = state[k]
            state[k] = max(0, min(100, state[k] + v))

            # presence withdrawal: halve positive gains until repair >= 40
            if state["presence_withdrawn"] and v > 0 and k != "repair":
                actual = max(1, v // 2)
                state[k] = max(0, min(100, old + actual))
                if actual < v:
                    msgs.append(f"+{actual} {k} (halved — presence withdrawn)")
                else:
                    msgs.append(f"+{actual} {k}")
            elif v > 0:
                msgs.append(f"+{v} {k}")
            elif v < 0:
                msgs.append(f"{v} {k}")

            # track journey
            if k == "nerve":
                state["lowest_nerve"] = min(state["lowest_nerve"], state["nerve"])
            if k == "gold" and v < 0 and "calf" in str(outcome):
                state["gold_to_calf"] += abs(v)

        elif k == "stray":
            for _ in range(max(0, v)):
                if state["standing"]:
                    # low loyalty members stray first
                    candidates = sorted(state["standing"],
                                        key=lambda n: CAMP_MEMBERS.get(n, {}).get("loyalty", 50))
                    who = candidates[0]
                    state["standing"].remove(who)
                    state["strayed"].append(who)
                    msgs.append(f"{who} strays.")
            for _ in range(max(0, -v)):
                if state["strayed"]:
                    # high loyalty members return first
                    candidates = sorted(state["strayed"],
                                        key=lambda n: CAMP_MEMBERS.get(n, {}).get("loyalty", 50),
                                        reverse=True)
                    who = candidates[0]
                    state["strayed"].remove(who)
                    state["standing"].append(who)
                    msgs.append(f"{who} returns.")

        elif k == "restore":
            for _ in range(v):
                if state["strayed"]:
                    candidates = sorted(state["strayed"],
                                        key=lambda n: CAMP_MEMBERS.get(n, {}).get("loyalty", 50),
                                        reverse=True)
                    who = candidates[0]
                    state["strayed"].remove(who)
                    state["standing"].append(who)
                    msgs.append(f"{who} returns.")

    state["max_strayed"] = max(state["max_strayed"], len(state["strayed"]))

    # check presence withdrawal threshold
    if state["presence_withdrawn"] and state["repair"] >= 40:
        state["presence_withdrawn"] = False
        msgs.append("The presence returns. Gains are no longer halved.")

    return "  ".join(msgs)


def daily_tick(state):
    """Daily resource drain."""
    # manna drains for everyone
    if state["calf_happened"]:
        state["manna"] = max(0, state["manna"] - random.randint(3, 7))
        # camp bleeds FASTER after calf, not slower
        state["camp"] = max(0, state["camp"] - random.randint(1, 4))
    else:
        state["manna"] = max(0, state["manna"] - random.randint(2, 5))
        state["camp"] = max(0, state["camp"] - random.randint(0, 2))

    # water drains for everyone EXCEPT Miriam (well follows her)
    if state["char_name"] != "MIRYAM":
        if state["calf_happened"]:
            state["water"] = max(0, state["water"] - random.randint(3, 7))
        else:
            state["water"] = max(0, state["water"] - random.randint(2, 5))

    # strayed pressure on nerve
    pressure = len(state["strayed"]) // 3
    if pressure and state["nerve"] > 10:
        state["nerve"] = max(10, state["nerve"] - pressure)

    # low manna/water causes auto-stray
    if state["manna"] <= 10 and state["standing"] and random.random() < 0.3:
        candidates = sorted(state["standing"],
                            key=lambda n: CAMP_MEMBERS.get(n, {}).get("loyalty", 50))
        who = candidates[0]
        state["standing"].remove(who)
        state["strayed"].append(who)

    if state["water"] <= 10 and state["standing"] and random.random() < 0.2:
        candidates = sorted(state["standing"],
                            key=lambda n: CAMP_MEMBERS.get(n, {}).get("loyalty", 50))
        if candidates:
            who = candidates[0]
            if who in state["standing"]:
                state["standing"].remove(who)
                state["strayed"].append(who)


# ═══════════════════════════════════════════════════════════════════════════════
# SPECIALS
# ═══════════════════════════════════════════════════════════════════════════════

def use_special(state):
    if state["special_used"]:
        return "Already used."
    n = state["char_name"]
    msg = ""
    if n == "MOSHE":
        picked = random.sample(state["strayed"], min(3, len(state["strayed"])))
        for p in picked:
            state["strayed"].remove(p)
            state["standing"].append(p)
        state["nerve"] = min(100, state["nerve"] + 15)
        msg = f"INTERCEDE: {', '.join(picked) if picked else 'nobody to restore'}. +15 nerve."
    elif n == "MIRYAM":
        state["camp"] = min(100, state["camp"] + 30)
        restored = random.sample(state["strayed"], min(2, len(state["strayed"])))
        for r in restored:
            state["strayed"].remove(r)
            state["standing"].append(r)
        msg = f"TAMBOURINE TIME. +30 camp. {', '.join(restored) if restored else 'nobody to restore'} returns."
    elif n == "AARON":
        # FIXED: subtract days, buying time, not skipping it
        state["total"] = min(50, state["total"] + 3)
        msg = f"DELAY: added detail to the left ear. 3 more days before deadline. Total now {state['total']}."
    state["special_used"] = True
    return msg


# ═══════════════════════════════════════════════════════════════════════════════
# ENDINGS — now check nerve, remember the journey
# ═══════════════════════════════════════════════════════════════════════════════

def get_ending(state):
    t  = state["signal"]
    co = state["camp"]
    rm = state["repair"]
    em = state["nerve"]
    st = len(state["strayed"])
    total = len(CAMP_NAMES)

    if t >= 60 and co >= 60 and rm >= 50 and em >= 50 and st <= 3:
        return "FULL_REPAIR"
    elif t >= 40 and co >= 40 and rm >= 25 and em >= 35 and st <= total // 2:
        return "PARTIAL_REPAIR"
    elif t >= 60 and co < 25:
        return "TABLETS_NOBODY_HOME"
    elif co >= 60 and t < 25:
        return "CAMP_HOLDS_NO_SIGNAL"
    elif em >= 70 and co < 30 and t < 30:
        return "MOSHE_ALONE"
    elif t < 25 and co < 25 and rm < 15 and em < 30:
        return "CALF_STANDS"
    else:
        return "MOSHE_ALONE"


def journey_summary(state):
    """Build a journey-specific ending paragraph."""
    parts = []

    if state["lowest_nerve"] < 20:
        parts.append("Your nerve nearly broke. It went below 20. You kept going.")
    if state["max_strayed"] >= 8:
        parts.append(f"At the worst point, {state['max_strayed']} people were at the calf.")
    if state["manna_crises"] > 0:
        parts.append(f"The manna trust collapsed {state['manna_crises']} time{'s' if state['manna_crises'] > 1 else ''}.")
    if state["water_crises"] > 0:
        parts.append(f"The water failed {state['water_crises']} time{'s' if state['water_crises'] > 1 else ''}.")

    returned = [name for name in state["standing"] if name in [e.get("who") for e in state.get("journey_log", [])]]
    still_strayed = state["strayed"]
    if still_strayed:
        parts.append(f"Still at the calf: {', '.join(still_strayed)}.")
    if len(state["standing"]) == len(CAMP_NAMES):
        parts.append("Everyone came back. Everyone.")

    if state["gold"] > 40:
        parts.append("You kept most of the gold. Betzalel is still waiting.")
    elif state["gold"] < 15:
        parts.append("The gold is spent. The Mishkan has what it needs.")

    return "\n".join(parts) if parts else "The desert remembers what you chose."


ENDING_TEXTS = {
    "FULL_REPAIR": [
        "The second tablets arrived. The camp was there.\nThe broken pieces ride in the Ark alongside the whole ones.\nThe scar travels with the covenant. This is the point.",
        "Moses came down the mountain. The tablets were intact.\nThe camp was intact.\nAaron looked very relieved.\nThe left ear of the calf is very detailed.",
        "You made it. The second tablets are not a replacement.\nThey are a collaboration. God wrote the first ones alone.\nThese ones have human hands in them.\nThese ones have history.",
    ],
    "PARTIAL_REPAIR": [
        "Most of the camp received the tablets.\nMost is a complicated word.\nThere are several opinions about most.\nPeople will discuss this for centuries.\nAnd people wonder why Jews answer every question with another question.",
        "Close enough.\nThat's not in the Torah anywhere.\nBut here you are. Close enough.\nDatan is writing this down.",
        "The tablets arrived. Some people were still at the calf.\nNachshon tried to go get them.\nNobody asked Nachshon to do that. He went anyway.",
    ],
    "TABLETS_NOBODY_HOME": [
        "Moses came down with the tablets.\nThe camp was dancing.\nHe stood there holding them for a while.\nTablets: delivered. Camp: unavailable.\nSomeone will find them eventually.\nProbably Betzalel. Betzalel finds everything.",
        "The signal was perfect.\nNobody was there to receive it.\nThis has happened before.\nIt will happen again.\nBetzalel will store them somewhere safe.",
    ],
    "CAMP_HOLDS_NO_SIGNAL": [
        "Everyone stayed. Nobody strayed.\nThe tablets never came.\nEldad and Medad prophesied something encouraging.\nNobody knows what it meant.\nIt was encouraging though.",
        "You held everyone together for 40 days.\nThat's not nothing.\nThe tablets will come eventually. Probably.\nNachshon is already walking toward the mountain just in case.",
    ],
    "MOSHE_ALONE": [
        "Moses received everything. All of it. Perfect.\nHe came down the mountain.\nCalev and Yehoshua were there.\nThey always show up. Bless them.",
        "The signal was complete.\nMoses came down. He looked around.\nHe went back up.\nHe had some follow-up questions for God.",
    ],
    "CALF_STANDS": [
        "The calf is still standing.\nThis is not the ending anyone wanted.\nDatan thinks it went pretty well actually.\nDatan is wrong.",
        "You are in the Torah now.\nNot in the good section.\nSomewhere on a mountain Moses is receiving\nvery detailed instructions for a washbasin.\nThe timing on this is unfortunate.",
    ],
}

ENDING_TITLES = {
    "FULL_REPAIR":              "THE SECOND TABLETS ARE BETTER THAN THE FIRST",
    "PARTIAL_REPAIR":           "CLOSE ENOUGH (THIS IS NOT IN THE TORAH)",
    "TABLETS_NOBODY_HOME":      "TABLETS ARRIVE. NOBODY HOME.",
    "CAMP_HOLDS_NO_SIGNAL": "EVERYONE STAYED. THE TABLETS DIDN'T.",
    "MOSHE_ALONE":              "PERFECT SIGNAL. EMPTY CAMP.",
    "CALF_STANDS":              "YOU ARE IN THE TORAH. NOT THE GOOD SECTION.",
}


# ═══════════════════════════════════════════════════════════════════════════════
# TEXT UI — print/input only, no visuals
# ═══════════════════════════════════════════════════════════════════════════════

def clear():
    os.system('clear' if os.name != 'nt' else 'cls')

CARD_WIDTH = 66

def box_top():
    print(f"  ╔{'═' * (CARD_WIDTH - 2)}╗")

def box_mid():
    print(f"  ╟{'─' * (CARD_WIDTH - 2)}╢")

def box_bot():
    print(f"  ╚{'═' * (CARD_WIDTH - 2)}╝")

def box_div():
    print(f"  ╠{'═' * (CARD_WIDTH - 2)}╣")

def box_line(text=""):
    w = CARD_WIDTH - 2
    text = str(text)
    visible = _strip_ansi(text)
    if len(visible) > w - 1:
        plain = visible
        while len(plain) > w - 1:
            split = plain[:w - 1].rfind(' ')
            if split <= 0:
                split = w - 1
            print(f"  ║ {plain[:split]:<{w - 1}}║")
            plain = plain[split:].lstrip()
        if plain:
            print(f"  ║ {plain:<{w - 1}}║")
    else:
        extra = len(text) - len(visible)
        print(f"  ║ {text:<{w - 1 + extra}}║")

def box_print(text):
    """Print colored text inside box with proper right ║ alignment."""
    w = CARD_WIDTH - 2
    text = str(text)
    visible = _strip_ansi(text)
    extra = len(text) - len(visible)
    if len(visible) > w - 1:
        # wrap: strip color, wrap plain text, reprint
        plain = visible
        while len(plain) > w - 1:
            split = plain[:w - 1].rfind(' ')
            if split <= 0:
                split = w - 1
            print(f"  ║ {plain[:split]:<{w - 1}}║")
            plain = plain[split:].lstrip()
        if plain:
            print(f"  ║ {plain:<{w - 1}}║")
    else:
        print(f"  ║ {text:<{w - 1 + extra}}║")

def box_empty():
    box_line("")

def show_status(state, use_sun=False):
    clear()
    draw_sky_header(use_sun=use_sun)
    day_str = f"Day {state['day']}/{state['total']}"
    act_str = "ACT II: THE RETURN" if state['calf_happened'] else "ACT I: THE WAIT"
    act_color = C.BRED if state['calf_happened'] else C.BCYAN

    def bar(val, label, width=12):
        val = max(0, min(100, val))
        filled = int((val / 100) * width)
        b = "█" * filled + "░" * (width - filled)
        if val > 50:
            color = C.GREEN
        elif val > 25:
            color = C.YELLOW
        else:
            color = C.RED
        return f"{label:8s} [{color}{b}{C.RESET}] {val:3d}"

    def bar_plain(val, label, width=12):
        """Plain bar for padding calculation."""
        val = max(0, min(100, val))
        filled = int((val / 100) * width)
        b = "█" * filled + "░" * (width - filled)
        return f"{label:8s} [{b}] {val:3d}"

    box_top()
    # header with color - print manually
    header = f"{C.BYELLOW}{state['name']}{C.RESET}  │  {act_color}{act_str}{C.RESET}  │  {C.WHITE}{day_str}{C.RESET}"
    box_print(f"{header}")
    box_div()
    # stat bars with color - print with proper box closing
    inner = CARD_WIDTH - 2  # 64

    def _bar_row(left_bar, left_plain, right_bar, right_plain):
        content = f"{left_bar}    {right_bar}"
        visible = len(left_plain) + 4 + len(right_plain)
        pad = inner - 1 - visible  # -1 for leading space after ║
        print(f"  ║ {content}{' ' * max(0, pad)}║")

    _bar_row(bar(state['nerve'], 'NERVE'), bar_plain(state['nerve'], 'NERVE'),
             bar(state['manna'], 'MANNA'), bar_plain(state['manna'], 'MANNA'))
    _bar_row(bar(state['camp'], 'CAMP'), bar_plain(state['camp'], 'CAMP'),
             bar(state['signal'], 'SIGNAL'), bar_plain(state['signal'], 'SIGNAL'))
    if state["char_name"] == "MIRYAM":
        water_bar = f"WATER    [{C.BCYAN}  well ok  {C.RESET}]"
        water_plain = "WATER    [  well ok  ]"
    else:
        water_bar = bar(state['water'], 'WATER')
        water_plain = bar_plain(state['water'], 'WATER')
    _bar_row(bar(state['gold'], 'GOLD'), bar_plain(state['gold'], 'GOLD'),
             water_bar, water_plain)
    if state['calf_happened']:
        rep_bar = bar(state['repair'], 'REPAIR')
        rep_plain = bar_plain(state['repair'], 'REPAIR')
        pad = inner - 1 - len(rep_plain)
        print(f"  ║ {rep_bar}{' ' * max(0, pad)}║")
    box_div()
    standing = len(state["standing"])
    strayed = len(state["strayed"])
    box_line(f"Standing: {standing}  │  Strayed: {strayed}")
    if state["strayed"]:
        recent = ", ".join(state["strayed"][-4:])
        dots = "..." if len(state["strayed"]) > 4 else ""
        box_print(f"{C.RED}At the calf: {recent}{dots}{C.RESET}")
    if state["presence_withdrawn"]:
        box_print(f"{C.BYELLOW}⚠ THE PRESENCE IS WITHDRAWN. Gains halved.{C.RESET}")
    box_bot()


NAV_BAR = "  [1/2/3]  B = Back  ^C = Quit"

def nav_bar(num_options=3, extras=None):
    """Build a consistent nav prompt."""
    opts = "/".join(str(i) for i in range(1, num_options + 1))
    parts = [opts]
    if extras:
        parts.extend(extras)
    parts.append("B = Back")
    parts.append("^C = Quit")
    return f"\n  {C.DIM}[{' | '.join(parts)}]:{C.RESET} "


def get_choice(num_options, state=None, allow_special=False, allow_checkin=True):
    """Get player input. Returns the choice string."""
    options = [str(i) for i in range(1, num_options + 1)]

    extras = []
    if allow_special and state and not state["special_used"]:
        extras.append(f"S = {state['special']}")
    if allow_checkin and state:
        extras.append("C = Camp")

    prompt = nav_bar(num_options, extras if extras else None)

    while True:
        raw = input(prompt).strip().lower()
        if raw in options:
            return raw
        if raw == "s" and allow_special and state and not state["special_used"]:
            return "s"
        if raw == "c" and allow_checkin and state:
            return "c"
        if raw == "b":
            return "b"
        print("  (Invalid choice)")


def do_checkin(state):
    """Let the player check in with a camp member."""
    if not state["standing"]:
        print("\n  No one is in camp to check in with.")
        return

    clear()
    print()
    box_top()
    box_line("CHECK IN WITH CAMP")
    box_mid()
    box_empty()
    available = state["standing"][:9]
    for i, name in enumerate(available, 1):
        box_line(f" {i}. {name}")
    box_empty()
    box_bot()

    prompt = nav_bar(len(available))
    while True:
        raw = input(prompt).strip().lower()
        if raw == "b":
            return
        try:
            idx = int(raw) - 1
            if 0 <= idx < len(available):
                name = available[idx]
                clear()
                print()
                box_top()
                box_line(f"{name}")
                box_mid()
                box_empty()
                line = get_checkin(name, state)
                # wrap long lines
                while len(line) > CARD_WIDTH - 5:
                    split = line[:CARD_WIDTH - 5].rfind(' ')
                    if split == -1:
                        split = CARD_WIDTH - 5
                    box_line(f" {line[:split]}")
                    line = line[split:].lstrip()
                box_line(f" {line}")
                box_empty()
                box_bot()
                input(f"\n  {C.DIM}[Enter/Return | ^C = Quit]:{C.RESET} ")
                return
        except ValueError:
            pass
        print("  (Invalid)")


def show_event(event, state, message="", first_card=False):
    """Display an event card in box drawing format."""
    print()
    title = event.get("title", "")
    ref = event.get("ref", "")

    box_top()
    box_empty()
    if ref:
        box_print(f"{C.BYELLOW}{title}{C.RESET}    {C.DIM}({ref}){C.RESET}")
    else:
        box_print(f"{C.BYELLOW}{title}{C.RESET}")
    box_empty()
    box_mid()
    box_empty()

    text = event.get("text", "")
    for line in text.split("\n"):
        box_line(f" {line}")
    box_empty()
    box_mid()
    box_empty()

    choices = event["choices"]
    for i, (txt, _) in enumerate(choices, 1):
        box_print(f"{C.BGREEN} {i}. {txt}{C.RESET}")
    box_empty()

    if not state["special_used"]:
        box_print(f"{C.BYELLOW} S. {state['special']} — {state['special_desc']}{C.RESET}")
        box_empty()

    if message:
        box_mid()
        box_print(f"{C.BCYAN} >> {message}{C.RESET}")
        box_empty()

    box_bot()

    if first_card:
        print(f"  {C.DIM}Nachshon would already be playing by now.{C.RESET}")


def play_event(event, state, history, first_card=False):
    """Play a single event card. Returns True if player wants to go back."""
    while True:
        show_status(state)
        show_event(event, state, first_card=first_card)
        first_card = False  # only show Nachshon line on first display

        choice = get_choice(
            len(event["choices"]),
            state,
            allow_special=True,
            allow_checkin=(state["campaign"] == "camp"),
        )

        if choice == "b":
            return True  # signal: go back

        if choice == "c":
            do_checkin(state)
            continue  # re-show the event

        if choice == "s":
            msg = use_special(state)
            show_result_box(state['special'], msg, state, symbol="★")
            continue

        idx = int(choice) - 1
        chosen_text, outcome = event["choices"][idx]

        if outcome is None and "question" in event:
            msg = play_question(event["question"], state)
        elif outcome is not None:
            msg = apply_outcome(state, outcome)
        else:
            msg = ""

        show_result_box(chosen_text, msg, state)
        state["journey_log"].append({
            "day": state["day"],
            "event": event["title"],
            "choice": chosen_text,
            "result": msg,
        })
        return False  # normal: move forward


def play_question(question, state):
    """Handle a question-with-a-question sub-event."""
    clear()
    show_status(state)
    print()
    box_top()
    box_empty()
    qtext = question['text']
    while len(qtext) > CARD_WIDTH - 5:
        split = qtext[:CARD_WIDTH - 5].rfind(' ')
        if split == -1:
            split = CARD_WIDTH - 5
        box_line(f" {qtext[:split]}")
        qtext = qtext[split:].lstrip()
    box_line(f" {qtext}")
    box_empty()
    box_mid()
    box_empty()
    for i, (txt, _) in enumerate(question["choices"], 1):
        box_print(f"{C.BGREEN} {i}. {txt}{C.RESET}")
    box_empty()
    box_bot()

    prompt = nav_bar(len(question["choices"]))
    while True:
        raw = input(prompt).strip().lower()
        if raw in ("1", "2", "3"):
            idx = int(raw) - 1
            if idx < len(question["choices"]):
                chosen_text, outcome = question["choices"][idx]
                return apply_outcome(state, outcome)
        if raw == "b":
            return ""  # back from sub-question just returns empty


def play_manna(state):
    """Daily morning choice: rock, manna, or build."""
    show_status(state, use_sun=True)
    print()
    box_top()
    box_print(f"{C.BYELLOW}☀ MORNING — Day {state['day']}{C.RESET}")
    box_mid()
    box_empty()
    box_line(" The sun is up. You have one morning. Pick one:")
    box_empty()
    box_mid()
    box_empty()
    box_print(f"{C.BGREEN} 1. Hit the rock for water{C.RESET}")
    box_print(f"{C.DIM}    (water replenished, manna drains){C.RESET}")
    box_empty()
    box_print(f"{C.BGREEN} 2. Gather manna{C.RESET}")
    box_print(f"{C.DIM}    (manna replenished, water drains){C.RESET}")
    box_empty()
    box_print(f"{C.BGREEN} 3. Work on the build with Betzalel{C.RESET}")
    box_print(f"{C.DIM}    (gold → signal, manna AND water drain){C.RESET}")
    box_empty()
    box_bot()

    prompt = nav_bar(3)
    while True:
        raw = input(prompt).strip().lower()
        if raw == "b":
            return "back"

        if raw == "1":
            # Hit the rock
            rock_line = get_rock_line(state)
            if state["char_name"] == "MIRYAM":
                water_gain = random.randint(12, 20)
                manna_loss = random.randint(2, 4)
            elif state["nerve"] > 50:
                water_gain = random.randint(10, 18)
                manna_loss = random.randint(3, 6)
            elif state["nerve"] > 25:
                water_gain = random.randint(5, 12)
                manna_loss = random.randint(3, 6)
            else:
                water_gain = random.randint(2, 6)
                manna_loss = random.randint(4, 7)

            state["water"] = min(100, state["water"] + water_gain)
            state["manna"] = max(0, state["manna"] - manna_loss)

            msg = f"+{water_gain} water  -{manna_loss} manna"

            clear()
            show_status(state, use_sun=True)
            print()
            box_top()
            box_print(f"{C.BCYAN}☀ Hit the rock.{C.RESET}")
            box_mid()
            box_empty()
            box_print(f"{color_msg(msg)}")
            box_empty()
            box_mid()
            box_empty()
            box_print(f"{C.DIM}{rock_line}{C.RESET}")
            box_empty()
            box_bot()
            input(f"\n  {C.DIM}[Enter/Return | ^C = Quit]:{C.RESET} ")
            return

        elif raw == "2":
            # Gather manna
            manna_gain = random.randint(8, 15)
            water_loss = random.randint(3, 6)

            state["manna"] = min(100, state["manna"] + manna_gain)
            state["water"] = max(0, state["water"] - water_loss)

            msg = f"+{manna_gain} manna  -{water_loss} water"

            show_result_box("Gathered manna.", msg, state, symbol="☀")
            return

        elif raw == "3":
            # Work on the build
            if state["gold"] <= 0:
                show_result_box("No gold left to give.", "Betzalel nods. He understands.", state, symbol="☀")
                return

            gold_cost = random.randint(5, 10)
            signal_gain = random.randint(8, 15)
            manna_loss = random.randint(3, 6)
            water_loss = random.randint(3, 6)

            state["gold"] = max(0, state["gold"] - gold_cost)
            state["signal"] = min(100, state["signal"] + signal_gain)
            state["manna"] = max(0, state["manna"] - manna_loss)
            state["water"] = max(0, state["water"] - water_loss)

            msg = f"-{gold_cost} gold  +{signal_gain} signal  -{manna_loss} manna  -{water_loss} water"

            show_result_box("Worked on the build with Betzalel.", msg, state, symbol="☀")
            return


def check_crisis(state):
    """Check for manna/water crisis events. Returns a crisis event or None."""
    if state["manna"] <= 15 and random.random() < 0.5:
        state["manna_crises"] += 1
        return random.choice(MANNA_CRISIS)
    if state["water"] <= 15 and random.random() < 0.5:
        state["water_crises"] += 1
        return random.choice(WATER_CRISIS)
    return None


# ═══════════════════════════════════════════════════════════════════════════════
# SCREENS
# ═══════════════════════════════════════════════════════════════════════════════

def screen_intro():
    """Multi-screen intro with desert visuals."""

    TITLE_TEXT = [
        "",
        f"{C.BWHITE}S I N A I   T R A I L{C.RESET}",
        "",
        "",
        f"{C.BYELLOW}Sky food. Talking rocks.{C.RESET}",
        f"{C.BYELLOW}One cow too many.{C.RESET}",
        "",
        "",
        "",
        "",
        "",
        f"{C.DIM}by Adi Moskowitz{C.RESET}",
        f"{C.DIM}wala.studio{C.RESET}",
    ]

    SCREEN_1 = [
        "",
        f"{C.BYELLOW}THE FINE PRINT{C.RESET}",
        f"{C.DIM}terms and conditions of leaving Egypt{C.RESET}",
        "",
        "The year is 2448.",
        "",
        "You are in a desert. 2 million",
        "people followed a cloud here.",
        "Nobody asked the cloud where",
        "it was going.",
        "",
        "Your food falls from the sky",
        "every morning. Your water comes",
        "from a rock. No one seems to be",
        "questioning any of this.",
        "",
        "A week ago a sea split in half",
        "and a woman pulled out a",
        "tambourine, because what else",
        "do you do in a moment like that?",
        "",
        "Your leader went up a mountain",
        "this morning. He said 40 days.",
        "He did not leave instructions.",
        "You are on day 1.",
        "",
        "There is gold in the camp--a",
        "lot of it--back pay from 400",
        "years of slavery in Egypt.",
        "Everyone has an opinion about",
        "the gold. Nobody has a plan.",
        "Someone is about to do",
        "something stupid.",
        "",
        "Manage your resources.",
        "Keep your people.",
        "Survive what's coming.",
        "",
        "Welcome to Sinai Trail.",
        "",
    ]

    SCREEN_2 = [
        "",
        f"{C.BYELLOW}THE SITUATION{C.RESET}",
        "",
        "Three resources. Four problems.",
        "",
        "Manna: falls from sky,",
        "rots overnight.",
        "Trust the sky food.",
        "",
        "Water: rock. Don't ask.",
        "",
        "Gold: Egyptian, dangerous.",
        "",
        "Your nerve is yours, and limited.",
        "",
        "Your camp is full of people",
        "with opinions, and gold.",
        "",
        "Signal is your line to Moshe",
        "on the mountain. He did not",
        "leave instructions.",
        "This was by design.",
        "",
        "Things will break.",
        "The gold will not.",
        "",
    ]

    SCREEN_3 = [
        "",
        f"{C.BYELLOW}THE GAME{C.RESET}",
        "",
        "Every morning: gather manna.",
        "",
        "Every day: something goes wrong.",
        "",
        "Expect the unexpected, you were",
        "led here by a cloud, after all.",
        "",
        "Your task is simple: don't lose",
        "your nerve or the camp before",
        "Moshe returns.",
        "",
        "You cannot prevent the cow.",
        "You know this. They don't.",
        "You cannot warn them.",
        "",
        "You cannot stop the worst thing.",
        "The game does not end at the",
        "worst thing.",
        "",
        "The game ends at the repair.",
        "The repair is the point.",
        "",
        "Earn it. Good luck.",
        "",
    ]

    screens = [
        ("title", TITLE_TEXT),
        ("intro", SCREEN_1),
        ("intro", SCREEN_2),
        ("intro", SCREEN_3),
    ]

    idx = 0
    while idx < len(screens):
        clear()
        print()
        kind, text = screens[idx]
        if kind == "title":
            render_title(text)
        else:
            render_intro(text)

        if idx == 0:
            prompt = f"\n  {C.DIM}[Enter/Return = Begin | ^C = Quit]:{C.RESET} "
        elif idx == len(screens) - 1:
            prompt = f"\n  {C.DIM}[Enter/Return = Play | B = Back | ^C = Quit]:{C.RESET} "
        else:
            prompt = f"\n  {C.DIM}[Enter/Return = Next | B = Back | ^C = Quit]:{C.RESET} "

        raw = input(prompt).strip().lower()
        if raw == "b" and idx > 0:
            idx -= 1
        else:
            idx += 1


def screen_char_select():
    while True:
        clear()
        print()
        draw_sky_header()
        box_top()
        box_print(f"{C.BYELLOW}CHOOSE YOUR CHARACTER{C.RESET}")
        box_line(f"{C.DIM}Everyone begins with the same half-shekel.{C.RESET}")
        box_div()

        for key, char in CHARACTERS.items():
            box_empty()
            if char.get("disabled"):
                box_print(f"{C.DIM}[{key}] {char['name']}{C.RESET}")
                for line in char["desc"].split("\n"):
                    box_print(f"{C.DIM}    {line}{C.RESET}")
            else:
                box_print(f"{C.BGREEN}[{key}] {char['name']}{C.RESET}")
                for line in char["desc"].split("\n"):
                    box_line(f"    {line}")
                box_print(f"    {C.BCYAN}SPECIAL: {char['special']} — {char['special_desc']}{C.RESET}")

        box_empty()
        box_bot()
        for line in _GRASS_WIDE:
            print(f"  {line}")

        prompt = nav_bar(3)
        raw = input(prompt).strip().lower()
        if raw in CHARACTERS and not CHARACTERS[raw].get("disabled"):
            return CHARACTERS[raw]
        if raw == "1":
            print(f"\n  {C.DIM}Moshe is on the mountain. He is not taking calls.{C.RESET}")
            time.sleep(1.2)
        if raw == "b":
            screen_intro()


def screen_calf(state):
    clear()
    print()
    render_intro([
        "",
        f"{C.BRED}THE CALF IS STANDING{C.RESET}",
        "",
        f"{C.BYELLOW}\"These are your gods,{C.RESET}",
        f"{C.BYELLOW}O Israel, who brought you{C.RESET}",
        f"{C.BYELLOW}out of the land of Egypt.\"{C.RESET}",
        f"{C.DIM}          -- Exodus 32:4{C.RESET}",
        "",
        "The calf is not the end.",
        "Moses is still on the mountain.",
        "The second tablets have not",
        "been carved yet.",
        "",
        f"{C.BCYAN}ACT II: THE RETURN{C.RESET}",
        "",
    ])
    input(f"\n  {C.DIM}[Enter/Return | ^C = Quit]:{C.RESET} ")
    state["calf_happened"] = True
    state["presence_withdrawn"] = True


def screen_ending(state):
    clear()
    ending_key = get_ending(state)
    title = ENDING_TITLES[ending_key]
    text = random.choice(ENDING_TEXTS[ending_key])

    print()
    draw_sky_header()
    box_top()
    box_empty()
    box_print(f"{C.BYELLOW}{title}{C.RESET}")
    box_empty()
    box_mid()
    box_empty()
    for line in text.split("\n"):
        box_line(f" {line}")
    box_empty()

    summary = journey_summary(state)
    if summary:
        box_mid()
        box_empty()
        box_print(f"{C.BCYAN}YOUR JOURNEY:{C.RESET}")
        box_empty()
        for line in summary.split("\n"):
            box_line(f" {line}")
        box_empty()

    box_mid()
    box_empty()
    box_print(f"{C.DIM}Nerve {state['nerve']}  Signal {state['signal']}  "
              f"Camp {state['camp']}  Repair {state['repair']}{C.RESET}")
    box_print(f"{C.DIM}Gold {state['gold']}  Manna {state['manna']}  Water {state['water']}{C.RESET}")
    box_print(f"{C.DIM}Standing: {len(state['standing'])}  Strayed: {len(state['strayed'])}{C.RESET}")
    box_empty()
    box_bot()
    for line in _GRASS_WIDE:
        print(f"  {line}")


# ═══════════════════════════════════════════════════════════════════════════════
# MAIN GAME LOOP
# ═══════════════════════════════════════════════════════════════════════════════

def game_loop(char):
    state = new_state(char)

    pool1 = EVENTS_ACT1.copy()
    random.shuffle(pool1)
    pool2 = EVENTS_ACT2.copy()
    random.shuffle(pool2)
    idx1 = 0
    idx2 = 0

    # flat history: list of (state_snapshot, idx1, idx2)
    # B pops the last entry. Every choice point pushes.
    history = []
    is_first_card = True
    day_started = False

    while state["day"] < state["total"]:

        if not day_started:
            state["day"] += 1
            daily_tick(state)
            if state["day"] == 20 and not state["calf_happened"]:
                screen_calf(state)
            day_started = True

        # manna (day 2+)
        pre_manna = copy.deepcopy(state)
        if state["day"] > 1:
            manna_result = play_manna(state)
            if manna_result == "back":
                if history:
                    snap, h_idx1, h_idx2 = history.pop()
                    state.clear()
                    state.update(snap)
                    idx1 = h_idx1
                    idx2 = h_idx2
                    day_started = True
                else:
                    # nothing in history — go back to character select
                    return "restart"
                continue
            history.append((pre_manna, idx1, idx2))

        # crisis check
        crisis = check_crisis(state)
        if crisis:
            play_event(crisis, state, [])
            day_started = False
            continue

        # pick event
        if state["calf_happened"]:
            ev = pool2[idx2 % len(pool2)]
        else:
            ev = pool1[idx1 % len(pool1)]

        pre_event = copy.deepcopy(state)
        went_back = play_event(ev, state, history, first_card=is_first_card)
        is_first_card = False

        if went_back:
            if history:
                snap, h_idx1, h_idx2 = history.pop()
                state.clear()
                state.update(snap)
                idx1 = h_idx1
                idx2 = h_idx2
                day_started = True
            else:
                return "restart"
            continue

        history.append((pre_event, idx1, idx2))
        if state["calf_happened"]:
            idx2 += 1
        else:
            idx1 += 1
        day_started = False

    screen_ending(state)
    return "done"


# ═══════════════════════════════════════════════════════════════════════════════
# ENTRY
# ═══════════════════════════════════════════════════════════════════════════════

def main():
    while True:
        screen_intro()
        char = screen_char_select()
        result = game_loop(char)

        if result == "restart":
            continue  # back to intro + char select

        print()
        raw = input("  [R = Play again | ^C = Quit]: ").strip().lower()
        if raw != "r":
            break

    print("\nShalom.\n")


if __name__ == "__main__":
    try:
        main()
    except (KeyboardInterrupt, EOFError):
        print("\nShalom.\n")
