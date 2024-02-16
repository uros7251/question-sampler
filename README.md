# Question Sampler

The Question Sampler is a Python script used to sample questions from a pool of questions provided in a JSON file. The sampling can be done with or without replacement.

## JSON File Format

The JSON file should contain a list of objects, where each object represents a question. Each question object should have the following attributes:

- `question`: The text of the question.
- `answer`: The answer to the question.
- `weight` (optional): The weight of the question, reflecting its importance. This attribute only has a meaningful effect when sampling with replacement. A higher weight means a greater probability of being sampled. As an example, take a look at [questions.json](questions.json).

## Usage

To run the sampler, clone the repo, create a JSON file with questions and run:
```
$ cd path/to/folder
$ python main.py [-h] [-r] [-e] filename
```

