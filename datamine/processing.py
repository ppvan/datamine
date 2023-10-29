from typing import Dict, List
from datatypes import Record
from datatypes import Tag, LabelClass
import json


class RecordEncoder:
    WORD_TAGS = [
        "B-Sub",
        "I-Sub",
        "B-Obj",
        "I-Obj",
        "B-Asp",
        "I-Asp",
        "B-Pre",
        "I-Pre",
        "O",
    ]
    SPECIALS = [
        ",",
        ".",
        ":",
        ";",
        "?",
        "!",
        '"',
        "'",
        "(",
        ")",
        "-",
        "/",
        "\\",
        "*",
        "%",
        "#",
        "@",
        "&",
        "_",
        "[",
        "]",
        "{",
        "}",
        "|",
        "<",
        ">",
        "`",
        "~",
        "^",
        "+",
        "=",
        "|",
        "/",
        "?",
        ";",
        ":",
        "“",
        "”",
    ]
    TAGS = WORD_TAGS + SPECIALS

    def record2tags(self, record: Record) -> List[Tag]:
        """POStag of sentence, expect only 1 quintuple"""

        if len(record.quintuples) != 1:
            raise ValueError("Expect only 1 quintuple")

        quintuple = record.quintuples[0]
        sentences_tokens = record.sentence.split(" ")
        tagged_tokens = ["O" for _ in sentences_tokens]  # default Other
        subject = quintuple["subject"]
        _object = quintuple["object"]
        aspect = quintuple["aspect"]
        predicate = quintuple["predicate"]

        for index, raw_token in enumerate(subject):
            token_pos, _token_val = raw_token.split("&&")
            tagged_tokens[int(token_pos) - 1] = "B-Sub" if index == 0 else "I-Sub"

        for index, raw_token in enumerate(_object):
            token_pos, _token_val = raw_token.split("&&")
            tagged_tokens[int(token_pos) - 1] = "B-Obj" if index == 0 else "I-Obj"

        for index, raw_token in enumerate(aspect):
            token_pos, _token_val = raw_token.split("&&")
            tagged_tokens[int(token_pos) - 1] = "B-Asp" if index == 0 else "I-Asp"

        for index, raw_token in enumerate(predicate):
            token_pos, _token_val = raw_token.split("&&")
            tagged_tokens[int(token_pos) - 1] = "B-Pre" if index == 0 else "I-Pre"

        for index, token in enumerate(sentences_tokens):
            if token in self.SPECIALS:
                tagged_tokens[index] = token

        encoded_tagged_tokens = [self.tag2id(tag) for tag in tagged_tokens]

        return encoded_tagged_tokens

    def tag2id(self, tag: Tag) -> str:
        """Tag to id"""
        return str(self.TAGS.index(tag) + 1)

    def record2features(self, record: Record) -> List[Dict]:
        """Transform record to list of word features"""

        sentence_features = []
        sentence = record.sentence
        sentence_words = sentence.split(" ")

        for index, word in enumerate(sentence_words):
            word_features = {
                "word": word,
                "is_first": index == 0,
                "is_last": index == len(sentence_words) - 1,
                "is_capitalized": word.capitalize() == word,
                "is_all_caps": word.upper() == word,
                "is_all_lower": word.lower() == word,
                "is_alphanumeric": int(word.isalnum()),
                "prev_word": "" if index == 0 else sentence_words[index - 1],
                "next_word": ""
                if index >= len(sentence_words) - 1
                else sentence_words[index + 1],
                "is_numeric": word.isdigit(),
                "capitals_inside": word[1:].lower() != word[1:],
            }

            sentence_features.append(word_features)

        return sentence_features


class RecordDecoder:
    def __init__(self):
        pass

    def parse_tag(self, _id: str):
        return RecordEncoder.TAGS[int(_id) - 1]

    def label_record(
        self, unlabel: Record, comparatives: List[LabelClass], POStag: List[Tag]
    ) -> Record:
        tokenized_sentence = unlabel.sentence.split(" ")
        unlabel.quintuples = []
        unlabel.comparative = comparatives

        for label in comparatives:
            if label == "No":
                continue
            quintuple = {
                "label": label,
                "subject": [],
                "object": [],
                "aspect": [],
                "predicate": [],
            }

            for index, token in enumerate(tokenized_sentence):
                if POStag[index] in ["B-Sub", "I-Sub"]:
                    quintuple["subject"].append(f"{index + 1}&&{token}")
                elif POStag[index] in ["B-Obj", "I-Obj"]:
                    quintuple["object"].append(f"{index + 1}&&{token}")
                elif POStag[index] in ["B-Asp", "I-Asp"]:
                    quintuple["aspect"].append(f"{index + 1}&&{token}")
                elif POStag[index] in ["B-Pre", "I-Pre"]:
                    quintuple["predicate"].append(f"{index + 1}&&{token}")

            unlabel.quintuples.append(quintuple)

        return unlabel

    def format_record(self, record: Record) -> str:
        """Format record to string"""
        formatted_sentence = f"{record.original}\t{record.sentence}"
        formatted_quintuples = [
            json.dumps(quintuple) for quintuple in record.quintuples
        ]
        return "\n".join([formatted_sentence, *formatted_quintuples])
