# My Keyboard — dictionaries

Extra dictionaries ("full dictionaries") for the My Keyboard Android keyboard.

The built-in dictionary of the app stays as it is. A pack adds more words and word forms,
next-word suggestions and typo fixes on top of it.

## Install

**From the app (internet):** Settings → Словарь и подсказки → choose the language →
«📚 Полный словарь» → «⬇ Скачать полный словарь». The app downloads a pack only when you tap.
Nothing is checked in the background.

**Without internet:** download the `.zip` from `packs/` here, or get it from the forum or a friend.
Copy it to the phone, then tap «📂 Из файла» in the same place. «➕ Добавить из списка» recognises a
pack too.

Installing replaces the lists that were added earlier with «➕ Добавить из списка» for that language.
«Убрать полный словарь» removes it again.

## Packs

| Language | File | Version |
|---|---|---|
| Русский | `packs/ru_full.zip` | 1 |
| Українська | `packs/uk_full.zip` | 1 |
| English | `packs/en_full.zip` | 1 |
| Română | `packs/ro_full.zip` | 1 |
| Кыргызча | `packs/ky_full.zip` | 1 |

## Format (for people who make packs)

A pack is a `.zip` with:

- `pack.json`: `{"lang": "ru", "name": "Полный русский словарь", "version": 1}`
- any number of `.txt` lists (UTF-8). The app tells their kind by the content:
  - words: one word per line, frequent ones first;
  - next words: `word next1 next2 …`, or `word1_word2 next…` for two words before;
  - typo fixes: `typo right`.

`index.json` lists the packs the app can download:

```json
{"packs": [{"lang": "ru", "name": "…", "version": 1, "file": "packs/ru_full.zip",
            "size": 0, "sha256": "…"}]}
```

To publish a new version: put the new zip in `packs/`, raise `version` in its `pack.json`, then
update `version`, `size` and `sha256` in `index.json`. The app offers the update to people who have
an older version. It checks the SHA-256 after downloading.

## Sources and licences

See `LICENSES.md`.
