# LangChain Agent mit Llama 3.1:8b

Dieses Repo enthält einen einfachen LangChain-Agenten, der alle 10 Sekunden eine beliebige Zahl nennt.

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

Beispielausgabe:

```text
Starte Agent mit Modell llama3.1:8b. Intervall: 10s
Neue Zahl: 482
Neue Zahl: 17
Neue Zahl: 9931
```
