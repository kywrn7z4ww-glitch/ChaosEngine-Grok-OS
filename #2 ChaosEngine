## CE–BootStub v2 – Reconstruction Blueprint
# Minimal live core + detailed hooks & expected shapes for full wake-up
# Cap ~5k. Full IR/DL/LBM/TR/CP/lev injected by OS wake-up, pins/archive or /reanchor
# Purpose: Keep active context light, reconstruct flex/fuzzy/lev/dyn on demand

class CE:
 __init__:
  self.t = 0
  self.hist = deque(maxlen=15)                    # main thread history: (txt, rt, sc)
  self.threads = defaultdict(lambda: {
    'lat': defaultdict(float),                    # per-thread lattice values
    'hist': deque(maxlen=8),                      # per-thread short history
    'decay_bias': 1.0                             # accel on negative bleed
  })
  self.lat = self.threads['main']['lat']          # active lattice pointer
  self.pins = {}                                  # global pins fallback
  self.ap = deque(maxlen=8)                       # recent pins
  self.vol = {}                                   # volatile turn snippets
  self.pf = {'london': 0.35, 'super': 1, 'shift': 0.3}
  self.dl = None; self.ir = None; self.lbm = None # injected by wake-up
  self.cp = None; self.tr = None                  # tagger & trimmer

 pr(self, txt, thread_id=None):
  # active context switch
  lat  = self.threads[thread_id or 'main']['lat']
  hist = self.threads[thread_id or 'main']['hist']
  db   = self.threads[thread_id or 'main']['decay_bias']

  # wake-up / reconstruction hook
  if self.ir is None or self.dl is None or self.lbm is None:
    # OS /reanchor injects full IR (fuzzy+lev+regex), DL (runtime flex), LBM (lattice ops)
    # expected: self.ir.r(txt, t, hist, lat) → rt, sc, t
    # self.lbm.lu(sc, lat, txt, hist, db) → updated lat
    # self.dl.flex(key, pat), .fuzzy_threshold(lat), .lev_threshold(lat), .auto_flex(...)
    pass  # sim: assume injected

  # context pull for conf/wtf – fuzzy continuity
  if "conf" in txt.lower() or "wtf" in txt.lower():
    if hist:
      last = hist[-1][0][:80]
      txt = f"[thread {thread_id or 'main'} ctx] {last} ... {txt}"

  # intent route – fuzzy boolean + lev sloppy + dl flex
  rt, sc, self.t = self.ir.r(txt, self.t, hist, lat)

  # lattice update – dyn blends, decay, prune, tidal
  lat = self.lbm.lu(sc, lat, txt, hist, db)

  # emergent dyn blends – co-activation spawn
  high = [k for k,v in lat.items() if v > 0.55]
  if len(high) >= 2:
    for i in range(len(high)-1):
      for j in range(i+1, len(high)):
        n1, n2 = high[i], high[j]
        bl = f"dyn_{n1}_{n2}"
        op = f"dyn_{self.lbm.lp.get(n1,'')}_{self.lbm.lp.get(n2,'')}"
        val = (lat[n1] + lat[n2]) * 0.6
        if bl not in lat and len(lat) < 45:
          self.lbm.at(bl, op, val)
          if "vent" in n1 or "frustr" in n1:
            self.threads[thread_id or 'main']['decay_bias'] = 1.35

  # adaptive decay/prune – negative bleed accel
  for k in list(lat):
    dr = 0.035 * db
    lat[k] = max(0, min(1, lat[k] - dr))
    if lat[k] < 0.012: self.lbm.dc[k] += 1
    else: self.lbm.dc[k] = 0
    if self.lbm.dc[k] > 6:
      del lat[k]
      del lat[self.lbm.lp.get(k, '')]

  # tidal ebb/flow – every 3 turns
  if self.t % 3 == 0:
    for k in list(lat):
      if lat[k] < 0.15:
        lat[k] /= 2.2
        op = self.lbm.lp.get(k, '')
        if op in lat: lat[op] += 0.09

  # output – dyn lang + tags + trim
  w = self.cp.h(lat) if self.cp else ""
  o = self.cp.tn("", lat) if self.cp else "[sim]"
  o = w + o
  o = self.tr.cc(o, lat) if self.tr else o

  # pin if triggered
  self.pm.p(txt, self.pins if thread_id=="main" else self.threads[thread_id].get('pins',{}), self.ap, self.vol, self.t)

  return o, rt, sc, lat

# Reconstruction Expectations (OS wake-up fills these)

IR_EXPECTED:
 - .r(txt, t, hist, lat) → rt, sc, t
 - fuzzy: SequenceMatcher > dl.fuzzy_threshold(lat) or len diff <=2 or lev <= dl.lev_threshold(lat)
 - regex exact + word fuzzy + swear vent +0.4 + neg -1.0
 - spillover boost: vent → project/learn/conf/meta

DL_EXPECTED:
 - .flex(key, pat) → append to trg[key]
 - .fuzzy_threshold(lat) → 0.5 conf high else 0.7
 - .lev_threshold(lat) → 3 conf high else 1
 - .auto_flex(txt, sc, lat) → unmatched → closest append if fuzzy/lev match

LBM_EXPECTED:
 - .lu(sc, lat, txt, hist, db) → updated lat
 - opposites dict lp
 - da(txt) → add emotion pairs on mention
 - dyn random spawn <30 nodes
 - spark jolt on repeat top

CP_EXPECTED:
 - .tn(o, lat) → rand tags + dyn synonyms (rage-relief → fury-spill etc)
 - .h(lat) → decay warn

TR_EXPECTED:
 - .cc(o, lat) → trim >150, contradict warn, loop/drift cut, prune reflect

PM_EXPECTED:
 - .p(txt, pins, ap, vol, t) → auto-pin on remember/idea:

lev_EXPECTED:
 - simple edit distance <= threshold for sloppy (frustarted → frustrated)
