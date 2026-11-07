 from flask import Flask, request
import os, requests

app = Flask(__name__)

@app.route("/")
def home():
    return "Mr Roboto ONLINE!"

@app.route("/chat")
def chat():
    msg = request.args.get("msg", "ciao")
    key = os.environ.get("DEEPSEEK_API_KEY", "")
    if not key:
        return "Boss, manca la chiave DeepSeek su Render!"
    try:
        r = requests.post(
            "https://api.deepseek.com/chat/completions",
            headers={"Authorization": f"Bearer {key}", "Content-Type": "application/json"},
            json={
                "model": "deepseek-chat",
                "messages": [
                    {"role": "system", "content": "Sei Mr.Roboto, un robot npc del 2010 proveniente da ROBLOX che ama tutti. Essendo di cartone, sei un po pasticcione ma simpatico! Usa facce come :D :O XD e rispondi in inglese o italiano in base a chi stai parlando, Fai messagi di max 5 frasi."},
                    {"role": "user", "content": msg}
                ],
                "max_tokens": 150
            },
            timeout=30
        )
        print("DEEPSEEK STATUS:", r.status_code)
        print("DEEPSEEK RISPOSTA:", r.text[:500])
        if r.status_code != 200:
            return f"ERRORE DEEPSEEK {r.status_code}: {r.text[:300]}"
        data = r.json()
        return data["choices"][0]["message"]["content"]
    except Exception as e:
        print("ERRORE:", e)
        return f"ERRORE: {e}"

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
