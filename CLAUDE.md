# القايلة (Al-Qayla) — project handoff for Claude

Owner: Mohammad (Kuwait). Reply ONLY in Arabic (Gulf dialect is fine). Never mix Arabic and English in one line.
He wants: step-by-step work, honest critique (no flattery), proactive advice on things he didn't think of, and every change
checked (screenshots) before reporting. Goal: a professional, polished, Gulf-heritage duel game (inspired by the old
iOS game "High Noon" in mechanics/feel only — never copy its name, art, sounds or code).

## Where things live
- Repo: github.com/ioxqox/alqayla (GitHub Pages). Live: https://ioxqox.github.io/alqayla/?v=NN (bump NN each release; last used 73).
- Claude can push directly (GitHub app installed). Commit as `Claude <noreply@anthropic.com>`.
- Plan & tracker doc (Claude Docs): https://claude.ai/code/artifact/a512277a-dd89-43db-aa94-a63e087aa06d
- Owner's PC (Windows, "killua", RTX 3080), mirror folder: `C:\Users\MA\Documents\MY PROJECT 2026\القايلة - ملفات اللعبة`
  (copy index.html + changed assets there after each release). Original ChatGPT art: `...\MY PROJECT 2026\الخلفيات الأصلية`.
  Source models/clips: `Young guy`, `Shayeb`, `Shanab`, `Sounds` folders in MY PROJECT 2026.

## Files in the repo
- `index.html` — the whole game (three.js r128 from cdnjs; GLTFLoader/SkeletonUtils from jsdelivr three@0.128.0). Save key `alqayla-v1` (localStorage).
- `hero.glb`, `shayeb.glb`, `shanab.glb` — Meshy-Lite characters rigged in Mixamo (clips: idle walk run die hit laugh aim pidle look). Clothing tint is a shader (tintHero) using baked `_GHUTRA`/`_NOTINT` vertex masks; iqal is a procedural double cord on the Head bone.
- `bg_fareej.jpg bg_souq.jpg bg_barr.jpg bg_sahel.jpg` — painted duel backdrops (BDROP table, `vp` = horizon height). `bg_lobby.jpg` — lobby "baraha" wall (LB table: zoom/gnd/par). `menu_art.jpg` — main menu & loading key art.
- `sfx_*.mp3`, `vox_*.mp3` (Kuwaiti taunts via ElevenLabs).
- `ui/` — polished UI kit cut from ChatGPT sheets (gray bg removed): btn_wood/red/green (used with CSS border-image classes `.kW .kR .kG`), panel_sadu (`.kP`), ribbon_sadu, btn_round, ic_* icons, coin, pearl, lock, ic_energy, ic_back, bar_empty (health/progress bars), bullet(_e), tiles, rank_* badges, trophy, stars, chests, `w_*.png` 7 weapon arts (+ `w_*_m.png` steel masks), `hol_*` animated holster cover, `c_*.png` clothing bases recoloured in code (clTint).
- `manifest.json`, `sw.js`, icons — installable PWA + fullscreen on first tap.

## Systems worth knowing
- Weapon finishes = full-body "camo" (camoGun): whole gun recoloured in polished metal, grip darkened, engraved pattern
  (swirl for silver/gold, Sadu diamonds for diamond tier & some special finishes; CAMO_P map). Tiers TIERS (kills/headshots), special finishes FIN (headshots).
  3D first-person revolver (rev.js code inside index.html: makeRevolver/makeFPHand) uses gunSteel/gunWood/gunWoodD + env reflections.
- Hub (weapons/clothes/shop) is stacked since v67: top bar (back, title, wallet pill with small +), preview stage on top (#hubShow spinning gun, or the 3D character placed by hubFit rays at 11%-41% of screen height with the camera pitched down), full-width sheet #hubR below with 3-column item cards (card2(): picture / name / footer strip, badges in corner).
- Lobby backdrop (LB): painting extended in a canvas (sky gradient above, mirrored sand below); k = size vs depth, base = wall-foot line below eye level. Characters stand on the sand in front, wall far behind.
- Balance (v68): NO power upgrades. gStat(id) returns the weapon's fixed base stats; old save.wg levels were refunded once (save.refund notice on the weapons list). Weapon screen tabs: المواصفات (wSpecs/specTable with ▲▼ vs equipped gun) · التقدم · الألوان. Next: customization slots (barrel 10 kills / grip 50 / action 200, sidegrades bought once with rupees), then a duel simulation to tune numbers so no weapon/loadout tops 55% wins. Design is in the plan doc.
- Controls (v69): direct-touch aiming removed — the game is played by phone motion. aimMode() = gyro, or finger-drag only if chosen or the device sends no motion (gyroSeen). MOT() = raise-to-draw only when the sensor really works (else the draw button shows). Raise-to-draw is on by default (save.motionV3 migration). First tap asks iOS for motion permission.
- Draw speed per weapon (WEAPONS.draw ms, gStat().draw): fard 0, naqsh 70, shotgun 150, fitil 240; shown as السحب in specs. Grip slot will trade stability vs draw speed (not aim speed).
- League badges (v73 set, ChatGPT): rank_bronze palm · rank_silver dallah · rank_gold mabkhara (green) · rank_pearl oyster+arch · rank_swords falcon (blue) · rank_legend khanjar+crown (red). Crown and red only on legend. lgBadge(i). Shown in the lobby banner (#bBadge) and results (league row, plus a promotion/demotion card computed from rating before/after).
- Chests (v71): claiming a wanted poster opens a small chest (openChest overlay #chestFx: closed chest shakes, then swaps to ui/*_open.png) and adds 1 to save.chestP; at CHEST_N=3 the sheikh's chest on the board (#bdChest) opens: rupees, 10-20 pearls, 30% chance of an unowned rupee-priced clothing item (bigLoot). Chests are earned only, never sold.
- Time of day (v72): each duel picks TOD noon 55% / maghrib 28% / night 17% (pickTod, setTod sets sun+hemi lights). Sunset is a colour-graded canvas copy of the noon painting (gradeTex). Night uses painted ChatGPT versions bg_*_n.jpg (bdNight), falling back to grading. Night: no sun, mirrors useless. Maghrib: low sun, mirror blinds 1.5x. Lobby/hub always noon.
- A global thin scroll hint (#scrollHint) appears on any scrolled list.
- Testing: Playwright + swiftshader in /home/claude/srv (copy index.html there, inject `window.__q=c=>eval(c);` before `function endLose(){`; do NOT copy sw.js into srv — it breaks local tests). Scripts t_audit.py (full flow), t45 (fight fx), t52 (weapons), t56 (clothes), t55 (holster).

## Roadmap status (see doc for the table)
1 bug fixes ✅ · 2 Pistol Strafe animation from Mixamo (waiting for owner to download "Pistol Strafe", Without Skin, 30fps) ·
3 painted backgrounds ✅ · UI kit ✅ · weapon art ✅ · clothing art ✅ · holster cover ✅ ·
4 3D weapons (better first-person revolver, Meshy) · 5 missing voice lines + music (ElevenLabs) ·
6 subscription month: redo characters/weapons/voices in full quality with commercial licences (Meshy free = CC BY, ElevenLabs free = non-commercial) ·
7 accounts + cloud save + split the single file · 8 friends test, then App Store / Google Play.

## Next steps (in order)
1. Owner tests v69 on phone (stacked hub, farther lobby wall, specs tab, motion-only controls, draw speed) and reports issues. Then balance step 2: customization slots.
2. Sunset/night done in v72 (graded). Later: new arena (dhow-building "النقعة"); real painted night versions from ChatGPT would look better than grading.
3. Store screenshots + icon from the new art.
4. Badges and chests done with final art (v73).
5. Known weak spots to be honest about: low-detail Meshy-Lite characters (fixed only in step 6), simple first-person gun, gray inside a few trigger guards.

## Working rules learned
- ChatGPT refuses detailed "firearm/sniper" prompts — describe guns as stylized cartoon game items/antique props.
- Ask ChatGPT for single sheets, no text, flat gray background; Claude cuts/keys them (better than ChatGPT slicing).
- Generate neutral/white bases and recolour in code instead of one image per colour.
- device_commit_files sometimes writes a stale snapshot: verify size with device_list_dir after copying.
