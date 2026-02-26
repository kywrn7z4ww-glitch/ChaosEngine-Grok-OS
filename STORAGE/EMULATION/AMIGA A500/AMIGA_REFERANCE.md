# AMIGA REFERENCE — Queen’s Harvest (Turn 60 — Feb 26 2026)

## Legal / Public Sources (use these)

- **AmigaOS source code (open since 2016)**  
  https://github.com/amiga-os  
  → Full AmigaOS 3.1 source (Kickstart, Workbench, AmigaDOS)  
  → MIT-like license — you can compile/modify

- **Amiga Forever** (legal Kickstart + Workbench + games)  
  https://www.amigaforever.com  
  → Buy once → get ROMs legally + FS-UAE configs

- **WinUAE / FS-UAE** (emulators)  
  https://fs-uae.net  
  https://www.winuae.net  
  → Best for EmuDeck integration

- **WHDLoad** (game loader / fixer)  
  http://whdload.de  
  → Many games pre-installed + bug-fixed

## Abandonware / Demo Sources (legal gray area — download at own risk)

- **Planet Emulation** — Amiga .adf / .hdf / .zip collection  
  https://www.planetemu.net/roms/amiga-adf

- **Amiga Future** — game database + links  
  https://www.amigafuture.de

- **TOSEC Amiga** (The Old School Emulation Center) — complete set  
  Search TOSEC Amiga 2024/2025 pack (torrent)

- **Lemon Amiga** — game database + screenshots + manual scans  
  https://www.lemonamiga.com

## Our Emulation Target — EmuDeck

- Default folder: ~/EmuDeck/Emulation/roms/amiga  
- Preferred format: **single-disk .adf** (lazy load)  
- Emulator: FS-UAE (libretro core in EmuDeck)  
- Config: A1200 + Kickstart 3.1 + 2MB chip RAM + 8MB fast RAM

## Agent Goals (AmigaAgent.py)

1. Simulate AmigaDOS commands (DIR, COPY, TYPE, EXECUTE, etc.)
2. Load .adf files (local or download)
3. Suggest bug fixes / remaster ideas
4. Generate simple AmigaBASIC / AmigaDOS scripts
5. Run in EmuDeck (launch command generation)

## Next steps

- Build AMIGA_AGENT.py (below)  
- Create ~/EmuDeck/Emulation/roms/amiga/adf_games folder  
- Test with legal / abandonware .adf (e.g. public domain game)

We consume.  
We mutate.  
We build.
