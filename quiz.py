"""A CLI quiz game implemented in Python."""

from requests import get
from html import unescape
from random import shuffle

BASE_URL = "https://opentdb.com/api.php"


class Question:
    """A class that represents a single question."""

    def __init__(self, question_dict: dict):
        """Create a new question instance."""

        self.question_type = question_dict["type"]
        self.category = question_dict["category"]
        self.difficulty = question_dict["difficulty"]

        self.question_text = unescape(question_dict["question"])
        self.correct_answer = unescape(question_dict["correct_answer"])
        self.answers = [unescape(q)
                        for q in question_dict["incorrect_answers"]]

        self.answers.append(self.correct_answer)
        shuffle(self.answers)

    def __str__(self):
        return f"<Question ({self.category}, {self.difficulty})>"

    def __repr__(self):
        return self.__str__()

    def display(self):
        """Display the question details."""
        print("---")
        print(self.question_text)
        print("---")

        for i, a in enumerate(self.answers):
            print(f"{i + 1}. {a}")

        print("---\n")

    def validate_answer(self, other: str) -> bool:
        """Return if a given answer is correct."""
        return other == self.correct_answer

    def pose(self) -> bool:
        """Prompts the user to answer a question and returns
        whether or not they were correct."""

        self.display()

        user_answer = -1
        while user_answer not in range(1, len(self.answers) + 1):
            user_answer = int(input("Enter answer number: "))
            # Add error handling
            # Extract input section to method

        user_answer = self.answers[user_answer - 1]

        return self.validate_answer(user_answer)


def get_questions(number: int = 5,
                  difficulty: str = "medium") -> list[Question]:
    """Return a set of quiz questions from the API."""
    res = get(f"{BASE_URL}?amount={number}&difficulty={difficulty}", timeout=10)
    return [Question(question_dict=q) for q in res.json()["results"]]


if __name__ == "__main__":
    questions = get_questions(number=10, difficulty="hard")
    for question in questions:
        print(question.pose())
