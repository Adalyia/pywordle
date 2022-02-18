import sys
import random
import importlib.resources as pkg_resources
from collections import Counter

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

    def __init__(self, guesses: list = None, max_guess_attempts: int = None, answer: str = None):
        self._words: list = [g.replace('\n', '').upper() for g in pkg_resources.files(__package__).joinpath('answers.txt').read_text().splitlines()]
        self._dictionary: list = [g.replace('\n', '').upper() for g in pkg_resources.files(__package__).joinpath('guesses.txt').read_text().splitlines()] + self._words
        self._alphabet: list = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K',
                               'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
        
        self._guesses: list = [g.upper() for g in guesses] if guesses is not None else []
        self._max_guess_attempts: int = max_guess_attempts if max_guess_attempts is not None else 6
        self._answer: str = answer.upper() if answer is not None and len(answer) == 5 and answer.upper() in self._words else random.choice(self._words)

        self._greeting = """Guess the WORDLE!

Each guess must be a valid five-letter word. Hit the enter button to submit.

After each guess, the colour of the tiles will change to show how close your guess was to the word.

Type quit/exit at any time to close the game.
        """

        self._example_data = [
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

        for guess in self._guesses:
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

        return [l for l in self._alphabet if l not in self.used_letters]

    @property
    def completed(self) -> bool:
        """Whether the game is completed/guess attempts have been exhausted

        :return: Whether there's any remaining guess attempts allowed
        :rtype: bool
        """
        return len(self._guesses) >= self._max_guess_attempts

    @property
    def winner(self) -> bool:
        """Whether or not the game has been won/the wordle has been guessed.

        :return: Whether the game has been won or not
        :rtype: bool
        """

        return self._answer in self._guesses

    @property
    def guess_table(self) -> str:
        """Returns a colourized table of the guesses made in the current game

        :return: A colourized table of guesses
        :rtype: str
        """

        return tabulate([self.colourize(graded_guess) for graded_guess in [self.grade_guess(guess) for guess in self._guesses]], tablefmt="pretty")

    @property
    def example_table(self) -> str:
        """Returns a colourized table showing gameplay examples
        
        :return: A colourized table of gameplay examples
        :rtype: str
        """

        return tabulate(self._example_data, tablefmt="pretty")
    
    def grade_guess(self, input: str) -> list:
        """Grade each letter of a guess from 0-2 for Miss, Partial, and True match

        :param guess: The guess to grade as a string
        :type guess: str
        :return: A graded list of the letters in a guess
        :rtype: list
        """
        letter_data = [None for letter in input]
        
        letter_count = Counter(self._answer)
        
        # First iterate through our list giving any true match a grade of 2
        for i in range(len(letter_data)):
            if input[i] == self._answer[i]:
                letter_data[i] = [input[i],2]
                letter_count[input[i]] -= 1
        
        # Next re-iterate the list and mark any partial matches up to the number of times said letter appears in the answer as grade 1
        for i in range(len(letter_data)):
            if input[i] in self._answer and input[i] != self._answer[i] and letter_count[input[i]] > 0:
                letter_data[i] = [input[i],1]
                letter_count[input[i]] -= 1
            elif letter_data[i] is None:
                # And any remaining as 0
                letter_data[i] = [input[i],0]
        
        return letter_data
    
    def colourize(self, input: list) -> list:
        """Returns a list of letters coloured for the console/terminal

        :param input: A graded list of letters to be colourized
        :type input: list
        :return: A list of colourized characters
        :rtype: list
        """
        
                
        return [colored(l[0], self.get_colour(l[1])) for l in input]
    
    def get_colour(self, grade: int) -> str:
        """Convert colour grade to a termcolor colour string

        :param grade: A colour grade
        :type grade: int
        :return: Termcolor colour string
        :rtype: str
        """
        
        colours = {
            0: "grey",
            1: "yellow",
            2: "green"
        }
        
        return colours[grade] if grade in colours else "grey"

    def make_guess(self, guess: str) -> bool:
        """Attempts to make an additional guess as to the correct word

        :param guess: The guess to enter
        :type guess: str
        :return: Whether the guess was made successfully
        :rtype: bool
        """

        guess = guess.upper()
        
        if self.validate_guess(guess):
            self._guesses.append(guess)
            return True
        
        return False

    def validate_guess(self, guess: str) -> bool:
        """Validates a user's guess

        :param guess: The guess to enter
        :type guess: str
        :return: Whether the guess is valid
        :rtype: bool
        """
        
        if not self.completed and (guess in self._dictionary):
            return True
        
        return False 

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
            if guess != "":
                print(colored(guess, "red"), "is not a valid 5-letter word.")
                
            return self.guess_prompt()

        return guess

    def play(self):
        """Advances/begins a Wordle game with the current parameters/state in textual format
        """

        print(self._greeting)
        print(self.example_table)

        if len(self._guesses) > 0:
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
                  colored(self._answer, "green"))



