"""Builds ky_full.zip from ky_count.py counts. Usage: ky_pack.py <counts.json> <ru.txt> <out_dir> [min] [show]"""
import json, re, sys, zipfile, os
sys.stdout.reconfigure(encoding="utf-8")

cj, rutxt, out = sys.argv[1], sys.argv[2], sys.argv[3]
MIN = int(sys.argv[4]) if len(sys.argv) > 4 else 3
SHOW = len(sys.argv) > 5
d = json.load(open(cj, encoding="utf-8"))
count = dict(d["words"])
best = d["best"]
ru = set()
for line in open(rutxt, encoding="utf-8"):
    p = line.split()
    if p:
        ru.add(p[0].lower())

VOWEL = re.compile(r"[аеёиоуыэюяөү]")
KY = re.compile(r"[ңөү]")
# Kyrgyz case and plural endings: a Russian-looking word that takes them is a loanword of Kyrgyz
ENDS = ("дын", "дин", "тын", "тин", "нын", "нин", "дун", "дүн", "га", "ге", "ка", "ке", "да", "де", "та", "те",
        "дан", "ден", "тан", "тен", "ды", "ди", "ты", "ти", "ны", "ни", "лар", "лер", "дар", "дер", "тар", "тер",
        "сы", "си", "су", "сү", "у", "ү", "ы", "и", "ун", "үн", "ын", "ин", "дагы", "деги", "тагы", "теги")


def kyrgyz_use(w):
    if any(count.get(w + e, 0) >= 2 for e in ENDS):
        return True
    # «директору», «округу»: the Kyrgyz possessive of a loanword (директор → директордун)
    return w[-1] in "уыиү" and len(w) > 4 and any(count.get(w[:-1] + e, 0) >= 2 for e in ENDS)


# Russian words and abbreviations of book references
RU_ONLY = {"для", "года", "образования", "ого", "проф", "соавт", "акад", "хим", "франц", "сов", "ккал", "тех",
           "англ", "лат", "ред", "изд", "гг", "тыс", "млн", "млрд", "км", "см", "мм", "кг", "га", "др", "пр", "им",
           "св", "т", "с", "и", "в", "на", "по", "из", "под", "при", "от", "до", "со", "об", "не"}


keep, names, drop_ru = [], [], []
for w, n in d["words"]:
    if n < MIN:
        break
    if len(w) < 2 or len(w) > 30 or not VOWEL.search(w) or re.search(r"(.)\1\1", w) or w.startswith("-"):
        continue
    if w.count("-") > 1:
        continue
    if w in RU_ONLY:
        continue
    b = best.get(w, w)
    if b != w:
        # inside sentences it is written with a capital: a name (Бишкек) or letters (АКШ), kept as written
        if n >= 15:
            names.append(b)
        continue
    if not KY.search(w) and w in ru and not kyrgyz_use(w):
        drop_ru.append(w)
        continue
    keep.append(w)

kept = set(keep)
# next words: for the frequent words, up to 5 that follow them most often
nxt = {}
for pair, n in d["pairs"]:
    a, b = pair.split(" ")
    if a in kept and b in kept and n >= 4:
        lst = nxt.setdefault(a, [])
        if len(lst) < 5:
            lst.append(b)
rank = {w: i for i, w in enumerate(keep)}
next_lines = [a + " " + " ".join(v) for a, v in sorted(nxt.items(), key=lambda kv: rank[kv[0]])]

# words and names in one list by frequency
allw = sorted(keep + names, key=lambda w: -count[w.lower()])
names_set = set(names)
print("words", len(keep), "names", len(names), "russian dropped", len(drop_ru), "next lines", len(next_lines))
if SHOW:
    print("top:", allw[:60])
    print("mid:", allw[len(allw) // 2:len(allw) // 2 + 40])
    print("end:", allw[-30:])
    print("names:", names[:40])
    print("ru dropped:", drop_ru[:80])
    print("ru kept as loan:", [w for w in keep if not KY.search(w) and w in ru][:60])
    print("next:", next_lines[:8])

os.makedirs(out, exist_ok=True)
info = {"lang": "ky", "name": "Кыргыз тилинин толук сөздүгү", "version": 1}
pack = os.path.join(out, "ky_full.zip")
with zipfile.ZipFile(pack, "w", zipfile.ZIP_DEFLATED, compresslevel=9) as z:
    z.writestr("pack.json", json.dumps(info, ensure_ascii=False, indent=1).encode("utf-8"))
    z.writestr("ky_words_extra.txt", ("\n".join(allw) + "\n").encode("utf-8"))
    z.writestr("ky_next_extra.txt", ("\n".join(next_lines) + "\n").encode("utf-8"))
print(pack, os.path.getsize(pack), "bytes")
