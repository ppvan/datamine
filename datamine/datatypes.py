from dataclasses import dataclass, field
from typing import Dict, List, Literal
import json


Tag = (
    Literal["B-Sub", "I-Sub", "B-Obj", "I-Obj", "B-Asp", "I-Asp", "B-Pre", "I-Pre", "O"]
    | str
)
LabelClass = (
    Literal["No", "DIF", "EQL", "SUP+", "SUP-", "SUP", "COM+", "COM-", "COM"] | str
)


@dataclass
class Record:
    original: str
    sentence: str
    # label None means we using dev dataset (no labels)
    quintuples: List[Dict]
    comparative: List[LabelClass] = field(default_factory=list)

    @staticmethod
    def parse(raw: str):
        """Parse a record from dataset format.
        Note that in devset, comparative is ["No"]
        """
        if "\t" not in raw:
            raise ValueError(f"Invalid record format: {raw}")

        sentences, *raw_labels = raw.split("\n")
        original, tokenized_sentence = sentences.split("\t")
        
        quintuples = [json.loads(label) for label in raw_labels]
        comparative = [tup["label"] for tup in quintuples]
        if not comparative:
            comparative = ["No"]

        return Record(
            original=original,
            sentence=tokenized_sentence,
            quintuples=quintuples,
            comparative=comparative,
        )
