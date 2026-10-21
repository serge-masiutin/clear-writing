# Practical technical English

Load for procedures, runbooks, troubleshooting, setup instructions, technical
descriptions, or an explicit STE request. Use alongside [the guide](guide.md).
For ordinary correspondence or narrative, keep natural plain English rather than
forcing a controlled language.

## Status and scope

This is an original, STE-informed editing profile based on ASD-STE100 Issue 9
(2025-01-15), not a reproduction of the standard or an approved-word checker.
STE includes writing rules **and** a controlled dictionary with permitted meanings
and parts of speech; it also permits technical nouns and verbs under specific rules.
Simple words alone do not establish compliance. Never label an edit STE-compliant
without checking the complete applicable rules, dictionary, and project terminology.
If these are unavailable, offer a STE-informed draft and state the limitation.
Do not invent approved words, rule numbers, certification, or a compliance score.

## Editing pass

1. **Protect the contract.** Identify actors, objects, conditions, order, limits,
   hazards, prohibitions, permissions, and uncertainty before rewriting. Keep code,
   commands, paths, UI labels, placeholders, and approved terms exact.
2. **Use one name for one concept.** Follow the supplied glossary. Repeat a term
   instead of varying it for style. Do not merge distinct concepts such as deleting,
   disabling, and archiving. Define an unfamiliar abbreviation at first use when
   its expansion is known and useful. Never guess an expansion.
3. **Separate procedure from description.** Put prerequisites before numbered steps.
   Put a condition before its action: “If the status is Ready, select Export.”
   Keep an explanation or a note outside the executable step. Preserve dependencies
   when splitting sentences; do not turn “only after” into an optional condition.
4. **Make each step actionable.** Start direct instructions with an imperative verb.
   Prefer one main action per step. Identify the object; replace “do this” and “it”
   when the referent is unclear. Keep tightly coupled actions together only when
   separating them would obscure the operation. Do not invent an actor in descriptions.
5. **Keep syntax simple.** Prefer active voice and direct verbs over nominalizations.
   Unpack ambiguous noun chains with prepositions or clauses. Preserve official
   multi-word names. Avoid idioms and ambiguous “-ing” clauses; rewrite them as
   explicit actions or conditions, but keep technical terms and quoted labels.
6. **Inspect length without sacrificing meaning.** STE sets maxima of 20 words for
   procedural sentences and 25 for descriptive sentences (rules 5.1 and 6.3), with
   its own counting rules in section 8. Treat these as editing targets in this
   profile, not a universal limit or a reason to delete a condition. A strict STE
   review needs the standard's counting method, not a whitespace counter or Flesch score.
7. **Keep modality exact.** Do not turn “may” into “must,” “can” into permission,
   or “should” into a requirement. Clarify ambiguous modality only from evidence;
   ask if the distinction changes safety, access, or obligations.
8. **Put safety before action.** Keep the source warning and its severity before
   the hazardous step. Do not weaken “must not,” hide a hazard in a note, or invent
   protective equipment, recovery commands, wait times, or safety guarantees.
9. **Check the result.** State an observable completion check when the source gives
   one. Replace vague “check that it works” with that check, not an invented value.
   If success criteria or recovery steps are missing, identify the gap separately.

## Examples

The examples teach clarity; they are not certified STE text.

| Source | Edit | Preserve |
| --- | --- | --- |
| After the status has changed to Ready, the Export button must be clicked. | After the status changes to Ready, select Export. | Required action; Ready and Export are exact labels |
| Before opening the cover, disconnect the power supply. | Disconnect the power supply before you open the cover. | Safety order; do not separate the second action from its prerequisite |
| Admins may export records; reviewers must not export them. | Admins may export records. Reviewers must not export records. | Permission and prohibition remain distinct |
| The archive must be no larger than 5 MB and must be uploaded over HTTPS in Debug only. | In Debug only, upload the archive over HTTPS. The archive must be no larger than 5 MB. | Mode, protocol, maximum size |
| Check that the service works. | Check that the service works. | No observable check was supplied; report the missing criterion rather than inventing an endpoint |

## Final check

Walk through the text as the intended operator: can they identify the prerequisite,
action, object, branch, and completion check without guessing? Compare against the
source again. Leave missing operational facts unresolved explicitly. Stop when the
task is clear and faithful, not when every sentence looks equally short.
The [local checker](../references/local-metrics.md) can flag prose issues; it does
not validate the STE dictionary, word counting, safety, or compliance.

## Sources and limits

- [ASD: About STE](https://www.asd-ste100.org/about_STE.html): scope, Issue 9,
  rules, dictionary, and technical terminology.
- [Official Issue 9](https://www.asd-ste100.org/assets/files/ASD-STE100_ISSUE9.pdf):
  sections 1–8, especially 3 (verbs), 5 (procedures), 6 (descriptions), and 7 (safety).
  The standard and its dictionary remain ASD's material; they are not bundled here.
- [ISO 24495-1:2023](https://www.iso.org/standard/78907.html): a language-independent
  plain-language framework. It complements, but does not replace, controlled-language rules.

Sources checked 2026-10-22. Ordinary editing with this profile does not require browsing.
