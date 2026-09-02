# E12-X1.11 Benchmark vs truebelief

Status: DIAGNOSTIC BENCHMARK, NO STRATEGY CHANGES

## Provenance

- Timestamp: `2026-08-28 12:58:20 +0200`
- Git branch: `main`
- Git commit: `4445aa0 Close E08 productive scale experiment`
- Working tree dirty: `True`
- Mode: `E12_Q0Q1_80K_ENGINE_X111`
- Submission SHA-256: `c5e42e237584ed006a68841c59d55ccd3d46799fb4254515cd33f6391637a30c`
- Local reproducibility: seed 0 `29858.0`, seed 421521921 `24827.0`
- truebelief replay source: `docs\101294736.json`
- truebelief replay SHA-256: `6281fdd32497c9db28e3d924ad8a55b12f841a5b1309164328679aa4f5ee8695`
- truebelief episode ID: `101294736`
- truebelief raw steps: `720`
- truebelief module version: `1.32.7`

The full truebelief Day 1 -> 30 timeline below is derived from the raw replay JSON. Raw replay days are indexed `0..29`; this report normalizes them to Day `1..30`.

## Final Result

| Agent | Seed | Final money | Owned quadrants | Peak active tiles | Peak workforce |
| --- | ---: | ---: | ---: | ---: | ---: |
| X1.11 local | 421521921 | `24827.00` | `2` | `27` | `4` |
| truebelief replay | 421521921 | `86297.00` | `2` | `50` | `12` |

- Absolute gap: `61470.00`
- Ratio truebelief / X1.11: `3.48x`
- X1.11 percent of truebelief: `28.8%`

## truebelief Day 1 -> 30 Timeline

| Day | Money | Delta | Quads | Hands | Crops | Pastures | Livestock | Weed | Crop mix | Market actions |
| ---: | ---: | ---: | --- | ---: | ---: | ---: | --- | ---: | --- | --- |
| 1 | `928` | `-2072` | NW | `5` | `21` | `4` | - | `0` | WHEAT:6, STRAWBERRY:7, MELON:8 | BUY_SEED:MELON=11; BUY_SEED:STRAWBERRY=10; BUY_SEED:WHEAT=18; HIRE=5 |
| 2 | `916` | `-12` | NW | `5` | `21` | `4` | - | `0` | WHEAT:6, STRAWBERRY:7, MELON:8 | HIRE=5 |
| 3 | `904` | `-12` | NW | `5` | `21` | `4` | - | `0` | WHEAT:6, STRAWBERRY:7, MELON:8 | HIRE=5 |
| 4 | `892` | `-12` | NW | `5` | `21` | `4` | - | `0` | WHEAT:6, STRAWBERRY:7, MELON:8 | HIRE=5 |
| 5 | `876` | `-16` | NW | `5` | `21` | `4` | - | `0` | WHEAT:6, STRAWBERRY:7, MELON:8 | BUY_ANIMAL:COW=1; HIRE=5; SELL:WHEAT=18 |
| 6 | `864` | `-12` | NW | `5` | `21` | `4` | - | `0` | WHEAT:6, STRAWBERRY:7, MELON:8 | HIRE=5 |
| 7 | `852` | `-12` | NW | `5` | `21` | `4` | - | `0` | WHEAT:6, STRAWBERRY:7, MELON:8 | HIRE=5 |
| 8 | `840` | `-12` | NW | `5` | `21` | `4` | - | `0` | WHEAT:6, STRAWBERRY:7, MELON:8 | HIRE=5 |
| 9 | `718` | `-122` | NW | `5` | `21` | `4` | - | `0` | WHEAT:6, STRAWBERRY:7, MELON:8 | BUY_ANIMAL:COW=1; BUY_SEED:WHEAT=4; HIRE=5; SELL:WHEAT=15 |
| 10 | `684` | `-34` | NW | `5` | `21` | `4` | COW:1 | `0` | WHEAT:6, STRAWBERRY:7, MELON:8 | BUY_PRODUCT:WHEAT=4; HIRE=5; SELL:WHEAT=3 |
| 11 | `1794` | `+1110` | NW,NE | `5` | `17` | `4` | COW:3 | `0` | WHEAT:6, STRAWBERRY:8, MELON:3 | BUY_ANIMAL:COW=5; BUY_LAND=1; BUY_PRODUCT:WHEAT=4; BUY_SEED:MELON=8; BUY_SEED:STRAWBERRY=11; BUY_SEED:WHEAT=22; HIRE=5; SELL:MELON=24 |
| 12 | `5223` | `+3429` | NW,NE | `6` | `22` | `9` | SHEEP:2, COW:6 | `0` | WHEAT:6, STRAWBERRY:11, MELON:5 | BUY_ANIMAL:COW=2; BUY_ANIMAL:SHEEP=5; BUY_PRODUCT:WHEAT=26; HIRE=6; SELL:FERTILIZER=1; SELL:MELON=24; SELL:STRAWBERRY=7 |
| 13 | `4969` | `-254` | NW,NE | `9` | `25` | `11` | SHEEP:3, COW:7 | `0` | WHEAT:1, STRAWBERRY:15, MELON:9 | BUY_PRODUCT:WHEAT=7; BUY_SEED:MELON=2; BUY_SEED:STRAWBERRY=1; HIRE=9; SELL:FERTILIZER=3 |
| 14 | `6515` | `+1546` | NW,NE | `10` | `37` | `11` | SHEEP:4, COW:7 | `0` | WHEAT:8, STRAWBERRY:19, MELON:10 | BUY_PRODUCT:WHEAT=14; HIRE=10; SELL:FERTILIZER=3; SELL:STRAWBERRY=7; SELL:WHEAT=10 |
| 15 | `6595` | `+80` | NW,NE | `10` | `39` | `11` | SHEEP:4, COW:7 | `0` | WHEAT:10, STRAWBERRY:19, MELON:10 | BUY_PRODUCT:WHEAT=11; HIRE=10; SELL:FERTILIZER=6 |
| 16 | `8326` | `+1731` | NW,NE | `9` | `39` | `11` | SHEEP:4, COW:7 | `0` | WHEAT:10, STRAWBERRY:19, MELON:10 | BUY_PRODUCT:WHEAT=11; HIRE=9; SELL:FERTILIZER=6; SELL:STRAWBERRY=7 |
| 17 | `8844` | `+518` | NW,NE | `10` | `39` | `11` | SHEEP:4, COW:7 | `0` | WHEAT:10, STRAWBERRY:19, MELON:10 | BUY_PRODUCT:WHEAT=11; HIRE=10; SELL:FERTILIZER=10; SELL:WHEAT=3 |
| 18 | `10810` | `+1966` | NW,NE | `10` | `39` | `11` | SHEEP:4, COW:7 | `0` | WHEAT:17, STRAWBERRY:12, MELON:10 | BUY_PRODUCT:WHEAT=11; BUY_SEED:WHEAT=4; HIRE=10; SELL:FERTILIZER=6; SELL:STRAWBERRY=7; SELL:WHEAT=7 |
| 19 | `17467` | `+6657` | NW,NE | `11` | `39` | `11` | SHEEP:4, COW:7 | `0` | WHEAT:17, STRAWBERRY:12, MELON:10 | BUY_SEED:WHEAT=2; HIRE=11; SELL:FERTILIZER=13; SELL:MILK=12; SELL:WHEAT=23; SELL:WOOL=11 |
| 20 | `24778` | `+7311` | NW,NE | `12` | `39` | `11` | SHEEP:4, COW:7 | `0` | WHEAT:17, STRAWBERRY:12, MELON:10 | BUY_PRODUCT:WHEAT=11; HIRE=12; SELL:FERTILIZER=8; SELL:MILK=21; SELL:WOOL=11 |
| 21 | `27587` | `+2809` | NW,NE | `10` | `37` | `11` | SHEEP:4, COW:7 | `0` | WHEAT:18, STRAWBERRY:12, MELON:7 | BUY_PRODUCT:WHEAT=11; BUY_SEED:WHEAT=2; HIRE=10; SELL:FERTILIZER=5; SELL:MILK=12; SELL:WHEAT=3 |
| 22 | `35307` | `+7720` | NW,NE | `12` | `34` | `11` | SHEEP:4, COW:7 | `0` | WHEAT:17, STRAWBERRY:12, MELON:5 | BUY_PRODUCT:WHEAT=11; BUY_SEED:WHEAT=14; HIRE=12; SELL:FERTILIZER=11; SELL:MELON=18; SELL:MILK=9; SELL:STRAWBERRY=1; SELL:WHEAT=11; SELL:WOOL=8 |
| 23 | `44125` | `+8818` | NW,NE | `11` | `31` | `11` | SHEEP:4, COW:7 | `0` | WHEAT:18, STRAWBERRY:12, MELON:1 | BUY_SEED:WHEAT=2; HIRE=11; SELL:FERTILIZER=10; SELL:MELON=18; SELL:MILK=11; SELL:STRAWBERRY=5; SELL:WHEAT=45; SELL:WOOL=4 |
| 24 | `53135` | `+9010` | NW,NE | `12` | `30` | `11` | SHEEP:4, COW:7 | `0` | WHEAT:18, STRAWBERRY:12 | BUY_PRODUCT:WHEAT=6; HIRE=12; SELL:FERTILIZER=11; SELL:MELON=24; SELL:MILK=9; SELL:STRAWBERRY=5; SELL:WHEAT=12; SELL:WOOL=12 |
| 25 | `57172` | `+4037` | NW,NE | `11` | `30` | `11` | SHEEP:4, COW:7 | `0` | WHEAT:18, STRAWBERRY:12 | BUY_PRODUCT:WHEAT=11; BUY_SEED:WHEAT=2; HIRE=11; SELL:FERTILIZER=10; SELL:MILK=9; SELL:STRAWBERRY=5; SELL:WHEAT=6 |
| 26 | `62344` | `+5172` | NW,NE | `11` | `30` | `11` | SHEEP:4, COW:7 | `0` | WHEAT:18, STRAWBERRY:12 | BUY_PRODUCT:WHEAT=11; BUY_SEED:WHEAT=14; HIRE=11; SELL:FERTILIZER=7; SELL:MILK=12; SELL:STRAWBERRY=5; SELL:WHEAT=6; SELL:WOOL=4 |
| 27 | `70890` | `+8546` | NW,NE | `11` | `30` | `11` | SHEEP:4, COW:7 | `0` | WHEAT:18, STRAWBERRY:12 | BUY_SEED:WHEAT=2; HIRE=11; SELL:FERTILIZER=10; SELL:MILK=12; SELL:STRAWBERRY=8; SELL:WHEAT=57; SELL:WOOL=8 |
| 28 | `77325` | `+6435` | NW,NE | `11` | `29` | `11` | SHEEP:4, COW:7 | `0` | WHEAT:18, STRAWBERRY:11 | BUY_PRODUCT:WHEAT=11; HIRE=11; SELL:FERTILIZER=10; SELL:MILK=12; SELL:STRAWBERRY=6; SELL:WHEAT=7; SELL:WOOL=8 |
| 29 | `85048` | `+7723` | NW,NE | `0` | `23` | `11` | SHEEP:4, COW:7 | `3` | WHEAT:15, STRAWBERRY:8 | SELL:FERTILIZER=8; SELL:MILK=15; SELL:STRAWBERRY=5; SELL:WHEAT=33 |
| 30 | `86297` | `+1249` | NW,NE | `0` | `16` | `11` | SHEEP:4, COW:7 | `7` | WHEAT:12, STRAWBERRY:4 | SELL:STRAWBERRY=1; SELL:WHEAT=9; SELL:WOOL=4 |

## X1.11 Timeline

| Day | Money | Quads | Hands | Crops | Pastures | Animals | Idle | Util | Crop mix |
| ---: | ---: | --- | ---: | ---: | ---: | ---: | ---: | ---: | --- |
| 1 | `2278` | NW | `1` | `9` | `0` | `0` | `16` | `0.36` | MELON:9 |
| 2 | `2277` | NW | `1` | `9` | `0` | `0` | `16` | `0.36` | MELON:9 |
| 5 | `2274` | NW | `1` | `9` | `0` | `0` | `16` | `0.36` | MELON:9 |
| 8 | `2271` | NW | `1` | `9` | `0` | `0` | `16` | `0.36` | MELON:9 |
| 10 | `2269` | NW | `1` | `9` | `0` | `0` | `15` | `0.36` | MELON:9 |
| 15 | `12038` | NW,NE | `3` | `26` | `0` | `0` | `23` | `0.52` | STRAWBERRY:17, MELON:9 |
| 20 | `12018` | NW,NE | `3` | `27` | `0` | `0` | `21` | `0.54` | STRAWBERRY:18, MELON:9 |
| 25 | `21303` | NW,NE | `3` | `27` | `0` | `0` | `21` | `0.54` | STRAWBERRY:27 |
| 29 | `24827` | NW,NE | `3` | `9` | `0` | `0` | `21` | `0.18` | STRAWBERRY:9 |

Note: the local environment's terminal observation for this run is indexed as Day 29/episode end; the final money shown above is the terminal X1.11 value.

## X1.9 -> X1.11 Evolution

| Version | Evidence | Final money | Gap vs truebelief | Ratio truebelief / ours |
| --- | --- | ---: | ---: | ---: |
| X1.9 | observed Kaggle replay | `6825.00` | `79472.00` | `12.64x` |
| X1.9 | local replay | `8714.00` | `77583.00` | `9.90x` |
| X1.11 | fresh local replay | `24827.00` | `61470.00` | `3.48x` |

X1.11 improves the local X1.9 reproduction substantially, but remains only about one third of the truebelief replay result.

## Terrain And Harvest

- X1.11 remains Q0+Q1 only and peaks at `27` productive crop tiles.
- truebelief remains Q0+Q1 only, reaches `50` productive tiles, and finishes with `16` crop tiles plus `11` pasture tiles.
- X1.9 historical audit bought Q2 and then left large areas idle; X1.11 avoids that specific capital sink.
- The remaining gap is not explained by Q2 waste; it is explained by much lower economic density and no visible high-yield livestock engine.

## Livestock

- X1.11 fresh replay: livestock spend `0.00`, active animals final `0`, milk revenue `0.00`.
- truebelief replay: active animals final `SHEEP:4, COW:7`, pasture tiles final `11`, shed residual `COW:2, SHEEP:1`.
- X1.9 historical audit: 8 cows, estimated milk revenue `2221.00`, estimated net livestock contribution `-5804.00`.
- The replay shows truebelief selling Milk, Wool, and Fertilizer repeatedly from Day 19 onward; X1.11 does not monetize livestock in the routed implementation.

## Dominant Gap Classification

| Impact | Gap source | Evidence |
| --- | --- | --- |
| PRIMARY | Sequencing and cash conversion | truebelief stays in Q0 through Day 10, buys Q1 on Day 11, then compounds from Day 19 onward; X1.11 reaches `24827` vs truebelief `86297`. |
| PRIMARY | Multi-engine portfolio | truebelief combines Wheat/Melon/Strawberry with Cow/Sheep, Milk/Wool/Fertilizer, and Wheat trading; X1.11 has `0` milk revenue. |
| MATERIAL | Workforce elasticity | truebelief repeatedly hires 9-12 total workers in mature days; X1.11 peaks at `4` effective workers. |
| SECONDARY | Q2 avoidance | X1.11 fixes X1.9 land over-expansion, but the ratio remains `3.48x` in favor of truebelief. |

## Top 3 Observable Differences

1. truebelief monetizes about `3.48x` more final cash than X1.11 on the same seed while also staying within Q0+Q1.
2. truebelief builds a livestock engine before expansion and sells Milk/Wool/Fertilizer from Day 19 onward; X1.11 has no livestock revenue path in the final routed implementation.
3. truebelief treats Wheat as both crop/feed/market commodity, including BUY_PRODUCT and SELL flows; X1.11 remains mainly a Melon/Strawberry crop cycle.

## Next Experiment Implication

Do not micro-tune X1.11. The next architecture needs the observable truebelief engine class: Day-1 dense mixed Q0, livestock before Q1, Q1 only after early monetization, elastic HIRE, and explicit cash conversion through crop + Milk + Wool + Fertilizer + Wheat market flows.
