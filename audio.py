
import pygame

# Channel indices
MUSIC = 0       # global background music
AMBIENT = 1     # ambient loops (e.g., rain)
ENGINE = 2      # driving engine / other continuous loop
COOKING = 3     # frying loop
FX = 4          # short one-shot effects (stir, bite, UI pips)

_initialized = False

def init():
    global _initialized
    if _initialized:
        return
    # Mixer init should be called after pygame.init() in main
    # Reserve a few channels so indexing is stable
    pygame.mixer.set_num_channels(8)
    _initialized = True

def channel(idx: int) -> pygame.mixer.Channel:
    return pygame.mixer.Channel(idx)

def play_music(volume: float = 0.15):
    """Start quiet global background music looping forever."""
    init()
    try:
        music = pygame.mixer.Sound("resources/under_rian.ogg")
    except Exception as e:
        print("[audio] Failed to load background music:", e)
        return
    ch = channel(MUSIC)
    if not ch.get_busy():
        ch.play(music, loops=-1)
    ch.set_volume(volume)

def stop_all():
    """Stop all managed channels."""
    for idx in (MUSIC, AMBIENT, ENGINE, COOKING, FX):
        channel(idx).stop()
