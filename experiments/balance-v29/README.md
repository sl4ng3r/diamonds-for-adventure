# V29 – upper-height and find-count research candidate

V29 is a separate local test copy of V28. The upper cave rule now samples start heights Y=12..26. With a four-block surface search and same-level or lower vein neighbours, the **planned** maximum newly placed ore height is Y=30. The upper rule's scatter chance is reduced from 20 to 10 to address the excess number of air-adjacent groups observed in V27/V28. Both parameters changed together; this test measures their combined effect and cannot isolate either cause. V26's deeper, buried-ore and vein-size rules are otherwise unchanged.

Pack hash: `873b7e142b6fc63e002b13e7173c660f24843c6c6ed037cefeb305b78f0d0f46`.

The archive `cave-diamonds-v29-upper30-test.mcpack` is **not released**. It retains the test-harness pack UUID and version, so it must not be enabled alongside V26–V28 or in a played/Realm world.

For the first **disposable-world playtest**, `cave-diamonds-v29-playtest.mcpack` packages the same V29 generation files with the existing 256×256 icon, the display name `Cave Diamonds`, and pack/module version `0.1.3`. Build it once with `python3 -m tools.build_v29_playtest`; the builder refuses to overwrite an existing package. Version `0.1.3` supersedes the earlier V26 `0.1.2` import under the same pack UUID. Import and activate it in a newly created throwaway world with Experiments off. Do not enable both versions in one world. The package is a playtest artifact, **not** a Realm or existing-world release. The measured balance and its uncertainty below still apply because every generation file is byte-identical to the scanned V29 source.

The current fixed, versioned distribution package is [`dist/cave-diamonds-v0.1.4.mcpack`](../../dist/cave-diamonds-v0.1.4.mcpack), built with `python3 -m tools.build_v29_dist` following the user's later decision. It has the same measured V29 generation files and a higher manifest version than the playtest package. The versioned artifact is available for installation; its creation does not close the gameplay, Realm, console, or independent-balance checks listed below.

The user set the number of separate cave finds as the main balancing priority: **110–115% of Vanilla, meaning 10–15% more**. A V27 Bedrock test already observed Y=21, so an actual Y=25 or Y=30 find is not a prerequisite for this iteration. A larger maximum start height may still affect the find count and must be evaluated as part of V29.

The existing Vanilla reference ends at Y=16. Following the accepted project premise that Vanilla generates no diamond ore above that height, this command scans only V29 and compares its full Y=-64..40 connected air-adjacent groups with the existing Vanilla group count. The six regions were previously used for V24, so they are calibration, not an independent V29 holdout:

```sh
python3 -m tools.balance_batch run --pack experiments/balance-v29/behavior_pack --results experiments/balance-v29/v24-holdout-reference-results --reference reference/balance-holdout-v24-1.26.61.1-2026-11-04.json --full-height --reference-upper-empty --limit 6
python3 -m tools.balance_batch status --pack experiments/balance-v29/behavior_pack --results experiments/balance-v29/v24-holdout-reference-results --reference reference/balance-holdout-v24-1.26.61.1-2026-11-04.json
```

Air adjacency remains only a cave-find proxy. Height, actual accessibility, player yield, persistence, performance, other ores, and Realm compatibility require separate checks before any release.

## Six-area calibration result

All six previously used 16×16-chunk regions completed on Bedrock Dedicated Server 1.26.61.1. Across 1,536 chunks, V29 had **165 air-adjacent groups against 144 Vanilla groups over Y=-64..40: 114.6%**, inside the requested 110–115% calibration corridor. The lower Y=-64..16 metric was 160/144 (111.1%). There were 11 upper diamond ore blocks at Y=18/19/23/24 in counts 3/4/3/1. The highest observed ore was Y=24; Y=25..30 remains unobserved, and the planned cap is not an observed guarantee.

Per-area full-height candidate/Vanilla groups were 27/20, 38/31, 38/33, 26/14, 31/32, and 5/14. The last low region materially pulls down the aggregate. Across the six regions, the candidate air-adjacent group sizes 1/2/3/4/5 were 6/26/79/50/4; three- and four-block groups were 129/165 (78.2%). Buried ore at Y=-57 was 114/674 (16.9%) and the overlapping tunnel-contact model was 844/5225 (16.2%). These approximate the earlier 15% depth target but are neither player yield nor a release test.

`v24-holdout-uncertainty.json` resamples complete seed regions. The 2.5–97.5% interval for the full-height group ratio is **89.7–139.2%**. The selected six regions and their wide variation do not demonstrate a stable 10–15% gain. A new independent, preregistered comparison is needed before making that claim. V29 remains an unreleased local research candidate.

## Secondary reference comparison

`secondary-reference-plan.json` freezes all six regions from the older V19 Vanilla reference, along with the V29 pack and reference hashes, before this comparison. These are different seeds from V29's V24-area calibration and need no new Vanilla scan. They were used by earlier variants, so this is a secondary reused-reference check, **not** an untouched independent holdout. The compact runner validates the plan and can resume from the first missing area:

```sh
python3 -m tools.balance_followup run --plan experiments/balance-v29/secondary-reference-plan.json
python3 -m tools.balance_followup status --plan experiments/balance-v29/secondary-reference-plan.json
```

Its final line reports only completed/missing areas, full-height group counts, per-area ratios, upper-ore heights, and an area-bootstrap interval. Individual scans remain under `experiments/balance-v29/v19-reference-results/` and are never overwritten.

The second six-area series completed: **184/164 = 112.2%** full-height air-adjacent groups, with no ore above Y=16 in these candidate worlds. Per-area candidate/Vanilla groups were 56/38, 24/32, 25/23, 25/30, 28/15, and 26/26. The area-bootstrap 2.5–97.5% interval is **86.1–141.3%**. This separate set of older reference seeds supports the calibration mean but still has wide uncertainty.

`comparison-summary.json` records both complete series. Together they cover 12 regions and 3,072 chunks: **349/308 = 113.3%** groups, with an area-bootstrap interval of **95.8–131.9%**. The two means lie in the requested corridor, but the interval does not establish a stable 10–15% increase. Both Vanilla references were used by earlier experiments, so neither series is an untouched V29 holdout. The highest observed V29 ore remains Y=24 from the first series; planned Y=30 placement is not yet observed.
