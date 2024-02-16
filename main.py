# Import the json module
import json
# Import the argparse module
import argparse
# Import sampler
from sampler import QuestionSampler

def run_sampler(filename: str, with_replacement: bool, equal_weights: bool) -> None:
    """
    Run the question sampler.

    Parameters:
    - filename (str): The path to the file containing the list of questions in JSON format.
    - with_replacement (bool): Whether to sample questions with replacement.
    - equal_weights (bool): Whether to assign equal weights to all questions.
    """
    try:
        qs = QuestionSampler(filename, with_replacement, equal_weights)
    except FileNotFoundError:
        print("File not found:", filename)
        exit()
    except json.JSONDecodeError:
        print("Invalid JSON format in file:", filename)
        exit()
    except KeyError as e:
        print("Column", e, "is missing in the file:", filename)
        exit()

    question = {
        "question": None,
        "answer": None
    }
    print("Welcome to the question and answer game!")
    print("To exit the game, press Ctrl + D (Unix) or Ctrl + Z (Windows) and then ENTER.")
    print("Press ENTER to open the next question/reveal the answer to the current question.")
    while True:
        try:
            input()
        except EOFError:
            break
        if question['question'] is None:
            question = qs.sample()
            print("Q:", question['question'])
        else:
            print("A:", question['answer'])
            question['question'] = None

def main(args):
    # Call the run_sampler function with the provided arguments
    run_sampler(args.filename, args.with_replacement, args.equal_weights)

if __name__ == "__main__":
    # Create an ArgumentParser object
    parser = argparse.ArgumentParser()

    # Add a positional argument for the filepath
    parser.add_argument("filename", help="the path of the json file with questions and answers")
    # Add an optional argument for the "-r" option
    parser.add_argument("-r", "--with-replacement", help="use sampling with replacement", action="store_true")
    # Add an optional argument for the "-e" option
    parser.add_argument("-e", "--equal-weights", help="use equal weights", action="store_true")

    # Parse the arguments from the command line
    args = parser.parse_args()

    # Call main function with the parsed arguments
    main(args)
        