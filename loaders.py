from dataclasses import dataclass
from typing import Dict, List
from pathlib import Path
import json


@dataclass
class Record:
    sentences: str
    # label None means we using dev dataset (no labels)
    labels: List[Dict] | None
    pass


class DataLoader:
    def load_data(self, dir: Path | str, type="train") -> List[Record]:
        if type == "train":
            return self._load_train_dataset(dir)
        elif type == "dev":
            return self._load_dev_dataset(dir)
        else:
            raise ValueError("Invalid dataset type, must be 'train' or 'dev'")

    def _load_train_dataset(self, dir: Path | str) -> List[Record]:
        dir = Path(dir)
        if not dir.is_dir():
            raise ValueError(f"Invalid dataset directory: {dir}")

        result = []

        for filepath in dir.iterdir():
            with open(filepath, "r") as fd:
                content = fd.read()
                raw_records = content.split("\n\n")

                for raw_record in raw_records:
                    record = self.parse_record(raw_record)
                    result.append(record)

        return result

    def _load_dev_dataset(self, dir: Path | str) -> List[Record]:
        return []

    def parse_record(self, raw: str) -> Record:
        sentence, *raw_labels = raw.split("\n")
        labels = [json.loads(label) for label in raw_labels]

        return Record(sentences=sentence, labels=labels)
