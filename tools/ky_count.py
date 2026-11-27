"""Counts words and word pairs of Kyrgyz Wikipedia (articles only) for the ky_full pack.
Usage: ky_count.py <kywiki.xml.bz2> <out.json>"""
import bz2, re, sys, json, collections
import xml.etree.ElementTree as ET

src, out = sys.argv[1], sys.argv[2]
NS = '{http://www.mediawiki.org/xml/export-0.11/}'

WORD = re.compile(r"[а-яёңөүА-ЯЁҢӨҮ]+(?:-[а-яёңөүА-ЯЁҢӨҮ]+)*")
SENT = re.compile(r"[.!?\n:;()«»\"]+")


def strip(t):
    # templates (nested), tables, refs, comments, files, html, links → their text
    t = re.sub(r"<!--.*?-->", " ", t, flags=re.S)
    t = re.sub(r"<ref[^>]*/>", " ", t)
    t = re.sub(r"<ref.*?</ref>", " ", t, flags=re.S)
    for _ in range(6):
        n = re.sub(r"\{\{[^{}]*\}\}", " ", t)
        if n == t:
            break
        t = n
    t = re.sub(r"\{\|.*?\|\}", " ", t, flags=re.S)
    t = re.sub(r"\[\[(?:Файл|Сүрөт|File|Image|Категория|Category)[^\]]*\]\]", " ", t, flags=re.I)
    t = re.sub(r"\[\[[^\]|]*\|([^\]]*)\]\]", r"\1", t)
    t = re.sub(r"\[\[([^\]]*)\]\]", r"\1", t)
    t = re.sub(r"\[https?://[^\s\]]*\s?([^\]]*)\]", r"\1", t)
    t = re.sub(r"<[^>]+>", " ", t)
    t = re.sub(r"'{2,}", "", t)
    t = re.sub(r"^[=*#:;|!].*$", "\n", t, flags=re.M)  # headings, lists of links, table rows
    return t


words = collections.Counter()
lower = collections.Counter()
# spelling inside a sentence (not its first word): tells names (Бишкек, АКШ) from words
forms = {}
pairs = collections.Counter()
pages = 0
with bz2.open(src, "rb") as f:
    for ev, el in ET.iterparse(f, events=("end",)):
        if el.tag != NS + "page":
            continue
        ns = el.findtext(NS + "ns")
        text = el.findtext(f"{NS}revision/{NS}text") or ""
        el.clear()
        if ns != "0" or text.lstrip().lower().startswith(("#redirect", "#багыттама", "#перенаправление")):
            continue
        pages += 1
        for part in SENT.split(strip(text)):
            prev = None
            first = True
            for m in WORD.finditer(part):
                w = m.group(0)
                lw = w.lower()
                words[lw] += 1
                if not first:
                    f = forms.setdefault(lw, {})
                    f[w] = f.get(w, 0) + 1
                first = False
                if prev is not None:
                    pairs[prev + " " + lw] += 1
                prev = lw
print("pages", pages, "distinct words", len(words), "pairs", len(pairs))
best = {w: max(f.items(), key=lambda kv: kv[1])[0] for w, f in forms.items()}
json.dump({"words": words.most_common(), "best": best,
           "pairs": [p for p in pairs.most_common() if p[1] >= 3]},
          open(out, "w", encoding="utf-8"), ensure_ascii=False)
