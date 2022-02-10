import os
import sys
import random

# Console imports, these are only necessary for playing from the terminal
from termcolor import colored
from tabulate import tabulate


class Wordle:
    """A representation of the popular game Wordle in Python

    :param guesses: A list of guesses in the current Wordle game - Used to load games in progress
    :type guesses: list
    :param max_guess_attempts: The maximum number of allowed attempts/guesses
    :type max_guess_attempts: int
    :param answer: The answer to the current Wordle game - Used to load games in progress
    :type answer: str
    """

    def __init__(self, *args, **kwargs):
        self.guesses: list = [
            g.upper() for g in kwargs['guesses']] if 'guesses' in kwargs else []
        self.max_guess_attempts: int = kwargs['max_guess_attempts'] if 'max_guess_attempts' in kwargs else 6
        self.words: list = [g.replace('\n', '').upper() for g in open(
            os.path.join(os.path.dirname(__file__), 'answers.txt'), 'r').readlines()]
        self.dictionary: list = [g.replace('\n', '').upper() for g in open(os.path.join(
            os.path.dirname(__file__), 'guesses.txt'), 'r').readlines()] + self.words
        self.alphabet: list = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K',
                               'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
        self.answer: str = kwargs['answer'].upper() if 'answer' in kwargs and kwargs['answer'].upper(
        ) in self.words else random.choice(self.words)

        self.greeting = """Guess the WORDLE!

Each guess must be a valid five-letter word. Hit the enter button to submit.

After each guess, the color of the tiles will change to show how close your guess was to the word.

Type quit/exit at any time to close the game.
        """

        self.example_data = [
            [colored("W", "green"), colored("E", "grey"), colored("A", "grey"), colored(
                "R", "grey"), colored("Y", "grey"), "The letter W is in the word and in the correct spot."],
            [colored("P", "grey"), colored("I", "yellow"), colored("L", "grey"), colored(
                "L", "grey"), colored("S", "grey"), "The letter I is in the word but in the wrong spot."],
            [colored("V", "grey"), colored("A", "grey"), colored("G", "grey"), colored(
                "U", "grey"), colored("E", "grey"), "Grey letters aren't used in any spots."]
        ]

    @property
    def used_letters(self) -> list:
        """The letters used in guesses by the user

        :return: The letters used in guesses thus far
        :rtype: list
        """

        used = []

        for guess in self.guesses:
            for letter in guess:
                if letter not in used:
                    used.append(letter)

        return used

    @property
    def unused_letters(self) -> list:
        """The letters not yet guessed

        :return: Letters not used in guesses
        :rtype: list
        """

        return [l for l in self.alphabet if l not in self.used_letters]

    @property
    def completed(self) -> bool:
        """Whether the game is completed/guess attempts have been exhausted

        :return: Whether there's any remaining guess attempts allowed
        :rtype: bool
        """
        return len(self.guesses) >= self.max_guess_attempts

    @property
    def winner(self) -> bool:
        """Whether or not the game has been won/the wordle has been guessed.

        :return: Whether the game has been won or not
        :rtype: bool
        """

        return self.answer in self.guesses

    @property
    def guess_table(self) -> str:
        """Returns a colorized table of the guesses made in the current game

        :return: A colorized table of guesses
        :rtype: str
        """

        return tabulate([self.colorize(guess) for guess in self.guesses], tablefmt="pretty")

    @property
    def example_table(self) -> str:
        """Returns a colorized table showing gameplay examples

        :return: A colorized table of gameplay examples
        :rtype: str
        """

        return tabulate(self.example_data, tablefmt="pretty")

    def make_guess(self, guess: str):
        """Attempts to make an additional guess as to the correct word

        :param guess: The guess to enter
        :type guess: str
        :return: Whether the guess was made successfully
        :rtype: bool
        """

        self.guesses.append(guess.upper())

    def validate_guess(self, guess: str) -> bool:
        """Validates a user's guess

        :param guess: The guess to enter
        :type guess: str
        :return: Whether the guess is valid
        :rtype: bool
        """
        if not self.completed and (guess.upper() in self.dictionary):
            return True

        return False

    def colorize(self, input: str) -> list:
        """Returns a list of letters coloured

        :param input: The word or guess to be colorized based on the game's answer
        :type input: str
        :return: A list of colorized characters
        :rtype: list
        """
        if self.answer is None:
            return None

        letters = [l for l in input]
        colored_letters = []

        for i in range(5):
            if letters[i] in self.answer:
                colored_letters.append(colored(
                    letters[i], "green") if letters[i] == self.answer[i] else colored(letters[i], "yellow"))
            else:
                colored_letters.append(colored(letters[i], "grey"))

        return colored_letters

    def guess_prompt(self) -> str:
        """Prompt the user to enter a guess in the console

        :return: The validated and capitalized guess
        :rtype: str
        """
        guess = input("Please enter a guess: ").upper()

        if guess == "EXIT" or guess == "QUIT":
            print("Goodbye! Thanks for playing!")
            sys.exit()

        if not self.validate_guess(guess):
            print(colored(guess, "red"), "is not a valid 5-letter word.")
            return self.guess_prompt()

        return guess

    def play(self):
        """Advances/begins a Wordle game with the current parameters/state in textual format
        """

        print(self.greeting)
        print(self.example_table)

        if len(self.guesses) > 0:
            print(self.guess_table)

        while not self.completed and not self.winner:
            print("Your used letters are", ",".join(self.used_letters))
            print("Your unused letters are", ",".join(self.unused_letters))

            guess = self.guess_prompt()
            self.make_guess(guess)

            print(self.guess_table)

        if self.winner:
            print(colored("Congratulations, you won!"))
        else:
            print("Better luck next time! The correct word was:",
                  colored(self.answer, "green"))


if __name__ == "__main__":
    try:
        game = Wordle()
        game.play()
    except KeyboardInterrupt:
        pass
