import json
import re
import itertools
from pathlib import Path


# -----------------------------
# Helpers
# -----------------------------

def extract_symptoms(text: str) -> list[str]:
    """
    Extrai sintomas do texto usando heurísticas simples.
    Busca listas após termos comuns como 'include', 'symptoms', etc.
    """
    text = text.lower()

    # Padrões comuns em textos médicos
    symptom_patterns = [
        r"symptoms? (?:include|are|may include|may involve):? (.*?)(?:\.|$)",
        r"signs? (?:include|are|may include):? (.*?)(?:\.|$)",
        r"can cause: (.*?)(?:\.|$)"
    ]

    candidates = []
    for pattern in symptom_patterns:
        match = re.search(pattern, text)
        if match:
            raw = match.group(1)
            items = re.split(r",| - |•|\n|\t", raw)
            items = [i.strip(" .;:-") for i in items if len(i.strip()) > 2]
            candidates.extend(items)

    # Filtro final: palavras curtas demais geralmente não são sintomas
    candidates = [c for c in candidates if len(c.split()) <= 7]

    # Deduplicar mantendo ordem
    seen = set()
    final = []
    for c in candidates:
        if c not in seen:
            seen.add(c)
            final.append(c)

    return final


def symptom_permutations(symptoms: list[str], max_examples=4):
    """
    Gera combinações diferentes para criar diversidade no dataset.
    """
    if len(symptoms) <= 3:
        return [symptoms]

    combos = list(itertools.combinations(symptoms, 3))
    return combos[:max_examples]


def build_instruction(symptoms: list[str]) -> str:
    joined = ", ".join(symptoms)
    return (
        f"Given the symptoms: {joined}, identify the most likely disease."
    )


# -----------------------------
# Conversão principal
# -----------------------------

def generate_symptom_to_disease_dataset(input_json_path: str,
                                        output_jsonl_path: str):
    input_path = Path(input_json_path)

    with open(input_path, "r", encoding="utf-8") as f:
        data = [json.loads(line) for line in f.readlines()]

    results = []

    for item in data:
        disease_name = item["instruction"]
        description = item["output"]

        symptoms = extract_symptoms(description)

        if not symptoms:
            continue

        combos = symptom_permutations(symptoms)

        for combo in combos:
            results.append({
                "instruction": build_instruction(combo),
                "input": "",
                "output": f"The most likely disease is {disease_name}."
            })

    with open(output_jsonl_path, "w", encoding="utf-8") as out:
        for entry in results:
            out.write(json.dumps(entry, ensure_ascii=False) + "\n")

    print("✓ Dataset invertido gerado com sucesso!")
    print(f"✓ Exemplos criados: {len(results)}")
    print(f"✓ Arquivo salvo em: {output_jsonl_path}")


generate_symptom_to_disease_dataset(
    input_json_path="dataset/dataset_alpaca.jsonl",
    output_jsonl_path="dataset/dataset_symptoms_to_disease.jsonl"
)
