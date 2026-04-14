# mycode
Tracking my Code

---

## 🦀 Maryland Flash Card Quiz

A beginner-friendly command-line quiz about the state of Maryland!

### Files
| File | Description |
|---|---|
| `flashquiz-maryland.py` | The quiz program |
| `maryland_quiz_source.json` | Richer source dataset (preferred) |
| `questions.json` | Simple fallback question list |

### How to Run

1. Make sure you have Python 3 installed:
   ```bash
   python3 --version
   ```

2. Run the quiz from the terminal:
   ```bash
   python3 flashquiz-maryland.py
   ```

3. Choose a difficulty level when prompted (Easy / Easy+Medium / All).

4. Type your answer and press **Enter** for each question.

5. Your final score and percentage are shown at the end. Good luck! 🏁

### Which data file is used?

The program looks for `maryland_quiz_source.json` first.  If that file exists
(it does by default), it is used and `questions.json` is ignored.  If the
source file is ever removed, the program automatically falls back to
`questions.json`.

### How questions are chosen

`maryland_quiz_source.json` contains a `facts` list.  Each fact has several
`question_templates` — different ways to ask the same question.  The program
picks **one template at random** per fact every time you run the quiz, so the
wording can vary between sessions.

### How aliases work

Some answers can be written in more than one way.  For example, the answer
"Blue Crab" also accepts "Blue Crabs" or "Maryland Blue Crab".  These
alternatives are stored in the `aliases` list for each fact.  The program
accepts the main `answer` **or** any alias, and the comparison is always
case-insensitive with leading/trailing spaces ignored.

### Requirements
- Python 3 (no extra packages needed — uses only the standard library)
- `maryland_quiz_source.json` (or `questions.json`) must be in the same folder
  as `flashquiz-maryland.py`
