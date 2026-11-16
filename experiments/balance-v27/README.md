# Cave Diamonds: upper-height research candidate

This is a non-release copy of V26 with a single new upper cave feature rule. The rule starts at Y=12..21, then searches up to 4 blocks for a floor, wall, or ceiling; all added cave neighbours stay at the same level or lower. The intended maximum newly placed ore height is Y=25. Existing V26 generation rules are unchanged. Pack hash: `f1ee6a1c0b23a8f4ffc33091fbc6ab8825d9d4366eb1990329e8b04eebaaf447`.

The package keeps V26's pack UUID and version because the isolated Bedrock test harness expects them. Do not activate it alongside V26 or in a played world. It has not been validated on a Realm or console.

The initial static JSON checks and 91 automated tests passed. Five small Bedrock test areas ran without reported content errors. Four ore blocks were observed above Y=16, in two connected pairs, all at Y=17. There is no observed ore near Y=25 yet. Those original scans counted air-adjacent groups only through Y=16, so the requested 10–15% more distinct cave finds cannot be assessed from them. The five areas are too small to establish a stable rate. No release or balance claim is made.

The five earlier scans are preserved under `results/` and use the old, incomplete upper-ore format. Their full-height cave group count is unavailable. The new diagnostic scan records neighbours for each upper ore. It combines Y=-64..16 and Y=17..40 before grouping, so veins crossing Y=16/17 are counted once. The first five paired comparisons under `full-height-results/` include fresh Vanilla and candidate scans. For further calibration, the project assumes Vanilla has no naturally generated diamond ore above Y=16 and reuses the frozen Vanilla reference; this avoids repeated Vanilla worlds. Keep those results in a separate directory, because the baseline source differs:

```sh
python3 -m tools.balance_batch run --pack experiments/balance-v27/behavior_pack --results experiments/balance-v27/full-height-results --full-height --limit 1
python3 -m tools.balance_batch status --pack experiments/balance-v27/behavior_pack --results experiments/balance-v27/full-height-results
python3 -m tools.balance_batch run --pack experiments/balance-v27/behavior_pack --results experiments/balance-v27/reference-baseline-results --full-height --reference-upper-empty --limit 1
```

This metric is still a technical count of air-adjacent connected ore blocks, not accessible cave finds or player yield. The packaged `.mcpack` is for inspection and disposable-world testing only.

## First complete-height comparison

The first five 4×4-chunk areas have now been remeasured with fresh Vanilla and V27 worlds. The combined Y=-64..40 metric counts 8 Vanilla and 17 V27 air-adjacent groups. All five Vanilla upper scans had no diamond ore in these areas. V27 had four upper ore blocks, all at Y=17 in two adjacent pairs; one block in each pair touched air. These two pairs contribute one group each. The small area's 212.5% group ratio is not a stable estimate of the desired 110–115%. The lower Y=-64..16 metric remains 15/8. There is still no observed ore near Y=25.

A larger calibration comparison uses the existing V24 large-area plan, which is **not** an independent V27 holdout:

```sh
python3 -m tools.balance_batch run --pack experiments/balance-v27/behavior_pack --results experiments/balance-v27/large-full-height-results --reference reference/balance-large-v24-1.26.61.1-2026-11-05.json --full-height --limit 1
python3 -m tools.balance_batch status --pack experiments/balance-v27/behavior_pack --results experiments/balance-v27/large-full-height-results --reference reference/balance-large-v24-1.26.61.1-2026-11-05.json

# For additional areas or later variants, reuse the frozen Vanilla reference:
python3 -m tools.balance_batch run --pack experiments/balance-v27/behavior_pack --results experiments/balance-v27/large-reference-results --reference reference/balance-large-v24-1.26.61.1-2026-11-05.json --full-height --reference-upper-empty --limit 1
```

The first 32×32-chunk area completed with fresh scans of both sides: 149 V27 air-adjacent groups against 94 Vanilla groups over Y=-64..40 (158.5%). The frozen Y=-64..16 Vanilla reference has 95 groups and the fresh lower scan has 94; this small world-generation difference is why the paired result uses 94. V27 had 49 upper ore blocks: Y=17/18/19/20/21 counts 11/11/13/8/6, with none at Y=22..40. This single previously selected calibration area exceeds the desired 110–115% interval and does not establish a global rate. V27 remains a rejected balance candidate and an unchanged research artifact.
