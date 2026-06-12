#!/usr/bin/env python3
import random
import sys

# ANSI color codes
GREEN  = "\033[42;30m"
YELLOW = "\033[43;30m"
GRAY   = "\033[100;37m"
RESET  = "\033[0m"
BOLD   = "\033[1m"
DIM    = "\033[2m"

WORDS = [
    "crane", "slate", "audio", "arose", "raise", "store", "stare", "snare",
    "spare", "share", "shame", "shale", "shake", "shade", "place", "plane",
    "plant", "plate", "blame", "blaze", "brave", "brace", "grace", "grade",
    "graze", "grape", "grave", "trace", "trade", "drape", "drive", "bride",
    "brine", "brite", "write", "white", "while", "whale", "phase", "chase",
    "chime", "crime", "prime", "price", "prize", "prose", "close", "clone",
    "clove", "globe", "glove", "grove", "grope", "groan", "grown", "brown",
    "drown", "crown", "frown", "prowl", "growl", "scowl", "shout", "stout",
    "trout", "snout", "scout", "clout", "cloud", "proud", "shroud", "grout",
    "light", "night", "sight", "right", "might", "fight", "tight", "blight",
    "fling", "cling", "bring", "sting", "thing", "swing", "sling", "ring",
    "think", "drink", "brink", "blink", "clink", "stink", "shrink", "rink",
    "black", "slack", "track", "crack", "smack", "snack", "stack", "knack",
    "frank", "blank", "clank", "plank", "spank", "stank", "thank", "drank",
    "flesh", "fresh", "press", "dress", "crest", "chest", "quest", "guest",
    "blest", "test", "blend", "spend", "trend", "front", "frost", "trust",
    "crust", "grump", "trump", "stump", "clump", "plump", "slump", "rump",
    "flood", "blood", "brood", "stood", "stool", "drool", "spool", "cool",
    "spoon", "croon", "groin", "loin", "oink", "point", "joint", "moist",
    "hoist", "built", "guilt", "quilt", "spilt", "stilt", "wilt", "jilt",
    "shelf", "smelt", "dwelt", "knelt", "melt", "spell", "dwell",
    "swell", "shell", "smell", "quell", "yell", "belle", "knell", "fell",
    "pixel", "level", "rebel", "novel", "camel", "gravel", "travel", "marvel",
    "panel", "canal", "final", "rival", "naval", "local", "vocal", "focal",
    "hotel", "model", "towel", "vowel", "bowel", "dote", "quote", "wrote",
    "float", "bloat", "boast", "coast", "roast", "toast", "moat", "goat",
    "saint", "paint", "faint", "quaint", "taint", "plaid", "braid", "raid",
    "maid", "said", "laid", "paid", "afraid", "blade", "made", "fade",
    "brave", "cave", "gave", "have", "nave", "rave", "save", "wave", "pave",
    "azure", "blush", "brush", "crush", "flush", "gush", "hush", "lush",
    "mush", "plush", "rush", "slush", "sushi", "cushy", "pushy", "mushy",
    "daisy", "dizzy", "fizzy", "fuzzy", "jazzy", "lazy", "hazy", "crazy",
    "jumpy", "lumpy", "bumpy", "dumpy", "grumpy", "humpy", "pumpy", "frumpy",
    "cloth", "broth", "froth", "sloth", "moth", "forth", "north", "worth",
    "sport", "short", "snort", "fort", "port", "sort", "tort", "wort",
    "stomp", "chomp", "romp", "pomp", "comp", "tromp",
]

# Deduplicate and keep only 5-letter words
WORDS = list({w for w in WORDS if len(w) == 5})


def score_guess(guess: str, target: str) -> list[tuple[str, str]]:
    target_chars = list(target)
    marked = [False] * 5

    # First pass: greens
    slots = []
    for i, (g, t) in enumerate(zip(guess, target)):
        if g == t:
            slots.append("green")
            marked[i] = True
        else:
            slots.append(None)

    # Second pass: yellows
    for i, g in enumerate(guess):
        if slots[i] is not None:
            continue
        for j, t in enumerate(target_chars):
            if not marked[j] and g == t:
                slots[i] = "yellow"
                marked[j] = True
                break
        if slots[i] is None:
            slots[i] = "gray"

    return list(zip(guess, slots))


def render_row(scored: list[tuple[str, str]]) -> str:
    parts = []
    for ch, color in scored:
        if color == "green":
            parts.append(f"{GREEN} {ch.upper()} {RESET}")
        elif color == "yellow":
            parts.append(f"{YELLOW} {ch.upper()} {RESET}")
        else:
            parts.append(f"{GRAY} {ch.upper()} {RESET}")
    return " ".join(parts)


def render_keyboard(guesses: list[list[tuple[str, str]]]) -> str:
    state: dict[str, str] = {}
    priority = {"green": 3, "yellow": 2, "gray": 1, None: 0}
    for row in guesses:
        for ch, color in row:
            if priority[color] > priority.get(state.get(ch), None):
                state[ch] = color

    rows = ["qwertyuiop", "asdfghjkl", "zxcvbnm"]
    lines = []
    for r in rows:
        parts = []
        for ch in r:
            color = state.get(ch)
            if color == "green":
                parts.append(f"{GREEN}{ch.upper()}{RESET}")
            elif color == "yellow":
                parts.append(f"{YELLOW}{ch.upper()}{RESET}")
            elif color == "gray":
                parts.append(f"{DIM}{ch.upper()}{RESET}")
            else:
                parts.append(ch.upper())
        lines.append(" ".join(parts))
    return "\n".join(lines)


def main():
    target = random.choice(WORDS)
    max_guesses = 6
    guesses: list[list[tuple[str, str]]] = []

    print(f"\n{BOLD}  W O R D L E{RESET}  —  Guess the 5-letter word in 6 tries\n")

    while len(guesses) < max_guesses:
        # Draw board
        for i in range(max_guesses):
            if i < len(guesses):
                print("  " + render_row(guesses[i]))
            else:
                print("  " + "  ".join([f"{DIM} _ {RESET}"] * 5))
        print()
        print(render_keyboard(guesses))
        print()

        remaining = max_guesses - len(guesses)
        try:
            guess = input(f"  Guess ({remaining} left): ").strip().lower()
        except (EOFError, KeyboardInterrupt):
            print(f"\n  The word was {BOLD}{target.upper()}{RESET}. Bye!\n")
            sys.exit(0)

        if len(guess) != 5:
            print("  Please enter a 5-letter word.\n")
            print("\033[F" * (max_guesses + 6))  # move cursor up to redraw
            continue
        if not guess.isalpha():
            print("  Letters only.\n")
            print("\033[F" * (max_guesses + 6))
            continue

        scored = score_guess(guess, target)
        guesses.append(scored)

        # Clear screen for clean redraw
        print("\033[2J\033[H", end="")
        print(f"\n{BOLD}  W O R D L E{RESET}  —  Guess the 5-letter word in 6 tries\n")

        if guess == target:
            for row in guesses:
                print("  " + render_row(row))
            messages = ["Genius!", "Magnificent!", "Impressive!", "Splendid!", "Great!", "Phew!"]
            print(f"\n  {BOLD}{messages[len(guesses)-1]}{RESET} You got it in {len(guesses)}!\n")
            return

    # Loss
    for row in guesses:
        print("  " + render_row(row))
    print(f"\n  The word was {BOLD}{target.upper()}{RESET}. Better luck next time!\n")


if __name__ == "__main__":
    main()
