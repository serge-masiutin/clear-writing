#!/usr/bin/env python3
"""Report local, reproducible Russian or English writing diagnostics as JSON.

The scores are Clear Writing indicators, not Glavred scores or a quality verdict.
No network requests, model calls, or file writes are performed.
"""

import argparse
from dataclasses import dataclass
import json
import re
import sys
from pathlib import Path


VERSION = "1"
MAX_CHARACTERS = 200_000
MIN_CLEANLINESS_WORDS = 30
MIN_READABILITY_WORDS = 50
MIN_READABILITY_SENTENCES = 3
MAX_REPORTED_FINDINGS = 100
MAX_REPORTED_LONG_SENTENCES = 30
WORD_RE = re.compile(r"[A-Za-z]+(?:['’][A-Za-z]+)?|[А-Яа-яЁё]+(?:-[А-Яа-яЁё]+)*")
SENTENCE_RE = re.compile(r"[^.!?…]+(?:[.!?…]+|$)", re.DOTALL)
EN_VOWELS = re.compile(r"[aeiouy]+", re.IGNORECASE)
RU_VOWELS = re.compile(r"[аеёиоуыэюя]+", re.IGNORECASE)


@dataclass(frozen=True)
class Rule:
    id: str
    category: str
    phrases: tuple[str, ...]


# These are original, deliberately small review lists. A match is a prompt to
# inspect context, not an instruction to delete the phrase.
RULES = {
    "ru": (
        Rule("ru_filler_intro", "filler", ("следует отметить", "необходимо отметить", "как известно", "ни для кого не секрет")),
        Rule("ru_filler_time", "filler", ("в настоящее время", "на сегодняшний день")),
        Rule("ru_bureaucratic", "bureaucratic", ("осуществление", "в целях", "имеет место")),
        Rule("ru_cliche", "cliche", ("комплексный подход", "широкий спектр", "новый уровень", "уникальная возможность")),
        Rule("ru_intensifier", "intensifier", ("очень", "крайне", "абсолютно", "максимально")),
        Rule("ru_evaluation", "evaluation", ("уникальный", "уникальная", "эффективный", "эффективная", "инновационный", "лучший")),
    ),
    "en": (
        Rule("en_filler_intro", "filler", ("it should be noted that", "as everyone knows", "needless to say")),
        Rule("en_filler_time", "filler", ("at this point in time",)),
        Rule("en_bureaucratic", "bureaucratic", ("in order to", "due to the fact that", "for the purpose of", "carry out")),
        Rule("en_cliche", "cliche", ("cutting-edge", "best-in-class", "world-class", "next level", "seamless experience")),
        Rule("en_intensifier", "intensifier", ("very", "extremely", "absolutely", "truly")),
        Rule("en_evaluation", "evaluation", ("unique", "innovative", "reliable", "efficient", "best")),
    ),
}


def syllables(word: str) -> int:
    if re.search(r"[А-Яа-яЁё]", word):
        return max(1, len(RU_VOWELS.findall(word)))
    lowered = word.casefold()
    count = len(EN_VOWELS.findall(lowered))
    if lowered.endswith("e") and not lowered.endswith(("le", "ye")) and count > 1:
        count -= 1
    return max(1, count)


def find_rules(text: str, language: str) -> list[dict]:
    findings = []
    for rule in RULES[language]:
        for phrase in rule.phrases:
            # Case-insensitive phrase boundaries; flexible whitespace includes line wraps.
            body = r"\s+".join(re.escape(part) for part in phrase.split())
            pattern = re.compile(r"(?<!\w)" + body + r"(?!\w)", re.IGNORECASE)
            for match in pattern.finditer(text):
                findings.append({"rule": rule.id, "category": rule.category,
                                 "start": match.start(), "end": match.end()})
    return sorted(findings, key=lambda finding: (finding["start"], finding["end"], finding["rule"]))


def count_flagged_words(words: list[re.Match], findings: list[dict]) -> int:
    intervals = []
    for finding in findings:
        start, end = finding["start"], finding["end"]
        if intervals and start <= intervals[-1][1]:
            intervals[-1] = (intervals[-1][0], max(end, intervals[-1][1]))
        else:
            intervals.append((start, end))
    index = 0
    flagged = 0
    for word in words:
        while index < len(intervals) and intervals[index][1] <= word.start():
            index += 1
        if index < len(intervals) and intervals[index][0] < word.end():
            flagged += 1
    return flagged


def analyze(text: str, language: str) -> dict:
    if language not in RULES:
        raise ValueError("language must be 'ru' or 'en'")
    if not text.strip():
        raise ValueError("text must not be empty")
    if len(text) > MAX_CHARACTERS:
        raise ValueError(f"text exceeds {MAX_CHARACTERS} characters")

    words = list(WORD_RE.finditer(text))
    if not words:
        raise ValueError("text must contain Russian or English words")
    target_words = sum(bool(re.search(r"[А-Яа-яЁё]" if language == "ru" else r"[A-Za-z]", word.group())) for word in words)
    if target_words / len(words) < 0.7:
        raise ValueError("at least 70% of words must use the selected language's script")

    sentences = []
    for match in SENTENCE_RE.finditer(text):
        sentence_words = list(WORD_RE.finditer(match.group()))
        if sentence_words:
            sentences.append((match.start(), match.end(), len(sentence_words)))

    findings = find_rules(text, language)
    flagged_words = count_flagged_words(words, findings)
    warnings = []
    cleanliness = None
    if len(words) >= MIN_CLEANLINESS_WORDS:
        cleanliness = round(10 * (1 - flagged_words / len(words)), 1)
    else:
        warnings.append("cleanliness_needs_30_words")

    readability = None
    reading_ease = None
    if len(words) >= MIN_READABILITY_WORDS and len(sentences) >= MIN_READABILITY_SENTENCES:
        average_sentence_length = len(words) / len(sentences)
        average_syllables = sum(syllables(word.group()) for word in words) / len(words)
        if language == "en":
            reading_ease = 206.835 - 1.015 * average_sentence_length - 84.6 * average_syllables
        else:
            reading_ease = 208.7 - 2.6 * average_sentence_length - 39.2 * average_syllables
        readability = round(max(0, min(10, reading_ease / 10)), 1)
        reading_ease = round(reading_ease, 1)
    else:
        warnings.append("readability_needs_50_words_and_3_sentences")

    long_sentences = [
        {"start": start, "end": end, "words": count}
        for start, end, count in sentences if count > 30
    ]
    return {
        "method_version": VERSION,
        "language": language,
        "word_count": len(words),
        "sentence_count": len(sentences),
        "cleanliness": {"score": cleanliness, "flagged_words": flagged_words,
                        "flagged_percent": round(100 * flagged_words / len(words), 1)},
        "readability": {"score": readability, "reading_ease": reading_ease,
                        "long_sentences": long_sentences[:MAX_REPORTED_LONG_SENTENCES],
                        "omitted_long_sentences": max(0, len(long_sentences) - MAX_REPORTED_LONG_SENTENCES)},
        "findings": findings[:MAX_REPORTED_FINDINGS],
        "omitted_findings": max(0, len(findings) - MAX_REPORTED_FINDINGS),
        "warnings": warnings,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--language", choices=("ru", "en"), required=True)
    parser.add_argument("--file", type=Path, help="UTF-8 plain text file; otherwise read stdin")
    args = parser.parse_args()
    try:
        text = args.file.read_text(encoding="utf-8") if args.file else sys.stdin.read()
        result = analyze(text, args.language)
    except (OSError, UnicodeError, ValueError) as error:
        parser.exit(2, f"check_text: {error}\n")
    json.dump(result, sys.stdout, ensure_ascii=False, indent=2)
    sys.stdout.write("\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
