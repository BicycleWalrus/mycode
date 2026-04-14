#!/usr/bin/env python3
"""
flashquiz-maryland.py

A beginner-friendly flash card quiz about the great state of Maryland!
Questions are loaded from questions.json in the same directory.

Run it with:
    python3 flashquiz-maryland.py
"""

import json   # for reading the questions file
import os     # for building the file path


def load_questions(filename):
    """Read questions from a JSON file and return them as a list."""
    # Build the full path to the file, relative to this script
    script_dir = os.path.dirname(os.path.abspath(__file__))
    filepath = os.path.join(script_dir, filename)

    with open(filepath, "r") as f:
        questions = json.load(f)

    return questions


def run_quiz(questions):
    """Ask each question, check the answer, and track the score."""
    score = 0
    total = len(questions)

    print("\n🦀  Welcome to the Maryland Flash Card Quiz!  🦀")
    print("=" * 48)
    print(f"There are {total} questions. Type your best guess!\n")

    for i, card in enumerate(questions, start=1):
        question = card["question"]
        correct_answer = card["answer"]

        # Show the question number and the question
        print(f"Question {i} of {total}:")
        print(f"  {question}")

        # Get the user's answer (strip extra spaces, ignore case)
        user_answer = input("  Your answer: ").strip()

        # Compare answers (case-insensitive for fairness)
        if user_answer.lower() == correct_answer.lower():
            print("  ✅  Correct!\n")
            score += 1
        else:
            print(f"  ❌  Not quite. The answer is: {correct_answer}\n")

    return score, total


def show_final_score(score, total):
    """Display the final score with a friendly message."""
    print("=" * 48)
    print(f"🏁  Quiz complete! You scored {score} out of {total}.")

    # Give a fun message based on how well the user did
    percentage = score / total * 100
    if percentage == 100:
        print("🎉  Perfect score! You really know your Maryland!")
    elif percentage >= 70:
        print("👍  Great job! You know Maryland pretty well.")
    elif percentage >= 40:
        print("📚  Not bad! A little more studying and you'll be an expert.")
    else:
        print("🦀  Keep exploring Maryland — there's so much to learn!")
    print("=" * 48)


def main():
    # Load questions from the JSON file
    questions = load_questions("questions.json")

    # Run the quiz and get the score
    score, total = run_quiz(questions)

    # Show the final result
    show_final_score(score, total)


# Only run main() when this file is executed directly
if __name__ == "__main__":
    main()
