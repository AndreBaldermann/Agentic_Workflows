"""LangChain agent that asks Llama 3.1:8b for a random number every 10 seconds."""

from __future__ import annotations

import random
import re
import time

from langchain_core.prompts import ChatPromptTemplate
from langchain_ollama import ChatOllama


MODEL_NAME = "llama3.1:8b"
INTERVAL_SECONDS = 10


def extract_number(text: str) -> int:
    """Extract the first integer from a model response, fallback to random."""
    match = re.search(r"-?\d+", text)
    if match:
        return int(match.group(0))
    return random.randint(0, 10_000)


def build_chain():
    prompt = ChatPromptTemplate.from_messages(
        [
            (
                "system",
                "Du bist ein Assistent, der nur eine einzelne ganze Zahl ausgibt.",
            ),
            ("human", "Nenne eine beliebige Zahl."),
        ]
    )

    llm = ChatOllama(model=MODEL_NAME, temperature=1)
    return prompt | llm


def main() -> None:
    chain = build_chain()
    print(f"Starte Agent mit Modell {MODEL_NAME}. Intervall: {INTERVAL_SECONDS}s")

    while True:
        response = chain.invoke({})
        number = extract_number(response.content)
        print(f"Neue Zahl: {number}")
        time.sleep(INTERVAL_SECONDS)


if __name__ == "__main__":
    main()
