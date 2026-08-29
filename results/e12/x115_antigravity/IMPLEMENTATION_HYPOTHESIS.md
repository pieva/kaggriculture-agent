# E12-X1.15-ANTIGRAVITY — Implementation Hypothesis & Architectural Design

## 1. Competitive Evidence Base (6 Replays)

### Primary Evidences Used:
1. **Day 1 Livestock Opening** (*OBSERVED* in `101462495`, `101761797`, `101891362`, `101717011`):
   - All top competitors buy 2–3 Cows and 1–2 Sheep on Day 1 Turn 1 along with 4–6 Hands.
2. **Fast 3-Quadrant Expansion (Q0 $\rightarrow$ Q1 $\rightarrow$ Q2)** (*OBSERVED* in 6/6 top runs):
   - Q1 is unlocked on Day 5–6 (~$500 cash); Q2 is unlocked on Day 8–10 ($500–$2,000 cash).
3. **75-Tile Physical Footprint Saturation** (*OBSERVED* in `101462495`, `101761797`, `101891362`):
   - Peak productive surface reaches 75 tiles (maximum possible across 3 quadrants).
4. **Herds of 12–15 Cows and 2–6 Sheep** (*OBSERVED* in 6/6 top runs):
   - Livestock generates 54%–64% of total revenue ($84k–$107k in milk/wool/fertilizer).
5. **High Sustained Workforce (Peak 12, Mean 10 Hands)** (*OBSERVED* in 6/6 top runs):
   - Ramping workforce aggressively from Day 1 to service the 75-tile surface.
6. **Task Priority Over Weed Digging** (*OBSERVED & CAUSAL* from X1.14 counterfactual):
   - Milking, shearing, fertilizing, harvesting, and watering strictly precede weeding.
7. **Endgame Continuity** (*OBSERVED* in top runs):
   - Hands are kept active through Day 30 to complete milking/harvesting cycles; planting stops on Day 26.

---

## 2. Hypothesis & Architectural Strategy

### Core Thesis:
X1.12 was bottlenecked by three structural constraints:
1. **Delayed livestock ramp** (Cow Day 5, Sheep Day 12, capped at 7/4) which delayed milk/wool compounding.
2. **2-quadrant spatial ceiling** (50 tiles max, where pasture and crops competed for limited space).
3. **Underpowered early workforce** (5 hands through Day 10) which slowed early cash velocity.

### Architectural Blueprint (`E12_X115_ANTIGRAVITY_INDEPENDENT`):
- **Day 1**: Buy 5 Hands, 2 Cows, 2 Sheep, 6 Melon, 6 Strawberry, 6 Wheat seeds + 4 Wheat feed. Build 4 pastures immediately.
- **Days 2–5**: Maintain crop watering/planting + milk/feed livestock. Accumulate ~$500 for Q1.
- **Day 5–6 (Q1 Expansion)**: Unlock Q1 as soon as cash reaches threshold ($500–$1,000). Expand crop footprint to 35–40 tiles.
- **Day 8–10 (Q2 Expansion)**: Unlock Q2 as soon as cash reaches threshold ($500–$1,000). Expand to full 75-tile footprint (up to 55 crops + 16–20 pastures).
- **Livestock Scaling**: Scale herd to 10–14 Cows + 3–5 Sheep as pastures are constructed in Q1/Q2.
- **Workforce Scaling**: Day 1: 5 hands, Day 5: 8 hands, Day 8: 10 hands, Day 10+: 12 hands. Maintained through Day 30.
- **Task Hierarchy**:
  1. Shed deposit
  2. Milk / Wool / Fertilizer collection
  3. Animal Feeding & Care
  4. Crop Harvesting
  5. Crop Watering
  6. Pasture Building & Crop Planting
  7. Weed Digging (lowest priority)
- **Market Policy**:
  - Instant sell of all shed goods (Milk, Wool, Fertilizer, Melons, Strawberries, Carrots, Tomatoes).
  - Dynamic feed buffer: maintain `max(8, animal_tiles * 3)` wheat without redundant buy/sell cycles.

---

## 3. Overfitting Risks & Safeguards

1. **Risk of Early Bankruptcy on Day 1**: Buying 2 Cows + 2 Sheep + 5 Hands + seeds costs ~$2,800 out of $3,000 starting cash.
   - *Safeguard*: Carefully budget Day 1 opening to leave a minimum cash buffer ($100–$200) for worker wages on Day 2.
2. **Risk of Feed Starvation**: Large herds require daily wheat feed.
   - *Safeguard*: Maintain dedicated wheat crop tiles + proactive feed buying if shed wheat drops below 8 units.
3. **Risk of Premature Q2 with High Backlog**: Expanding to Q2 without enough workers to maintain Q0+Q1.
   - *Safeguard*: Ensure at least 8 hands and active livestock cash flow before triggering Q2 purchase.
