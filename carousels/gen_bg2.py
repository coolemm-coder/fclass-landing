import os, json, base64, urllib.request
TOKEN = os.environ["OPENROUTER_API_KEY"]
URL = "https://openrouter.ai/api/v1/chat/completions"
IMGS = {
    "istanbul": "Cinematic vertical night view of Istanbul with Hagia Sophia and Blue Mosque silhouette, Bosphorus, deep navy blue sky, warm golden lights, luxury premium travel aesthetic, no text, no people",
    "barcelona": "Cinematic vertical view of Barcelona with Sagrada Familia silhouette at dusk, deep navy blue sky, warm golden lights, premium travel aesthetic, no text, no people",
}
def gen(name, prompt):
    body = json.dumps({"model":"google/gemini-2.5-flash-image","messages":[{"role":"user","content":prompt}],"modalities":["image","text"]}).encode()
    req = urllib.request.Request(URL, data=body, headers={"Authorization":f"Bearer {TOKEN}","Content-Type":"application/json","HTTP-Referer":"https://fclass.by"})
    with urllib.request.urlopen(req, timeout=80) as r:
        d = json.load(r)
    imgs = d.get("choices",[{}])[0].get("message",{}).get("images",[])
    if imgs:
        b64 = imgs[0]["image_url"]["url"].split(",",1)[1]
        open(f"bg/{name}.jpg","wb").write(base64.b64decode(b64))
        print(f"{name}: saved (${d.get('usage',{}).get('cost')})")
    else:
        print(f"{name}: no image - {d.get('error')}")
for n,p in IMGS.items(): gen(n,p)
print("done")
