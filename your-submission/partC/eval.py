import json
import re
from difflib import SequenceMatcher


def similarity(a, b):
    return SequenceMatcher(None, a, b).ratio()


def extract_numbers(text):
    return re.findall(r"\d+(?:[.,]\d+)?", text)


def evaluate_item(item, generated):
    formal = item["formal"]
    target = item["target"]

    similarity_to_target = similarity(generated, target)

    formal_numbers = extract_numbers(formal)
    generated_numbers = extract_numbers(generated)

    missing_numbers = [
        number for number in formal_numbers
        if number not in generated_numbers
    ]

    return {
        "id": item["id"],
        "language": item["language"],
        "similarity_to_target": round(similarity_to_target, 3),
        "formal_chars": len(formal),
        "generated_chars": len(generated),
        "length_ratio": round(
            len(generated) / max(len(formal), 1), 3
        ),
        "missing_numbers": missing_numbers,
        "meaning_flag": len(missing_numbers) > 0,
    }


def main():
    with open("partC/eval_set.json", "r", encoding="utf-8") as f:
        dataset = json.load(f)

    print("Part C evaluation set")
    print("=" * 60)
    print("examples:", len(dataset))
    print()

    # For now, use the formal input itself as a placeholder.
    # Real model outputs will replace this in the next step.
    results = []

    for item in dataset:
        result = evaluate_item(item, item["formal"])
        results.append(result)

    print(
        f"{'ID':<8} {'Language':<10} "
        f"{'TargetSim':>10} {'LenRatio':>10} {'Meaning':>10}"
    )
    print("-" * 60)

    for result in results:
        print(
            f"{result['id']:<8} "
            f"{result['language']:<10} "
            f"{result['similarity_to_target']:>10.3f} "
            f"{result['length_ratio']:>10.3f} "
            f"{'PASS' if not result['meaning_flag'] else 'CHECK':>10}"
        )


if __name__ == "__main__":
    main()