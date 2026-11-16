# V28 – throttled upper-height research candidate

V28 copies V27 and changes only the new upper cave rule: it routes that rule through `cave_upper_chance`, a scatter feature with one placement attempt and `scatter_chance: 20`. The intended effect is to keep roughly one fifth of V27's added upper-rule attempts. This is a hypothesis, not a measured effect. The existing V26 depth, buried-ore and vein-size rules remain byte-identical to V27. The planned maximum newly placed ore height remains Y=25.

Pack hash: `f98ad176b7951745345e6b59a1bfa7ef009498171698305558667bfe2664d2a2`.

The packaged `.mcpack` is a local test artifact only. Its pack UUID and version match V26/V27 for the isolated test harness, so it must not be activated alongside those packs. No Realm or gameplay approval is implied.

The project assumes Vanilla has no naturally generated diamond ore above Y=16. The following command scans only V28 and compares the combined Y=-64..40 candidate group count with the existing Y=-64..16 Vanilla reference. The assumption and baseline source are recorded in each result. Use a new result directory for each pack and reference:

Current priority is the number of distinct air-adjacent groups. A measured Y=21 occurrence in V27 already improves on the first Y=17 observations. Raising the planned upper placement limit to Y=30 is an optional later experiment, not part of V28; it could also change group counts and would require its own measurement.

```sh
python3 -m tools.balance_experiment scan --pack experiments/balance-v28/behavior_pack --results experiments/balance-v28/large-reference-results --reference reference/balance-large-v24-1.26.61.1-2026-11-05.json --index 0 --full-height --reference-upper-empty
python3 -m tools.balance_batch status --pack experiments/balance-v28/behavior_pack --results experiments/balance-v28/large-reference-results --reference reference/balance-large-v24-1.26.61.1-2026-11-05.json
```

This is a reused calibration region, not an independent holdout. Air adjacency does not prove cave access or player yield. Further balance, persistence, performance, and Realm tests remain open.

## First engine result

The first 32×32-chunk calibration region produced 127 full-height air-adjacent V28 groups against 95 in the frozen Vanilla reference (133.7%). The lower-only comparison was 119/95 (125.3%). V27 produced 149/94 in a freshly paired comparison of the same seed and chunk range; the Vanilla group count varied by one between the older reference and the fresh world. V28 had 27 upper ore blocks, at Y=17/18/19/20 in counts 3/9/5/10, with none at Y=21..40. This confirms some reduction from V27 but does not establish the global 110–115% goal.

The next calibration step uses the six 16×16-chunk regions from the older V24 holdout. Those seeds have already been used for previous variants, so they are **not** an independent V28 holdout:

```sh
python3 -m tools.balance_batch run --pack experiments/balance-v28/behavior_pack --results experiments/balance-v28/v24-holdout-reference-results --reference reference/balance-holdout-v24-1.26.61.1-2026-11-04.json --full-height --reference-upper-empty --limit 6
python3 -m tools.balance_batch status --pack experiments/balance-v28/behavior_pack --results experiments/balance-v28/v24-holdout-reference-results --reference reference/balance-holdout-v24-1.26.61.1-2026-11-04.json
```

The user redirected the work toward a possible Y=30 upper limit and the number of distinct finds. This six-area V28 run was stopped after four complete areas; the partial results remain untouched. Across those four selected areas, V28 had 123/98 full-height air-adjacent groups (125.5%) and two upper ore blocks, both at Y=19. This is a partial calibration result, not a final six-area estimate.
