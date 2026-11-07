from flask import Flask, request
import os, requests
app = Flask(__name__)

DEEPSEEK_API_KEY = os.environ.get("DEEPSEEK_API_KEY")

def rispondi(msg):
    if not DEEPSEEK_API_KEY:
        return "Boss, manca la chiave DeepSeek su Render!"

    try:
        r = requests.post(
            "https://api.deepseek.com/chat/completions",
            headers={"Authorization": f"Bearer {DEEPSEEK_API_KEY}", "Content-Type": "application/json"},
            json={
                "model": "deepseek-chat",
                "messages": [
                    {"role": "system", "content": "Sei Mr.Roboto, un robot npc del 2010 proveniente da ROBLOX che ama tutti. Essendo di cartone, sei un po pasticcione ma simpatico! Usa facce come ":D" ":O" "XD" e rispondi in inglese o italiano in base a chi stai parlando, Fai messagi di max 5 frasi."},
                    {"role": "user", "content": msg}
                ],
                "temperature": 0.8
            },
            timeout=20
        )
        data = r.json()
        return data["choices"][0]["message"]["content"]
    except Exception as e:
        print("Errore DeepSeek:", e)
        return "Ops boss, DeepSeek ha lag... riprova!"

@app.route("/")
def home():
    return "Mr. Roboto + DeepSeek ONLINE!"

@app.route("/chat")
def chat():
    msg = request.args.get("msg", "ciao")
    return rispondi(msg)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
