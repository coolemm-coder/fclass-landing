import os, json, base64, urllib.request

TOKEN = os.environ["OPENROUTER_API_KEY"]
URL = "https://openrouter.ai/api/v1/chat/completions"

CITIES = {
    "cologne": "Cinematic vertical night view of Cologne Cathedral (Kölner Dom) and Hohenzollern bridge over Rhine river, deep navy blue sky, warm golden lights, luxury premium business travel aesthetic, moody atmospheric, no text, no people",
    "shanghai": "Cinematic vertical night skyline of Shanghai Lujiazui with Oriental Pearl Tower, deep navy blue sky, warm golden city lights reflecting on Huangpu river, luxury premium business travel aesthetic, no text, no people",
    "dusseldorf": "Cinematic vertical night view of Dusseldorf Medienhafen modern architecture and Rhine tower, deep navy blue sky, warm golden lights, luxury premium business travel aesthetic, moody, no text, no people",
}

def gen(name, prompt):
    body = json.dumps({
        "model": "google/gemini-2.5-flash-image",
        "messages": [{"role": "user", "content": prompt}],
        "modalities": ["image", "text"],
    }).encode()
    req = urllib.request.Request(URL, data=body, headers={
        "Authorization": f"Bearer {TOKEN}",
        "Content-Type": "application/json",
        "HTTP-Referer": "https://fclass.by",
    })
    with urllib.request.urlopen(req, timeout=80) as r:
        d = json.load(r)
    if "error" in d:
        print(f"{name}: ERROR {d['error']}")
        return
    imgs = d.get("choices", [{}])[0].get("message", {}).get("images", [])
    cost = d.get("usage", {}).get("cost", "?")
    if imgs:
        url = imgs[0].get("image_url", {}).get("url", "")
        b64 = url.split(",", 1)[1]
        open(f"bg/{name}.jpg", "wb").write(base64.b64decode(b64))
        print(f"{name}: saved (${cost})")
    else:
        print(f"{name}: no image")

for name, prompt in CITIES.items():
    gen(name, prompt)
print("done")
