"""LangChain agent with llama3.1:8b that generates a random number every 10 seconds."""

from __future__ import annotations

import random
import re
import time
from typing import TypedDict

from langchain_core.messages import HumanMessage, SystemMessage, ToolMessage
from langchain_core.tools import tool
from langchain_ollama import ChatOllama

MODEL_NAME = "llama3.1:8b"
INTERVAL_SECONDS = 10
DEFAULT_MIN = 0
DEFAULT_MAX = 100


class NumberRange(TypedDict):
    min_value: int
    max_value: int


@tool
def random_number_generator(min_value: int, max_value: int) -> int:
    """Generiert eine ganzzahlige Zufallszahl im inklusiven Wertebereich [min_value, max_value]."""
    if min_value > max_value:
        min_value, max_value = max_value, min_value
    return random.randint(min_value, max_value)


def extract_range(user_prompt: str) -> NumberRange:
    """Extract a range from user text; fallback to 0-100."""
    numbers = [int(match) for match in re.findall(r"-?\d+", user_prompt)]

    if len(numbers) >= 2:
        low, high = numbers[0], numbers[1]
    else:
        low, high = DEFAULT_MIN, DEFAULT_MAX

    if low > high:
        low, high = high, low

    return {"min_value": low, "max_value": high}


def build_model() -> ChatOllama:
    llm = ChatOllama(model=MODEL_NAME, temperature=0.7)
    return llm.bind_tools([random_number_generator])


def generate_message(llm_with_tools: ChatOllama, bounds: NumberRange) -> str:
    system_prompt = (
        "Du bist ein Assistent für Zufallszahlen. "
        "Du MUSST das Tool random_number_generator genau einmal pro Anfrage aufrufen. "
        "Nutze exakt die übergebenen min_value und max_value. "
        "Gib danach eine kurze, freundliche Antwort auf Deutsch aus, "
        "die Wertebereich und erzeugte Zahl enthält."
    )

    human_prompt = (
        "Ich möchte eine Zufallszahl. "
        f"Verwende den Wertebereich min_value={bounds['min_value']} "
        f"und max_value={bounds['max_value']}."
    )

    first_response = llm_with_tools.invoke(
        [SystemMessage(content=system_prompt), HumanMessage(content=human_prompt)]
    )

    if not first_response.tool_calls:
        fallback_number = random_number_generator.invoke(bounds)
        return (
            "(Fallback) Hier ist deine Zufallszahl "
            f"im Bereich {bounds['min_value']} bis {bounds['max_value']}: {fallback_number}."
        )

    tool_call = first_response.tool_calls[0]
    tool_result = random_number_generator.invoke(tool_call["args"])

    final_response = llm_with_tools.invoke(
        [
            SystemMessage(content=system_prompt),
            HumanMessage(content=human_prompt),
            first_response,
            ToolMessage(content=str(tool_result), tool_call_id=tool_call["id"]),
        ]
    )
    return final_response.content


def main() -> None:
    print("Bitte gib deinen Wunsch ein (z. B. 'Ich will eine Zufallszahl von 10 bis 50').")
    user_prompt = input("> ").strip()

    bounds = extract_range(user_prompt)
    llm_with_tools = build_model()

    print(
        f"Starte Agent mit Modell {MODEL_NAME}. "
        f"Intervall: {INTERVAL_SECONDS}s. "
        f"Aktiver Bereich: {bounds['min_value']} bis {bounds['max_value']}"
    )

    while True:
        message = generate_message(llm_with_tools, bounds)
        print(message)
        time.sleep(INTERVAL_SECONDS)


if __name__ == "__main__":
    main()
