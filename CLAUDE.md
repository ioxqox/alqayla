# القايلة (Al-Qayla) — project handoff for Claude

Owner: Mohammad (Kuwait). Reply ONLY in Arabic (Gulf dialect is fine). Never mix Arabic and English in one line.
He wants: step-by-step work, honest critique (no flattery), proactive advice on things he didn't think of, and every change
checked (screenshots) before reporting. Goal: a professional, polished, Gulf-heritage duel game (inspired by the old
iOS game "High Noon" in mechanics/feel only — never copy its name, art, sounds or code).

## Where things live
- Repo: github.com/ioxqox/alqayla (GitHub Pages). Live: https://ioxqox.github.io/alqayla/?v=NN (bump NN each release; last used 81).
- Claude can push directly (GitHub app installed). Commit as `Claude <noreply@anthropic.com>`.
- Plan & tracker doc (Claude Docs): https://claude.ai/code/artifact/a512277a-dd89-43db-aa94-a63e087aa06d
- Owner's PC (Windows, "killua", RTX 3080), mirror folder: `C:\Users\MA\Documents\MY PROJECT 2026\القايلة - ملفات اللعبة`
  (copy index.html + changed assets there after each release). Original ChatGPT art: refs\chatgpt (older copies also in `...\MY PROJECT 2026\الخلفيات الأصلية`).
  Source models/clips: `Young guy`, `Shayeb`, `Shanab`, `Sounds` folders in MY PROJECT 2026.

## Files in the repo
- `index.html` — the whole game (three.js r128 from cdnjs; GLTFLoader/SkeletonUtils from jsdelivr three@0.128.0). Save key `alqayla-v1` (localStorage).
- `hero.glb`, `shayeb.glb`, `shanab.glb` — Meshy-Lite characters rigged in Mixamo (clips: idle walk run die hit laugh aim pidle look). Clothing tint is a shader (tintHero) using baked `_GHUTRA`/`_NOTINT` vertex masks; iqal is a procedural double cord on the Head bone.
- `bg_fareej.jpg bg_souq.jpg bg_barr.jpg bg_sahel.jpg` — painted duel backdrops (BDROP table, `vp` = horizon height). `bg_lobby.jpg` — lobby "baraha" wall (LB table: zoom/gnd/par). `menu_art.jpg` — main menu & loading key art.
- `sfx_*.mp3`, `vox_*.mp3` (Kuwaiti taunts via ElevenLabs).
- `ui/` — polished UI kit cut from ChatGPT sheets (gray bg removed): btn_wood/red/green (used with CSS border-image classes `.kW .kR .kG`), panel_sadu (`.kP`), ribbon_sadu, btn_round, ic_* icons, coin, pearl, lock, ic_energy, ic_back, bar_empty (health/progress bars), bullet(_e), tiles, rank_* badges, trophy, stars, chests, `w_*.png` 7 weapon arts (+ `w_*_m.png` steel masks), `hol_*` animated holster cover, `c_*.png` clothing bases recoloured in code (clTint).
- `refs/chatgpt/` — ALL original ChatGPT images at full resolution (arenas day+night, lobby, menu art, UI/weapon/holster/clothes sheets, badges, chests, icon); refs/README.md maps each to its game asset. Always add new ChatGPT originals here.
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
- v75 (owner's 18 notes): numbers in English digits via AR() (1,250 / 1.2M), fractions wrapped in LRI/PDI; new round icon set ui/ic_*.png (plus, map, shop, guns, clothes, trophy, wanted, settings, leagues, friends, speaker, x) used in drawer (8 items, 4x2), main menu, map button, wallet plus.
- Pages (.pg): #lgPage leagues ladder (openLeagues: current/next/locked, map each league unlocks) and #tlPage titles (openTitles: hero ribbon, next-title bar, rarity sections, cards). Old #career list no longer used.
- Maps belong to leagues: MAPS[].lg (fareej 0, souq 1, barr 2, sahel 3); mapOpen(m) uses league(save.best); maps opened before v75 kept via save.mapsOld.
- Lobby banner: level shown as a star medallion (no more "م"), rating with trophy icon, streak chip. Signs sit right above heads (y 1.98, scale .5); lobby camera farther (dz 3.7/asp, 7.4-11); lobby poses pidle/look.
- Backdrops are padded (extTex, BPAD) and world-anchored at eye 1.62 so the death fall never shows edges. Bottom safe area: CSS var --sb = max(safe-area, visualViewport overlap, 8px).
- UI sounds (v77): sfx_ui_{tap,tab,back,open,close,buy,err,equip,toggle}.mp3 rendered offline by /home/claude/sfxgen/gen.py (numpy); ui(kind) plays them; a global pointerdown handler classifies any clickable via uiKind() (buttons, onclick, cursor:pointer, back/tab/toggle). pay() plays buy/err; open* functions play open; equip on gun/clothes change. They follow the sound switch only (music separate).
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
3. Store art (v73+): store/store_1..6.jpg (1290x2796, framed in-game shots with Arabic captions) and store/feature_1024x500.jpg. Built by /home/claude/store/comp.py + fg.py. App icon done (v74, store/icon_1024.png; red sky, figure centred for Android circle crop).
4. Badges and chests done with final art (v73).
5. Known weak spots to be honest about: low-detail Meshy-Lite characters (fixed only in step 6), simple first-person gun, gray inside a few trigger guards.

## Working rules learned
- Every ChatGPT request goes on the owner's PC as a numbered folder: `القايلة - ملفات اللعبة\طلبات شات جي بي تي\NN <name>\` with `الأمر.txt` (UTF-8 BOM, the prompt) + `مرجع N - <file>.png` references. 01 = round icon sheet (pending).
- ChatGPT refuses detailed "firearm/sniper" prompts — describe guns as stylized cartoon game items/antique props.
- Ask ChatGPT for single sheets, no text, flat gray background; Claude cuts/keys them (better than ChatGPT slicing).
- Generate neutral/white bases and recolour in code instead of one image per colour.
- device_commit_files sometimes writes a stale snapshot: verify size with device_list_dir after copying.
- v76 (owner's notes after v75): maps unlock by league only (mapsOld removed, fixMap resets save.map); lobby sprite signs replaced by one HTML plate #lobTag over the selected character (clamped on screen), lobby camera farther (dz 9.2-13, LGAP 1.45); duel backdrop bottom mirror bug fixed (was overwriting the painting = the "paper" seam), #sky set to the painting's top colour so camera tilts never show an edge; padded backdrop textures built on demand, only 2 kept (bdFor); maghrib removed from rotation (noon 72% / night 28%), night lights brighter; mirror glare is a sun-flash centred on the enemy; smoothNormals() on character meshes (faceted look); portraits with gold bevel frames and softer light; polished metallic borders for titles/leagues cards, lock image without the white circle; level star number dark/engraved; banner subtitle wraps to 2 lines; انحاش uses ui/btn_round; big screens held sideways (foldables/tablets) run in a centred portrait column (html.lbx, AW/AH/AOX replace innerWidth/innerHeight, CSS vw -> var(--vw)).
- v77: shop icons are painted tiles (.shI with tile_wood/paper/pearl + coins, cloth art, shells/chest); clothes category tabs use tile frames and ui/star.png; .sw swatches glossy; lobby plate #lobTag uses btn_wood/red/green border-image (nemesis = darkened wood); leagues page = "مركزك" Sadu card (.lgMe: badge, points/best/wins, bar) + "سلّم الدوريات" ladder in wooden tile boxes, ascending from الفريج, no auto-scroll; taunt bubble uses btn_paper 9-slice with brass tail. ChatGPT request 02 = bishts done in v78: bs_brown/bs_black use ui/c_bisht_brown/black.png untinted; c_bisht_navy.png ready (item bs_navy mapped in clImgOf but not in CLOTHES yet — wait for the economy talk).
- Pending discussion with owner (do not build before he agrees): tools/items redesign (unlock by league, pros/cons, counters, new tools like the lasso flip) and monetization/economy.
- v79: owner likes the soft tap tone → ui() maps back/tab/toggle/open/close to 'tap' (one tone for every button; buy/err/equip stay). Smoke (المبخرة) used to wash the character white (fog colour = cream map fog, backdrop unfogged): now #smokeFx drifting haze overlay over everything + smoke-grey fog (night: blue-grey), html.nightTod class. اسحب/جاهز use .kR; انحاش uses ui/btn_round_red.png (btn_round with glossy red centre, made in PIL); in-duel tool buttons on tile_wood. Maps page: ribbon-framed titles (also .pgTop h2), league chip (.mLg) on each open map, gold frame + ribbon "المختارة" for the chosen map (#maps-scoped rules, older rules later in the CSS).
- Owner decisions (v79 talk): tool names must be plain everyday words (heritage stays in art/theme, not tool names). Monetization like League of Legends: cosmetics + battle pass only, never pay-to-win.
- v80: owner rejected the ribbon titles/tags on the maps page → page titles (#maps h2, .pgTop h2) are btn_wood plaques (::before border-image), map cards framed with tile_wood 9-slice (16px), chosen map = glow + btn_green "✓ المختارة" plaque, league chip + twist pills are btn_wood/btn_red/btn_green plaques. Leagues card (.lgMe) bar/text inset so they stay inside the Sadu frame.
- Owner APPROVED (v80): tools list with secret pick + reveal + 3s swap of one tool; exclusive premium gun collections (look + shot effect, no stats; kill camos stay earned-only); starter pack. Two tools replaced at his request: الصفارة الوهمية → النسخة الوهمية (decoy double, منظار exposes it), سدادات الأذن → التركيز (first second after draw in slow-motion for you, then hand shakes 2s). Build the tools system next.
- v81: UI kit edges cleaned (grey fringe → nearest inner colour, outer ring softened) for tile_*/btn_*/panel_sadu/ribbon/btn_round*/lock/star/ic_* (cache ?v=2). Wide frames use new ui/panel_wood|dark|paper.png (720x300, built from tile_* by tiling mirrored centre/edges, bottom edge = flipped top, slice 51) instead of stretching tile_*. Maps: info area is an embossed plate (.mi), chosen tag sits on the frame like "أنت هنا" (red pill), page-title plaques padded so text stays inside.
- Final tools (owner approved, v81 talk): الدرع، المرآة، النظارة الشمسية، قنبلة دخان، المنظار، الطلقة الخارقة، المراوغة (tilt phone to dodge one shot)، النفس العميق (hold phone still 1s → next shot perfectly steady)، الحبل، السكين، القنبلة الضوئية (+ القهوة heal). Slots 1/2/2/3/3/4 by league; secret pick, reveal, 3s swap.
- Owner showed Kammelna (بلوت) profile: trophy shelves with spotlights, multi-level medals (levels 1-5, goal pill, reward), calligraphy title emblems, soft cream pill buttons, blurred-backdrop modals. Plan: profile page "ملفي" with tabs الأوسمة / الألقاب / الجوائز; achievements with 5 levels (bronze→legend recolour of gold medals); titles rendered as real Arabic calligraphy font on generated empty plaques (AI garbles Arabic letters — never ask ChatGPT for Arabic text).
- ChatGPT requests on PC: 03 أيقونات الأدوات (12 round icons), 04 الأوسمة (12 gold Sadu-ribbon medals), 05 إطارات الألقاب (4 empty rarity plaques), 06 رف الجوائز (empty shelf with spotlights). All pending.
