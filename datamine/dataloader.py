from typing import List
from pathlib import Path

from datatypes import Record


class DataLoader:
    @staticmethod
    def load_data(dir: Path | str) -> List[Record]:
        dir = Path(dir)
        if not dir.is_dir():
            raise ValueError(f"Invalid dataset directory: {dir}")

        result = []
        for filepath in dir.iterdir():
            result.extend(DataLoader.load_data_single(filepath))
        return result

    @staticmethod
    def load_data_single(filepath: Path | str) -> List[Record]:
        result = []
        with open(filepath, "r") as fd:
            content = fd.read()
            raw_records = content.split("\n\n")

            for raw_record in raw_records:
                if len(raw_record) == 0:
                    continue
                record = Record.parse(raw_record)
                result.append(record)

        return result
