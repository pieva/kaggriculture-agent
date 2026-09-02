# Benchmark Registry

Analysis-only registry built from raw Kaggriculture replay JSON files in `docs/benchmark`.

| Episode | Seed | Competitor | Our reward | Competitor reward | Gap | Ratio | Q2 competitor | Final quadrants | Livestock | Peak hands | Peak crop | Peak productive | Weed tile-days | Main sells | SHA-256 |
|---|---:|---|---:|---:|---:|---:|---|---|---|---:|---:|---:|---:|---|---|
| 101294736 | 421521921 | truebelief | 6825 | 86297 | 79472 | 12.644 | no | NW,NE | COW:9, SHEEP:5 | 12 | 39 | 50 | 10 | WHEAT:268, FERTILIZER:138, MILK:134, MELON:108, WOOL:70 | `6281fdd32497c9db28e3d924ad8a55b12f841a5b1309164328679aa4f5ee8695` |
| 101705751 | 1056561958 | Dr. Mikholae Hutchinson | 38815 | 90137 | 51322 | 2.322 | no | NW,NE | COW:7, GOOSE:2, SHEEP:4 | 10 | 30 | 46 | 11 | FERTILIZER:208, MILK:161, STRAWBERRY:132, WHEAT:109, EGG:71 | `79be341c03a5f471baaa28cf6419ff89d85c06fc88de50901c5c1e3da92ac6b3` |
| 101717011 | 1273000467 | Alexander Sokolov | 24314 | 50420 | 26106 | 2.074 | no | NW | COW:4, SHEEP:2 | 8 | 9 | 15 | 145 | WHEAT:756, MILK:129, FERTILIZER:69, CARROT:59, WOOL:52 | `f298356ebe1bf9e7aad4acff32a6114db4f015f90f613e8e913565913494f3b9` |

## Notes

- Episode 101294736: truebelief reaches 86297 vs 6825; Q2=no; peak hands 12; peak crop/productive 39/50; livestock {"COW":9,"SHEEP":5}; weed tile-days 10. Our side peak hands 8, peak crop/productive 26/34, weed tile-days 19.
- Episode 101705751: Dr. Mikholae Hutchinson reaches 90137 vs 38815; Q2=no; peak hands 10; peak crop/productive 30/46; livestock {"COW":7,"GOOSE":2,"SHEEP":4}; weed tile-days 11. Our side peak hands 9, peak crop/productive 21/30, weed tile-days 158.
- Episode 101717011: Alexander Sokolov reaches 50420 vs 24314; Q2=no; peak hands 8; peak crop/productive 9/15; livestock {"COW":4,"SHEEP":2}; weed tile-days 145. Our side peak hands 9, peak crop/productive 23/32, weed tile-days 140.
