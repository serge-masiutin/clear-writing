# Local Cleanliness and Readability, version 1

Use the bundled `scripts/check_text.py` only on plain Russian or English prose. It uses
Python 3.9+'s standard library, reads a UTF-8 file or stdin, writes JSON to stdout, and
does not use a network, an API key, a model, or a third-party package. Do not put
confidential source text on a command line: process it through stdin or a local file.
The output contains rule identifiers and character offsets, not excerpts.

```sh
python3 scripts/check_text.py --language ru --file article.txt
python3 scripts/check_text.py --language en < article.txt
```

The scores belong to **Clear Writing**. They are not Glavred scores, cannot be
compared to Glavred scores, and have not been calibrated against human judgments.
The two language profiles use different readability coefficients; do not compare
their scores with each other. `method_version` identifies the scoring contract.

## What the numbers mean

- **Cleanliness / Чистота**: the share of words *not* covered by the bundled review
  phrases, multiplied by ten. Overlapping matches count each word once. A score
  exists at 30 words or more. The small rule lists cover filler, bureaucratic
  language, clichés, intensifiers, and unsupported evaluations. They are selective,
  not a complete language model. An unflagged text can still be vague or dishonest.
- **Readability / Читаемость**: Flesch Reading Ease, divided by ten and clamped to
  0–10. English uses `206.835 − 1.015 × words/sentences − 84.6 ×
  syllables/words`. Russian uses Solovyev et al.'s adaptation,
  `208.7 − 2.6 × words/sentences − 39.2 × syllables/words`. A score exists at
  50 words and 3 sentences or more. The raw `reading_ease` is also reported.
  Syllable counts and sentence boundaries are heuristic; abbreviations, names,
  lists, and technical terms can distort them. Sentences over 30 words are
  reported for inspection, not treated as errors or a hard writing limit.
- A missing score is `null` with a reason in `warnings`. Never replace it with a
  guessed number. Offsets in `findings` and `long_sentences` use Python Unicode
  character positions in the original input. Each phrase match is a question for
  the editor; it is not an automatic deletion instruction.
  The report includes at most 100 phrase matches and 30 long sentences; omitted
  counts are explicit. Scores still use every match in the input.

Use the results to locate a passage, read it in context, and decide whether changing
it helps the intended reader. Preserve evidence, meaningful uncertainty, legal or
technical terms, quotations, conditions, and the author's voice. Recheck after
substantial edits. When a score rises but the text loses useful information, prefer
the useful version. Do not report scores to the user unless requested or helpful to
the task; never claim that a score measures comprehension or overall quality.

## Evidence and limits

- [Glavred's own explanation](https://glvrd.ru/about/) says its score reflects the
  share of detected stop words, not text quality. Its [API documentation](https://glvrd.notion.site/v3-43755f79edae4a3da0949a9a38393969)
  describes server-side fragment detection and scoring from those fragments, but
  does not publish the full evolving rule set or an independently reproducible
  formula. This implementation is original and does not use Glavred's API or code.
- [Gordejeva et al. (2022)](https://pmc.ncbi.nlm.nih.gov/articles/PMC9152717/)
  report the English Flesch formula and Solovyev et al.'s Russian adaptation. They
  also note that syllable estimation is fallible and such formulas omit syntax,
  connections between sentences, illustrations, and the reader's knowledge.
- [Digital.gov's plain-language guidance](https://digital.gov/guides/plain-language/test)
  recommends testing whether real readers can understand and use important text.
  Paraphrase and usability testing answer questions that automated scores cannot.

This checker does not test grammar, spelling, factual accuracy, tone, accessibility,
or whether a reader can complete their task. It is intended for prose, not code,
tables, raw Markdown, or mixed-language documents. Check bilingual passages in
separate invocations. Input over 200,000 characters, empty input, and a mismatched
selected language fail with a nonzero exit status rather than producing a score.
