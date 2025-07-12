from branches.dataset_tuner.dataset_parser import parse_dataset
from branches.dataset_tuner.dataset_validator import validate_schema

def test_tuner():
    sample = {
        "records": [
            { "text": "AI is transforming the world.", "tags": ["tech", "ai"] },
            { "text": "Data helps build better models.", "tags": ["data"] }
        ]
    }

    valid, msg = validate_schema(sample)
    assert valid, f"❌ Invalid schema: {msg}"
    entries = parse_dataset(sample)
    assert len(entries) == 2, "❌ Parsing error"

    print("✅ Dataset Tuner test passed.")

if __name__ == "__main__":
    test_tuner()
