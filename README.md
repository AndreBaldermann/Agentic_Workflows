# LangChain Agent mit Llama 3.1:8b

Dieser Agent fragt dich beim Start nach deinem Wunschtext (inkl. optionalem Wertebereich),
ruft dann über Llama ein Zufallszahl-Tool auf und gibt alle 10 Sekunden das formulierte Ergebnis aus.

## Verhalten

- Du gibst einen Prompt ein, z. B. `Ich will eine Zufallszahl von 10 bis 50`.
- Wenn kein Wertebereich angegeben ist, wird automatisch **0 bis 100** verwendet.
- Llama ruft den Zufallszahlengenerator mit dem erkannten Bereich auf.
- Danach formuliert Llama eine kurze Antwort mit Bereich + erzeugter Zahl.

## Voraussetzungen

- Python 3.10+
- [Ollama](https://ollama.com/) installiert
- Modell lokal verfügbar:

```bash
ollama pull llama3.1:8b
```

## Installation

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Starten

```bash
python llama_number_agent.py
```

## Beispiel

```text
Bitte gib deinen Wunsch ein (z. B. 'Ich will eine Zufallszahl von 10 bis 50').
> Ich will eine Zufallszahl
Starte Agent mit Modell llama3.1:8b. Intervall: 10s. Aktiver Bereich: 0 bis 100
Hier ist deine Zufallszahl im Bereich 0 bis 100: 42.
```
