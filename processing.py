from typing import Dict, List, Literal
from datatypes import Record

Tag = Literal[
    "B-Sub", "I-Sub", "B-Obj", "I-Obj", "B-Asp", "I-Asp", "B-Pre", "I-Pre", "O"
]


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

    def record2tags(self, record: Record) -> List[List[Tag]]:
        """POStag of sentence, for each quintuple"""
        tags_sequence = []
        sentences_tokens = record.sentence.split(" ")

        for quintuple in record.quintuples:
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

            tags_sequence.append(encoded_tagged_tokens)

        return tags_sequence

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

    def id2tag(self, _id: str):
        return RecordDecoder.TAGS[int(_id) - 1]

    pass
