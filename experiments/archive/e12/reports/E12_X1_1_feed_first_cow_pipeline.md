# E12-X1.1 — Feed-First Cow Pipeline (Engine Diagnosis & Single-Cow Bootstrap Gate)

## Summary & Objectives
E12-X1.0 established the 2×2 livestock core geometry `[(3,3), (3,4), (4,3), (4,4)]`, but collapsed economically (Mean Final Money: $6,227.60) due to unharvested WHEAT, starving cows, premature land expansion, and repeated hiring loops.
E12-X1.1 resolves this exact engine bottleneck by implementing a **Feed-First Cow Pipeline** with strict single-cow bootstrap gating and dedicated feed tile allocation.

## Key Changes & Architectural Decisions

1. **Feed-First Cow Bootstrap Gate**:
   - Cow #1 purchase is GATED until harvested WHEAT is available in shed (`wheat_shed >= 1`).
   - Cow #2..#4 purchases are GATED until Cow #1 has produced milk (`milk_harvested >= 1`) AND WHEAT buffer is positive (`wheat_shed >= 4`).
2. **Dedicated Feed Tile Ring**:
   - Reserved tiles `[(2,3), (2,4), (1,3), (1,4), (3,1), (4,1)]` for dedicated WHEAT cultivation.
   - Hand 1 plants and waters WHEAT daily on feed tiles.
3. **Capital Protection & Hire Loop Fix**:
   - Fixed repeated daily `HIRE` action bug by checking `current_hands < target_hands`.
   - Gated Q1 land expansion until Milk harvest/revenue is verified.
   - Preserved $150.00 operating cash float during ROI seed purchases.

## Telemetry Invariants & Verification Criteria
- `MILK` harvested > 0 units.
- Realized `MILK` revenue > $0.00.
- Zero premature cow starvation / zero repeated purchasing of dead cows.
