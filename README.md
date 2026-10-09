# Clear Writing / Ясный текст

An agent skill for writing and editing clear English and Russian: emails, documentation, articles, reports, presentations, and UI copy. It helps an AI agent explain what matters while preserving facts, conditions, and the author's intent. Both languages have complete guides, examples, and review cases.

Скилл для AI-агентов, которые пишут и редактируют письма, документацию, статьи, отчёты, презентации и тексты интерфейса на русском и английском. Помогает объяснить главное, сохранив факты, условия и замысел автора. Для обоих языков есть полные руководства, примеры и контрольные случаи.

[English](#english) · [Русский](#русский)

## English

### What it does

- **Clarity beyond brevity.** Works on the reader's needs, context, structure, explanations, wording, and tone. Cutting words is useful only when it helps the reader.
- **Meaning first.** Instructs the agent to preserve negation, uncertainty, numbers, units, deadlines, names, and technical contracts, and to avoid inventing facts.
- **Two full editions.** Selects the guide by the target text's language. Editing does not imply translation; bilingual work uses both guides.
- **Self-contained guidance.** Includes six topic chapters per language, editing patterns, a decision table, a glossary, and review cases. No books or external summaries are needed to apply the skill.

### Example

After installation, ask your agent:

```text
Use $clear-writing to edit this customer email.
Keep the deadline and the condition. Return only the edited text.
"We would like to inform you that if payment is not received by 15 October,
access to the service will be suspended."
```

Illustrative edit, not a guaranteed model response:

> If we do not receive payment by 15 October, we will suspend access to the service.

You can also ask it to draft instructions, explain a technical concept to a particular audience, restructure a report, or edit UI copy. Supply the source text or facts, the audience, and any wording or format that must stay unchanged.

### Install

With Node.js and npm installed, run this from your project directory:

```sh
npx skills add serge-masiutin/clear-writing --skill clear-writing
```

The [skills CLI](https://github.com/vercel-labs/skills) lets you choose the target agent. To install for Codex or Claude Code explicitly:

```sh
npx skills add serge-masiutin/clear-writing --skill clear-writing -a codex
npx skills add serge-masiutin/clear-writing --skill clear-writing -a claude-code
```

Choose one command for your agent. Add `-g` for a user-wide installation instead of a project installation. Review any existing `clear-writing` installation before replacing it.

Alternatively, use Git and copy the complete skill folder into your agent's skills directory. For a project using `.agents/skills` (POSIX shell):

```sh
git clone https://github.com/serge-masiutin/clear-writing.git clear-writing-source
mkdir -p .agents/skills
test ! -e .agents/skills/clear-writing && \
  cp -R clear-writing-source/skills/clear-writing .agents/skills/clear-writing
```

The copy command refuses to overwrite an existing destination. **Copy the whole folder, not just `SKILL.md`: the guides and references are required.** Follow your agent's instructions for discovering newly installed skills. The invocation syntax depends on the agent; `$clear-writing` is an explicit Codex invocation.

### Contents and maintenance

The entry point is [`skills/clear-writing/SKILL.md`](skills/clear-writing/SKILL.md). It routes the agent to the appropriate language and topic:

| Material | English | Russian |
| --- | --- | --- |
| Complete guide | [Guide](skills/clear-writing/en/guide.md) | [Руководство](skills/clear-writing/ru/guide.md) |
| Editing techniques | [Patterns](skills/clear-writing/en/patterns.md) | [Приёмы](skills/clear-writing/ru/patterns.md) |
| Decision table | [Cheatsheet](skills/clear-writing/en/cheatsheet.md) | [Шпаргалка](skills/clear-writing/ru/cheatsheet.md) |
| Terminology | [Glossary](skills/clear-writing/en/glossary.md) | [Словарь](skills/clear-writing/ru/glossary.md) |
| Behavioral review | [Cases](skills/clear-writing/en/references/review-cases.md) | [Случаи](skills/clear-writing/ru/references/review-cases.md) |

The six chapters cover readers and context, words and sentences, explanation and evidence, structure, presentation, and writing formats. When changing the method, follow the [localization review](skills/clear-writing/references/localization-review.md) and review both language editions. Review cases are manual evaluation material, not an automated test suite. Model output still needs review for factual accuracy and task-specific requirements.

### Origin and license

Extracted from [serge-masiutin/rails-template](https://github.com/serge-masiutin/rails-template/tree/3e4ad0db288137d5800645ca47f7457fa93967d8/.agents/skills/clear-writing), commit `3e4ad0db288137d5800645ca47f7457fa93967d8`. The initial standalone package preserves all 24 source skill files byte for byte, including skill metadata version `7`.

The method is an independent practical adaptation of «Пиши, сокращай» by Maxim Ilyakhov and Lyudmila Sarycheva (4th edition, 2024) and «Ясно, понятно» by Maxim Ilyakhov (2021). It is not an official skill by the authors and does not include the books. Rules and teaching examples were written for the skill.

[MIT license](LICENSE), copyright © 2026 Serge Masiutin. A copy of the license is included inside the installable skill folder.

## Русский

### Что делает скилл

- **Работает не только с краткостью.** Учитывает задачу читателя, контекст, структуру, объяснения, слова и тон. Сокращение полезно, только если помогает понять текст.
- **Сохраняет смысл.** Предписывает сохранять отрицания, степень уверенности, числа, единицы, сроки, названия и технические контракты; запрещает выдумывать факты.
- **Содержит две полные версии.** Выбирает руководство по языку целевого текста. Редактура не означает перевод; для двуязычного результата используются оба руководства.
- **Не требует книг.** В каждой языковой версии есть шесть тематических глав, приёмы редактуры, таблица выбора, словарь и контрольные случаи. Все материалы для применения входят в скилл.

### Пример

После установки попросите агента:

```text
Используй $clear-writing, чтобы отредактировать письмо клиенту.
Сохрани срок и условие. Верни только чистовой текст.
«Настоящим уведомляем вас о том, что в случае непоступления оплаты
до 15 октября доступ к сервису будет приостановлен».
```

Пример редактуры, а не гарантированный ответ модели:

> Если оплата не поступит до 15 октября, мы приостановим доступ к сервису.

Также можно попросить написать инструкцию, объяснить техническую тему определённой аудитории, перестроить отчёт или отредактировать текст интерфейса. Передайте исходный текст или факты, опишите читателя и укажите, какие формулировки и формат нужно сохранить.

### Установка

Установите Node.js и npm, затем выполните в каталоге своего проекта:

```sh
npx skills add serge-masiutin/clear-writing --skill clear-writing
```

[Установщик skills](https://github.com/vercel-labs/skills) предложит выбрать агента. Чтобы явно указать Codex или Claude Code:

```sh
npx skills add serge-masiutin/clear-writing --skill clear-writing -a codex
npx skills add serge-masiutin/clear-writing --skill clear-writing -a claude-code
```

Выберите одну команду для своего агента. Добавьте `-g`, если скилл должен быть доступен во всех проектах пользователя. Перед заменой проверьте существующую установку `clear-writing`.

Другой способ — клонировать репозиторий через Git и скопировать папку скилла целиком. Для проекта, который использует `.agents/skills`, выполните в POSIX-совместимой оболочке:

```sh
git clone https://github.com/serge-masiutin/clear-writing.git clear-writing-source
mkdir -p .agents/skills
test ! -e .agents/skills/clear-writing && \
  cp -R clear-writing-source/skills/clear-writing .agents/skills/clear-writing
```

Команда копирования не заменяет существующую папку. **Копируйте всю папку, а не только `SKILL.md`: руководства и справочники необходимы для работы.** Для обнаружения нового скилла следуйте инструкции вашего агента. Синтаксис вызова зависит от агента; `$clear-writing` — явный вызов в Codex.

### Состав и развитие

Точка входа — [`skills/clear-writing/SKILL.md`](skills/clear-writing/SKILL.md). Она направляет агента к нужному языку и теме:

| Материал | Русский | English |
| --- | --- | --- |
| Полное руководство | [Руководство](skills/clear-writing/ru/guide.md) | [Guide](skills/clear-writing/en/guide.md) |
| Приёмы редактуры | [Приёмы](skills/clear-writing/ru/patterns.md) | [Patterns](skills/clear-writing/en/patterns.md) |
| Таблица выбора | [Шпаргалка](skills/clear-writing/ru/cheatsheet.md) | [Cheatsheet](skills/clear-writing/en/cheatsheet.md) |
| Термины | [Словарь](skills/clear-writing/ru/glossary.md) | [Glossary](skills/clear-writing/en/glossary.md) |
| Проверка поведения | [Случаи](skills/clear-writing/ru/references/review-cases.md) | [Cases](skills/clear-writing/en/references/review-cases.md) |

Шесть глав посвящены читателю и контексту, словам и предложениям, объяснению и доказательствам, структуре, подаче и форматам текста. При изменении методики пройдите [проверку локализации](skills/clear-writing/references/localization-review.md) и контрольные случаи обеих версий. Это материалы для ручной оценки, а не автоматические тесты. Ответы модели нужно проверять на достоверность и соответствие конкретной задаче.

### Источник и лицензия

Скилл выделен из [serge-masiutin/rails-template](https://github.com/serge-masiutin/rails-template/tree/3e4ad0db288137d5800645ca47f7457fa93967d8/.agents/skills/clear-writing), коммит `3e4ad0db288137d5800645ca47f7457fa93967d8`. Первая самостоятельная поставка сохраняет все 24 исходных файла скилла побайтово, включая версию `7` в метаданных.

Методика — самостоятельная практическая адаптация книг «Пиши, сокращай» Максима Ильяхова и Людмилы Сарычевой (4-е издание, 2024) и «Ясно, понятно» Максима Ильяхова (2021). Это не официальный скилл авторов; сами книги в поставку не входят. Правила и учебные примеры написаны для скилла.

[Лицензия MIT](LICENSE), © 2026 Serge Masiutin. Копия лицензии включена в устанавливаемую папку скилла.
