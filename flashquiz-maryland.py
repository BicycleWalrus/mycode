#!/usr/bin/env python3
"""
flashquiz-maryland.py

A beginner-friendly flash card quiz about the great state of Maryland!

The quiz prefers the richer source file 'maryland_quiz_source.json' when it
exists in the same directory.  If that file is not found it falls back to the
simpler 'questions.json' format.

Run it with:
    python3 flashquiz-maryland.py
"""

import json    # for reading JSON data files
import os      # for building file paths
import random  # for shuffling questions and picking templates
import sys     # for exiting cleanly on errors


# ---------------------------------------------------------------------------
# File loading helpers
# ---------------------------------------------------------------------------

def load_json_file(filepath):
    """
    Open a JSON file and return its contents as a Python object.
    Returns None (and prints a message) if the file is missing or unreadable.
    """
    if not os.path.exists(filepath):
        return None  # caller will handle the missing-file case

    try:
        with open(filepath, "r") as f:
            return json.load(f)
    except json.JSONDecodeError as e:
        print(f"\n⚠️  The file '{filepath}' has invalid JSON and cannot be read.")
        print(f"   Details: {e}")
        sys.exit(1)  # stop cleanly instead of showing a long traceback


# ---------------------------------------------------------------------------
# Converting the rich source dataset into simple quiz cards
# ---------------------------------------------------------------------------

# The 'maryland_quiz_source.json' file has a list of 'facts'.
# Each fact looks like this:
#
#   {
#     "id": "md-capital",
#     "category": "government",
#     "difficulty": "easy",
#     "fact": "The capital city of Maryland is Annapolis.",
#     "question_templates": [
#         "What is the capital city of Maryland?",
#         "Which city is the capital of Maryland?"
#     ],
#     "answer": "Annapolis",
#     "aliases": []          <-- other accepted spellings / short forms
#   }
#
# We pick ONE question_template per fact (randomly) and build a simple card
# that the rest of the program can use.

def facts_to_cards(facts):
    """
    Convert a list of fact objects from maryland_quiz_source.json into a
    list of simple quiz-card dictionaries, each with:
        - 'question'   : the question string to show the user
        - 'answer'     : the main correct answer
        - 'aliases'    : list of other accepted answer strings
        - 'difficulty' : 'easy', 'medium', or 'hard'
    """
    cards = []
    for fact in facts:
        # Make sure the required fields are present before using them
        if "question_templates" not in fact or "answer" not in fact:
            continue  # skip incomplete facts silently

        templates = fact["question_templates"]
        if not templates:
            continue  # no question to ask — skip this fact

        # Pick one template at random so the quiz feels fresh each run
        question = random.choice(templates)

        card = {
            "question":   question,
            "answer":     fact["answer"],
            "aliases":    fact.get("aliases", []),  # default to empty list
            "difficulty": fact.get("difficulty", "easy"),
        }
        cards.append(card)

    return cards


# ---------------------------------------------------------------------------
# Loading quiz cards from whichever file is available
# ---------------------------------------------------------------------------

def load_quiz_cards():
    """
    Try to load quiz cards from the richer source file first.
    Fall back to questions.json if the source file is not found.

    Returns a list of quiz-card dictionaries.
    """
    script_dir = os.path.dirname(os.path.abspath(__file__))

    # --- Try the richer source file first ---
    source_path = os.path.join(script_dir, "maryland_quiz_source.json")
    source_data = load_json_file(source_path)

    if source_data is not None:
        # Validate that the expected 'facts' key exists
        if "facts" not in source_data or not isinstance(source_data["facts"], list):
            print("\n⚠️  'maryland_quiz_source.json' is missing the 'facts' list.")
            sys.exit(1)

        print("  (Using maryland_quiz_source.json)")
        return facts_to_cards(source_data["facts"])

    # --- Fall back to the simple questions.json format ---
    fallback_path = os.path.join(script_dir, "questions.json")
    fallback_data = load_json_file(fallback_path)

    if fallback_data is None:
        print("\n⚠️  Neither 'maryland_quiz_source.json' nor 'questions.json' was found.")
        print("   Please make sure at least one of these files is in the same folder.")
        sys.exit(1)

    if not isinstance(fallback_data, list):
        print("\n⚠️  'questions.json' does not contain a valid list of questions.")
        sys.exit(1)

    print("  (Using questions.json)")

    # The simple format has 'question' and 'answer' but no aliases or difficulty.
    # Add defaults so the rest of the code works the same way for both formats.
    for card in fallback_data:
        card.setdefault("aliases", [])
        card.setdefault("difficulty", "easy")

    return fallback_data


# ---------------------------------------------------------------------------
# Answer checking
# ---------------------------------------------------------------------------

def is_correct(user_answer, card):
    """
    Return True if user_answer matches the card's main answer OR any alias.
    Comparison is case-insensitive and ignores leading/trailing whitespace.
    """
    # Normalise the user's input once
    user = user_answer.strip().lower()

    # Check the main answer
    if user == card["answer"].strip().lower():
        return True

    # Check each alias
    for alias in card.get("aliases", []):
        if user == alias.strip().lower():
            return True

    return False


# ---------------------------------------------------------------------------
# Difficulty filtering
# ---------------------------------------------------------------------------

def ask_difficulty():
    """
    Ask the user which difficulty level they want to play.
    Returns a set of difficulty strings that should be included.
    """
    print("\nChoose a difficulty level:")
    print("  1 - All questions")
    print("  2 - Easy only")
    print("  3 - Easy + Medium")

    choice = input("Enter 1, 2, or 3 (default: 1 — all): ").strip()

    if choice == "2":
        print("  Difficulty: Easy only\n")
        return {"easy"}
    elif choice == "3":
        print("  Difficulty: Easy + Medium\n")
        return {"easy", "medium"}
    else:
        # Default to all questions for any other input (including blank)
        if choice not in ("1", ""):
            print("  (Invalid choice — showing all questions)")
        else:
            print("  Difficulty: All questions\n")
        return {"easy", "medium", "hard"}


def filter_by_difficulty(cards, allowed_difficulties):
    """Return only the cards whose difficulty is in allowed_difficulties."""
    return [c for c in cards if c.get("difficulty", "easy") in allowed_difficulties]


# ---------------------------------------------------------------------------
# Quiz runner
# ---------------------------------------------------------------------------

def run_quiz(cards):
    """Ask each question in order, check answers, and return the score."""
    score = 0
    total = len(cards)

    print("\n🦀  Welcome to the Maryland Flash Card Quiz!  🦀")
    print("=" * 50)
    print(f"There are {total} questions. Type your best guess!\n")

    for i, card in enumerate(cards, start=1):
        print(f"Question {i} of {total}:")
        print(f"  {card['question']}")

        user_answer = input("  Your answer: ").strip()

        if is_correct(user_answer, card):
            print("  ✅  Correct!\n")
            score += 1
        else:
            # Show the main answer so the user can learn from the mistake
            print(f"  ❌  Not quite. The answer is: {card['answer']}\n")

    return score, total


# ---------------------------------------------------------------------------
# Final score display
# ---------------------------------------------------------------------------

def show_final_score(score, total):
    """Display the final score, percentage, and an encouraging message."""
    percentage = round(score / total * 100)

    print("=" * 50)
    print(f"🏁  Quiz complete!")
    print(f"    You got {score} out of {total} correct  ({percentage}%)")

    if percentage == 100:
        print("🎉  Perfect score! You really know your Maryland!")
    elif percentage >= 70:
        print("👍  Great job! You know Maryland pretty well.")
    elif percentage >= 40:
        print("📚  Not bad! A little more studying and you'll be an expert.")
    else:
        print("🦀  Keep exploring Maryland — there's so much to learn!")

    print("=" * 50)


# ---------------------------------------------------------------------------
# Main program flow
# ---------------------------------------------------------------------------

def main():
    # Step 1: Load quiz cards (prefers maryland_quiz_source.json)
    all_cards = load_quiz_cards()

    # Step 2: Ask the user which difficulty level they want
    allowed = ask_difficulty()

    # Step 3: Filter to only the chosen difficulty
    cards = filter_by_difficulty(all_cards, allowed)

    if not cards:
        print("⚠️  No questions matched the selected difficulty. Exiting.")
        sys.exit(0)

    # Step 4: Shuffle so the order is different every run
    random.shuffle(cards)

    # Step 5: Run the quiz
    score, total = run_quiz(cards)

    # Step 6: Show the final result
    show_final_score(score, total)


# Only run main() when this file is executed directly (not when imported)
if __name__ == "__main__":
    main()
