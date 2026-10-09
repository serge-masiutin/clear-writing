# Clear Writing / Ясный текст

Clear Writing gives AI agents practical guidance for writing and editing in English and Russian. Use it to make emails, documentation, articles, reports, presentations, and UI copy easier to understand without losing meaning.

Clear Writing — скилл с практическими правилами письма и редактуры для AI-агентов. Помогает сделать письма, документацию, статьи, отчёты, презентации и тексты интерфейса понятнее, сохранив смысл. Работает с русским и английским текстом.

[English](#english) · [Русский](#русский)

## English

### What it does

- **Organize the message.** Put the reader's question first, choose a useful structure, and explain unfamiliar ideas with examples.
- **Remove clutter.** Replace bureaucratic phrasing and vague claims with direct language. Keep the detail the reader needs.
- **Preserve meaning.** Keep facts, conditions, negation, uncertainty, numbers, and deadlines. Do not invent missing information.
- **Use the right language.** Each language has a complete guide. Editing keeps the source language unless translation is requested; bilingual work uses both guides.

The skill contains instructions and reference material for an AI agent. It needs no books or external summaries.

### Example

After installation, ask your agent:

```text
Use $clear-writing to edit this customer email.
Keep the deadline and the condition. Return only the edited text.
"We would like to inform you that if payment is not received by 15 October,
access to the service will be suspended."
```

Example edit:

> If we do not receive payment by 15 October, we will suspend access to the service.

For other tasks, provide the text or source facts, describe the reader, and specify what must stay unchanged. For example: “Explain this API to a junior developer” or “Restructure this report so the decision comes first.”

`$clear-writing` explicitly invokes the skill in Codex. Other agents may use different invocation syntax.

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

Choose the command for your agent. Add `-g` to make the skill available across your projects. If `clear-writing` is already installed, check your local changes before replacing it.

Alternatively, use Git and copy the complete skill folder into your agent's skills directory. For a project using `.agents/skills` (POSIX shell):

```sh
git clone https://github.com/serge-masiutin/clear-writing.git clear-writing-source
mkdir -p .agents/skills
test ! -e .agents/skills/clear-writing && \
  cp -R clear-writing-source/skills/clear-writing .agents/skills/clear-writing
```

The copy runs only if the destination does not exist. **Copy the whole folder:** `SKILL.md` links to the guides and references beside it. Follow your agent's instructions for loading newly installed skills.

### Explore the guides

Start with [`SKILL.md`](skills/clear-writing/SKILL.md), which tells the agent which guide to read. Each edition includes:

| Material | English | Russian |
| --- | --- | --- |
| Complete guide | [Guide](skills/clear-writing/en/guide.md) | [Руководство](skills/clear-writing/ru/guide.md) |
| Editing techniques | [Patterns](skills/clear-writing/en/patterns.md) | [Приёмы](skills/clear-writing/ru/patterns.md) |
| Decision table | [Cheatsheet](skills/clear-writing/en/cheatsheet.md) | [Шпаргалка](skills/clear-writing/ru/cheatsheet.md) |
| Terminology | [Glossary](skills/clear-writing/en/glossary.md) | [Словарь](skills/clear-writing/ru/glossary.md) |
| Behavioral review | [Cases](skills/clear-writing/en/references/review-cases.md) | [Случаи](skills/clear-writing/ru/references/review-cases.md) |

Six topic chapters cover the reader, wording, evidence, structure, presentation, and writing formats. The agent loads the relevant chapters as needed.

To change the skill, follow the [localization review](skills/clear-writing/references/localization-review.md) and work through the review cases in both languages. These are manual checks; they do not replace reviewing the agent's output for your task.

### Basis and license

The guidance draws on «Пиши, сокращай» by Maxim Ilyakhov and Lyudmila Sarycheva (4th edition, 2024) and «Ясно, понятно» by Maxim Ilyakhov (2021). This is an independent adaptation, not an official skill by the authors. The books are not included; the rules and teaching examples were written for this skill.

[MIT license](LICENSE), copyright © 2026 Serge Masiutin. A copy of the license is included inside the installable skill folder.

## Русский

### Чем помогает

- **Выстроить объяснение.** Начать с вопроса читателя, выбрать подходящую структуру и пояснить незнакомые идеи примерами.
- **Убрать лишнее.** Заменить канцелярит и расплывчатые оценки прямыми формулировками. Сохранить подробности, которые нужны читателю.
- **Сохранить смысл.** Не потерять факты, условия, отрицания, степень уверенности, числа и сроки. Не выдумывать недостающие сведения.
- **Выбрать язык.** Для каждого языка есть полное руководство. При редактуре язык исходника сохраняется, если перевод не запрошен; для двуязычного текста используются оба руководства.

Скилл состоит из инструкций и справочных материалов для AI-агента. Книги и внешние конспекты для работы не нужны.

### Пример

После установки попросите агента:

```text
Используй $clear-writing, чтобы отредактировать письмо клиенту.
Сохрани срок и условие. Верни только чистовой текст.
«Настоящим уведомляем вас о том, что в случае непоступления оплаты
до 15 октября доступ к сервису будет приостановлен».
```

Пример редактуры:

> Если оплата не поступит до 15 октября, мы приостановим доступ к сервису.

Для других задач передайте текст или исходные факты, опишите читателя и укажите, что нельзя менять. Например: «Объясни этот API начинающему разработчику» или «Перестрой отчёт: начни с решения».

`$clear-writing` явно вызывает скилл в Codex. У других агентов синтаксис вызова может отличаться.

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

Выберите команду для своего агента. Добавьте `-g`, чтобы скилл был доступен во всех ваших проектах. Если `clear-writing` уже установлен, перед заменой проверьте свои локальные правки.

Другой способ — клонировать репозиторий через Git и скопировать папку скилла целиком. Для проекта, который использует `.agents/skills`, выполните в POSIX-совместимой оболочке:

```sh
git clone https://github.com/serge-masiutin/clear-writing.git clear-writing-source
mkdir -p .agents/skills
test ! -e .agents/skills/clear-writing && \
  cp -R clear-writing-source/skills/clear-writing .agents/skills/clear-writing
```

Копирование выполнится, только если папки назначения ещё нет. **Копируйте папку целиком:** `SKILL.md` ссылается на руководства и справочники внутри неё. Для подключения нового скилла следуйте инструкции вашего агента.

### Что внутри

Начните с [`SKILL.md`](skills/clear-writing/SKILL.md): он указывает агенту, какое руководство читать. В каждой языковой версии есть:

| Материал | Русский | English |
| --- | --- | --- |
| Полное руководство | [Руководство](skills/clear-writing/ru/guide.md) | [Guide](skills/clear-writing/en/guide.md) |
| Приёмы редактуры | [Приёмы](skills/clear-writing/ru/patterns.md) | [Patterns](skills/clear-writing/en/patterns.md) |
| Таблица выбора | [Шпаргалка](skills/clear-writing/ru/cheatsheet.md) | [Cheatsheet](skills/clear-writing/en/cheatsheet.md) |
| Термины | [Словарь](skills/clear-writing/ru/glossary.md) | [Glossary](skills/clear-writing/en/glossary.md) |
| Проверка поведения | [Случаи](skills/clear-writing/ru/references/review-cases.md) | [Cases](skills/clear-writing/en/references/review-cases.md) |

Шесть тематических глав посвящены читателю, формулировкам, доказательствам, структуре, подаче и форматам текста. Агент читает нужные главы по мере работы.

При изменении скилла пройдите [проверку локализации](skills/clear-writing/references/localization-review.md) и контрольные случаи на обоих языках. Это ручные проверки; они не заменяют оценку ответа агента в вашей задаче.

### Основа и лицензия

В основе — подходы из книг «Пиши, сокращай» Максима Ильяхова и Людмилы Сарычевой (4-е издание, 2024) и «Ясно, понятно» Максима Ильяхова (2021). Это самостоятельная адаптация, а не официальный скилл авторов. Книги в состав скилла не входят; правила и учебные примеры написаны для него.

[Лицензия MIT](LICENSE), © 2026 Serge Masiutin. Копия лицензии включена в устанавливаемую папку скилла.
