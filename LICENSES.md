# Sources and licences

The lists in the packs were built from open data. Credit and licence for each source:

| Source | Used for | Licence |
|---|---|---|
| FrequencyWords (Hermit Dave, OpenSubtitles 2018) | words and their order by frequency | CC-BY-SA 4.0 |
| Hunspell ru_RU (LibreOffice, A. Lebedev) | filter: only real word forms are kept | BSD |
| Hunspell en_US (LibreOffice, SCOWL) | filter for `en_full.zip`: only real words are kept | SCOWL licence (permissive) |
| Hunspell ro_RO (LibreOffice, rospell) | filter for `ro_full.zip`: only real words are kept | GPL-2 / LGPL-2.1 / MPL-1.1 |
| Hunspell uk_UA (LibreOffice, spell-uk) | filter for `uk_full.zip`: only real words are kept | MPL 1.1 |
| Kyrgyz Wikipedia (ky.wikipedia.org, dump of 2026-11-01) | `ky_full.zip`: words, names and next words by frequency | CC-BY-SA 4.0 |
| Expressive Keyboard data | next-word pairs, typo fixes | MIT |

Because of CC-BY-SA 4.0, the packs are shared under **CC-BY-SA 4.0** too:
you may copy, change and share them, with credit, under the same licence.

`en_full.zip`, `ro_full.zip` and `uk_full.zip` (2026-11-22): FrequencyWords `en_full` / `ro_full` / `uk_full` words seen at least 10 times,
not in the app's built-in list, accepted by the Hunspell dictionary above (used only as a filter; no Hunspell
data is in the packs). For Ukrainian, words of the app's Russian list are left out (subtitles mix in Russian).

`ky_full.zip` (2026-11-27): words of the articles of Kyrgyz Wikipedia seen at least 4 times (about 84 000 words,
6 700 names written as inside sentences, e.g. Бишкек, АКШ) and up to 5 next words for 24 000 words. Russian words of
book references are left out unless they also take Kyrgyz endings (директор → директордун). Built by
`tools/ky_count.py` and `tools/ky_pack.py`. The Kyrgyz plugin of Multiling O is not used (not an open licence);
its dictionary can still be loaded in the app from the plugin's own .apk file.

> TODO: check this table against the build script of `ru_full.zip` (the original build folder was lost).
