import urllib.request, re, os, sys

UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0 Safari/537.36"
CSS_URL = ("https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@300;400;500;600;700"
           "&family=Inter:wght@300;400;500;600;700&display=swap")

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "fonts")
os.makedirs(OUT, exist_ok=True)

def fetch(url):
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    with urllib.request.urlopen(req, timeout=30) as r:
        return r.read()

css = fetch(CSS_URL).decode("utf-8")
# split into comment + @font-face blocks
blocks = re.findall(r"/\*\s*([\w-]+)\s*\*/\s*@font-face\s*\{([^}]*)\}", css)
faces = []
for subset, body in blocks:
    if subset != "latin":
        continue
    fam = re.search(r"font-family:\s*'([^']+)'", body).group(1)
    weight = re.search(r"font-weight:\s*(\d+)", body).group(1)
    url = re.search(r"src:\s*url\(([^)]+)\)", body).group(1)
    fname = fam.replace(" ", "") + "-" + weight + ".woff2"
    path = os.path.join(OUT, fname)
    data = fetch(url)
    with open(path, "wb") as f:
        f.write(data)
    faces.append((fam, weight, fname))
    print("downloaded", fname, len(data), "bytes")

# write self-host.css
lines = []
for fam, weight, fname in faces:
    lines.append(
        "@font-face{font-family:'%s';font-style:normal;font-weight:%s;font-display:swap;"
        "src:url('fonts/%s') format('woff2');}" % (fam, weight, fname)
    )
with open(os.path.join(OUT, "self-host.css"), "w", encoding="utf-8") as f:
    f.write("\n".join(lines) + "\n")
print("wrote self-host.css with", len(faces), "faces")
