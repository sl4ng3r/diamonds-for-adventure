# V33 – fewer visible cave diamonds

The player found too many diamonds in a large cave near Y=−40 with V29. The new balancing target is **110–115% of Vanilla's individual air-adjacent diamond ore blocks**, rather than 110–115% of connected air-adjacent groups. Air adjacency is still only a proxy for what a player can see and reach.

V29 had 819 versus 342 air-adjacent blocks in the twelve reused 16×16-chunk reference regions (239.5%). V30 wrapped the regular cave rules with a 45% scatter chance; V31 tested 15% in one area and was stopped after only 9 versus 21 air-adjacent blocks. V32 used 30% for all regular cave rules. V33 separates the rules: **20%** wrapper chance for the three deep rules and **60%** for the mid-height rule. V34 kept the deep setting and reduced the mid-height chance to 45%. The upper cave rule, buried-ore rules, and vein-size files remain byte-identical to V29 in V33. Scatter chances are engine parameters, not proven exact spawn probabilities.

| Variant | First six areas | Second six areas | Combined air-adjacent blocks | Y=−47..−32 combined |
| --- | ---: | ---: | ---: | ---: |
| V29 | 380/161 | 439/181 | 819/342 (239.5%) | 325/111 (292.8%) |
| V30 | 249/161 | not measured | — | — |
| V31 | 9/21, one area | not measured | — | — |
| V32 | 194/161 | 180/181 | 374/342 (109.4%) | 167/111 (150.5%) |
| **V33** | **193/161** | **186/181** | **379/342 (110.8%)** | **121/111 (109.0%)** |
| V34 | 171/161 | 158/181 | 329/342 (96.2%) | 111/111 (100.0%) |

V33's full Y=−64..40 height bands, individual series and pack hash are in `comparison-summary.json`. The combined area-bootstrap 2.5–97.5% interval for its air-adjacent block ratio is **95.0–125.9%**, so these reused calibration references do not establish a stable worldwide 10–15% gain. The six-plus-six seeds were used for older variants and were inspected while tuning V33. They are not an untouched holdout. No new Vanilla scans were run; the accepted project premise is that Vanilla has no natural diamond ore above Y=16.

The local experience can still differ: at Y=−15..−1, V33 has 87 versus 50 air-adjacent blocks; across the twelve regions it has only 167 versus 308 connected air-adjacent groups. This is fewer sites with more exposed blocks per site, which may feel too sparse between rich finds. At Y=−57, 226 versus 1,334 buried ore blocks (16.9%) and the overlapping tunnel model had 1,637 versus 10,823 contacts (15.1%). These are not measured player yields. The highest observed V33 ore remains Y=+24, and the planned +30 cap is unobserved.

The current fixed package is [`dist/cave-diamonds-v0.1.5.mcpack`](../../dist/cave-diamonds-v0.1.5.mcpack), built with `python3 -m tools.build_v33_dist`. Its generation files match this measured V33 source byte-for-byte. Version 0.1.5 is an installable package, not proof of Realm, console, old-world, or gameplay compatibility. Test it in a backed-up or disposable world first. Earlier generated chunks will not provide a clean comparison with newly generated chunks.

Reproduce the compact reports from the preserved results while their local raw scans under `data/research/` are available:

```sh
python3 -m tools.balance_followup status --plan experiments/balance-v33/calibration-plan.json
python3 -m tools.balance_followup status --plan experiments/balance-v33/secondary-plan.json
```

These plans validate the pack, Vanilla reference, seed list, and result hashes. A missing area can be resumed with `run` and the same plan. The source worlds and raw scans under `data/research/` are deliberately not committed, so a fresh clone has the recorded summary and result JSON but cannot recompute air exposure without the raw scans. Cave accessibility, real mining, persistence, performance, other ores, and Realm/console behavior remain separate checks.
