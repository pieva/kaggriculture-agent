# E12-X1.14 Implementation Delta

## Scope

Mode added: `E12_WORKFORCE_CAPACITY_X114`.

This was a fast build focused on Workforce Capacity First. It does not modify X1.12 behavior, does not enable Q2, and does not rebuild the standalone submission.

## Variants

- `A`: X1.12 baseline unchanged.
- `B`: preventive/aggressive HIRE with Q2 disabled.
- `C`: B plus crop maintenance priority.
- `D`: C plus livestock expansion brake.
- `E`: Q1-protected workforce capacity.
- `F`: E plus crop priority and livestock brake.

## Result

No variant beats X1.12 on both required seeds.

| Variant | Seed 0 | Seed 421521921 | Verdict |
|---|---:|---:|---|
| A | `$42,491` | `$48,313` | baseline |
| B | `$39,301` | `$36,238` | rejected |
| C | `$31,585` | `$35,537` | rejected |
| D | `$31,744` | `$35,654` | rejected |
| E | `$7,530` | `$6,177` | rejected |
| F | `$439` | `$496` | rejected |

## Interpretation

Workforce Capacity First improves some diagnostics, especially weed tile-days, but the tested variants lose too much economic conversion.

- B reduces weeds on required seeds from `137/129` to `21/21`, but suppresses Q1 on the required seeds and loses Sheep revenue.
- C/D reduce weeds to `6/6`, but crop priority creates too much travel/idle drag and blocks Sheep/Q1 value.
- E/F show that naive Q1 protection interacts badly with HIRE and livestock sequencing.
- B beats X1.12 on seed `1273000467` (`$54,228` vs `$43,021`), so the compact/land-discipline idea remains valuable, but it is not robust enough for Kaggle upload.

## Adoption

`E12_WORKFORCE_CAPACITY_X114` is `IMPLEMENTED` and `TESTED`, but not `ADOPTED`.

`X1.14 NO IMPROVEMENT: DO NOT UPLOAD`
