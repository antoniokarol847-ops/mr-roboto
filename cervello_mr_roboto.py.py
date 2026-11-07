# ======================================================================
# MR. ROBOTO - RETRO ROBLOX 2010 EDITION - FINAL
# Build: 14 Marzo 2010 - Place Version: 1.0
# Creator: Builderman Fan - Guest 1337
# Descrizione: Chat bot che capisce le parole 
# ======================================================================
import random
import re
from collections import Counter

# ----------------------------------------------------------------------
# 1. DIZIONARIO RETRO - COME WIKIPEDIA 2010
# Ogni parola ha i suoi sinonimi, anche scritti male come si scriveva su Roblox
# ----------------------------------------------------------------------
DIZIONARIO_RETRO = {
    "freddo": ["freddo", "freddissimo", "fredd", "gelo", "ghiaccio", "congelare", "congelando", "brividi", "tremare", "brrr", "cold", "freezing", "frozen", "neve"],
    "caldo": ["caldo", "caldissimo", "afa", "sudare", "sudo", "sciogliere", "bollente", "fuoco", "hot", "sweat"],
    "fame": ["fame", "hungry", "mangiare", "pizza", "hamburger", "stomaco", "vuoto", "panino", "nom"],
    "triste": ["triste", "sad", "piangere", "piango", "magone", "depresso", "down", "tristezza", "cry"],
    "arrabbiato": ["arrabbiato", "rage", "arrabbiare", "incazzato", "urlare", "urlo", "gridare", "grido", "nervoso", "angry"],
    "stanco": ["stanco", "tired", "dormire", "sonno", "letto", "nanna", "esausto", "distrutto", "afk", "zzz", "sleepy"],
    "ciao": ["ciao", "salve", "hey", "hi", "yo", "oi", "fra", "fratm", "fratello", "bro", "buongiorno", "we", "ehi"],
    "grazie": ["grazie", "grazie mille", "ty", "tyvm", "thx", "thanks", "grazieee"],
    "epico": ["epico", "epik", "epikk", "epic", "mitico", "leggenda", "pro", "forte", "pwnage", "win", "awesome", "cool"],
    "vicini": ["vicini", "pianerottolo", "condominio", "casino", "rumore", "baccano", "urlano", "gridano", "lag", "spam", "noisy"],
    "inglese": ["inglese", "english", "england", "wait", "what", "not english", "non inglese"],
    "roblox": ["roblox", "place", "obby", "tycoon", "builderman", "guest", "bacon", "noob", "obby", "robux", "catalog", "spawn"],
    "musica": ["musica", "canzone", "audio", "suono", "song", "music", "radio"],
}

# Mappa inversa: ogni parola scritta -> concetto
PAROLA_A_CONCETTO = {}
for concetto, parole in DIZIONARIO_RETRO.items():
    for p in parole:
        PAROLA_A_CONCETTO[p] = concetto

# ----------------------------------------------------------------------
# 2. DATABASE - 100+ FRASI TIPO VECCHIO FORUM ROBLOX
# Più frasi ci sono, più capisce, come un mini-Google del 2010
# ----------------------------------------------------------------------
KNOWLEDGE = [
    # FREDDO
    ("freddo", "ho freddo sto congelando brrr"),
    ("freddo", "fa freddissimo fuori si gela"),
    ("freddo", "tremo dal freddo ho i brividi"),
    ("freddo", "che gelo fa oggi"),
    # CALDO
    ("caldo", "ho caldo sto sudando"),
    ("caldo", "che afa fa caldissimo"),
    ("caldo", "mi sto sciogliendo dal caldo"),
    # FAME
    ("fame", "ho fame voglio una pizza"),
    ("fame", "ho lo stomaco vuoto"),
    ("fame", "sono affamato da morire"),
    # TRISTE
    ("triste", "insert angry bird sad emoji"),
    ("triste", "ho voglia di piangere sono sad"),
    # ARRABBIATO
    ("arrabbiato", "sono arrabbiato voglio urlare"),
    ("arrabbiato", "sono in rage"),
    # STANCO
    ("stanco", "sono stanco morto voglio dormire"),
    ("stanco", "sono distrutto vado afk"),
    ("stanco", "ho sonno voglio andare a letto"),
    # CIAO
    ("ciao", "ciao fra come stai"),
    ("ciao", "oi fra come va"),
    ("ciao", "hey bro come stai"),
    ("ciao", "ciao fratello tutto bene"),
    # GRAZIE
    ("grazie", "grazie mille bro"),
    ("grazie", "tyvm sei un pro"),
    # EPICO
    ("epico", "oggi mi sento epico"),
    ("epico", "sono una leggenda mitico pro"),
    ("epico", "epic win sono fortissimo"),
    ("epico", "mi sento pro oggi"),
    # VICINI
    ("vicini", "i vicini gridano sul pianerottolo"),
    ("vicini", "c'è casino sul pianerottolo"),
    ("vicini", "i vicini fanno rumore"),
    # INGLESE
    ("inglese", "wait io non sono inglese"),
    ("inglese", "non parlo inglese"),
    ("inglese", "non sono inglese parlo italiano"),
    # ROBLOX
    ("roblox", "giochiamo a roblox"),
    ("roblox", "vieni nel mio place è epic"),
    ("roblox", "facciamo un obby"),
    ("roblox", "ho comprato bacon hair dal catalog"),
    ("roblox", "Builderman mi ha addato"),
    ("roblox", "sono Guest ma sono pro"),
]

# ----------------------------------------------------------------------
# 3. RISPOSTE IN PURO STILE 2010
# Con oof, xD, :D, :O, e tutto il resto
# ----------------------------------------------------------------------
RISPOSTE_RETRO = {
    "freddo": [
        "BRRR oof! Sei frozen! Vai vicino al fuoco dello spawn! xD",
        "oof che gelo! Compra hoodie da 10 robux dal catalog!",
        "Freddo lvl 9000! *trembling Guest face* xD"
    ],
    "caldo": [
        "OMG hot! Stai sciogliendo come noob in lava obby! xD",
        "Afa bestiale! Usa comando /e swim! xD"
    ],
    "fame": [
        "OMG fame lvl 9000! Vuoi pizza? Ho bloxy cola! xD",
        "Nom nom nom! *mangia bacon hair* xD"
    ],
    "triste": [
        "Oof D: Non sad! Sei pro! Ti regalo Guest hat! :3",
        "Nooo! *ti da cookie* Non essere triste! xD"
    ],
    "arrabbiato": [
        "WOAH! Calmo Guest! Non fare rage! xD",
        "Report spam! Niente flame nel mio place! >:O"
    ],
    "stanco": [
        "Oof tired! Vai afk! Io guardo il place! zzz...",
        "BRB! Vado a dormire sul letto di Roblox! xD"
    ],
    "ciao": [
        "Yo fra! Welcome to my place! Come va? :D xD",
        "Hi Guest! Vuoi essere mio friend? Addami! xD",
        "Ciao bro! Vuoi fare trade di face? xD"
    ],
    "grazie": [
        "np np! +rep! Sei pro! :D",
        "De nada fra! Addami come friend! xD"
    ],
    "epico": [
        "YOOOO EPIC WIN!!! :O Sei leggenda! Pro player! xD",
        "OMG EPIC! Hai sbloccato badge: Epic Guest! :D"
    ],
    "vicini": [
        "Oof che lag! I vicini fanno spam come noob! xD",
        "Pianerottolo = server pieno! Fai /e dance per ignorarli! xD"
    ],
    "inglese": [
        "Oof sorry! Io parlo ita + 2010 language: oof xD! 🇮🇹",
        "No english! Solo oof e xD! xD"
    ],
    "roblox": [
        "Roblox 2010 best game ever! xD Join my place!",
        "Bacon hair + Guest = epic combo! xD"
    ],
    "musica": [
        "Metto audio: Nyan Cat 10 hours! xD",
        "Radio place: Spooky Scary Skeletons! xD"
    ],
}

# ----------------------------------------------------------------------
# 4. MOTORE - CAPISCE LE PAROLE COME META AI MA RETRO
# ----------------------------------------------------------------------
def pulisci(testo):
    testo = testo.lower()
    testo = re.sub(r'[^a-z ]', ' ', testo)
    return testo.split()

def trova_concetti(parole_utente):
    trovati = Counter()
    for p in parole_utente:
        # Se la parola esiste precisa
        if p in PAROLA_A_CONCETTO:
            trovati[PAROLA_A_CONCETTO[p]] += 2
        # Se la parola contiene una keyword (per typo tipo fratmmm -> fra)
        for kw, concetto in PAROLA_A_CONCETTO.items():
            if len(kw) >= 3 and kw in p:
                trovati[concetto] += 1
    return trovati

def roboto_retro(msg):
    parole = pulisci(msg)
    concetti = trova_concetti(parole)

    print("\n" + "-"*40)
    print(f"[2009 Guest]: {msg}")

    if not concetti:
        print("[Mr.Roboto]: oof idk bro xD Non ho capito! D:")
        print("             Prova: ciao, freddo, caldo, fame, epico, roblox")
        print(f"[DEBUG 2010]: concetti=nessuno [0% oof]")
        return

    # Prende il concetto più votato
    concetto_migliore = concetti.most_common(1)[0][0]
    punteggio = concetti.most_common(1)[0][1]

    # Fix per il bug di prima: se parli inglese non deve dire che sei stanco
    if "inglese" in concetti and concetto_migliore == "stanco":
        concetto_migliore = "inglese"

    # Cerca frase simile nel database per debug
    best_frase = ""
    for c, frase in KNOWLEDGE:
        if c == concetto_migliore:
            best_frase = frase
            break

    risposta = random.choice(RISPOSTE_RETRO.get(concetto_migliore, ["oof xD"]))

    print(f"[DEBUG 2010]: capito come '{concetto_migliore}' -> {best_frase} [{punteggio*25}% oof]")
    print(f"[Mr.Roboto]: {risposta}")

# ----------------------------------------------------------------------
# 5. AVVIO - COME UN VECCHIO SERVER ROBLOX
# ----------------------------------------------------------------------
print("="*45)
print("ROBLOX - Mr.Roboto Place - 2010 Edition")
print("Server: 1/10 players - Version: 1.0")
print("Music: Playing... 'Welcome to the Club' - 2009")
print("Catalog: Bacon Hair - 0 Robux")
print("="*45)

# Test dei bug che hai trovato
roboto_retro("ciao fratm come staii xD?")
roboto_retro("oggi mi sento epikk")
roboto_retro("CIAO FRATMMM")
roboto_retro("wait io non sono inglese-")
roboto_retro("ho freddo brrr")
roboto_retro("join my place è epico")

print("\n" + "="*45)
print("Chatta! Scrivi: basta per uscire")
print("="*45)

while True:
    try:
        m = input("\n[Guest 1337]: ")
    except:
        break
    if m.lower().strip() in ["basta", "leave", "exit", "quit"]:
        print("[Mr.Roboto] has left the game. oof! xD")
        break
    roboto_retro(m)