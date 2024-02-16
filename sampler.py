import json
import random

class Question:
    question: str
    answer: str
    weight: float

    def __init__(self, question: str, answer: str, weight: float = 1):
        """
        Initialize a Question object.
        
        Parameters:
        - question (str): The question text.
        - answer (str): The answer text.
        - weight (float): The weight of the question (default: 1).
        """
        self.question = question
        self.answer = answer
        self.weight = weight
    
    @staticmethod
    def from_dict(data: dict) -> 'Question':
        """
        Create a Question object from a dictionary.
        """
        return Question(data['question'], data['answer'], data['weight']) if 'weight' in data else Question(data['question'], data['answer'])


class QuestionSampler:
    cdf: list[float]
    _n: int 
    questions: list[Question]
    with_replacement: bool
    equal_weights: bool

    def __init__(self, filename: str, with_replacement: bool = False, equal_weights: bool = False):
        """
        Initialize a QuestionSampler object.

        Parameters:
        - filename (str): The path to the file containing the list of questions in JSON format.
        - with_replacement (bool): Whether to sample questions with replacement (default: False).
        - equal_weights (bool): Whether to assign equal weights to all questions (default: False).
        """
        self.with_replacement = with_replacement
        self.equal_weights = equal_weights
        with open(filename, "r") as f:
            # Parse the file using json.load and assign it to a variable
            list_of_questions = json.load(f)
            assert isinstance(list_of_questions, list)
            # Create a list of Question objects from the list of dictionaries
            self.questions = [Question.from_dict(q) for q in list_of_questions]
            # Initialize cdf and n
            self.reset()
    

    def sample(self) -> dict[str, str]:
        """
        Sample a question from the question pool.

        Returns:
        - dict[str, str]: A dictionary containing the sampled question and its answer.
        """
        random_value = random.uniform(0, self.cdf[self._n - 1])
        index = self._upper_bound(random_value)
        question = self.questions[index]
        result = {'question': question.question, 'answer': question.answer}
        if not self.with_replacement:
            if self._n > 1:
                # move the question to the back and decrease the size of the list
                self._remove_from_pool(index)
            else:
                # if there is only one question left, reset the sampler
                self.reset()
        return result
    
    def reset(self) -> None:
        """
        Reset the question sampler.

        This method resets the internal state of the question sampler, allowing it to sample questions again.
        """
        self._n = len(self.questions)
        # Create a list of floats representing the cumulative distribution function
        if self.equal_weights:
            self.cdf = [i + 1 for i in range(self._n)]
        else:
            self.cdf = [q.weight for q in self.questions]
            for i in range(1, len(self.cdf)):
                self.cdf[i] += self.cdf[i - 1]

    def _remove_from_pool(self, index: int) -> None:
        """
        Remove a question from the question pool.

        This method removes the question at the given index from the question pool and updates the cumulative distribution function (cdf) accordingly.

        Parameters:
        - index (int): The index of the question to be removed.
        """
        self._n -= 1
        # swap the last element with the element at index
        self.questions[index], self.questions[self._n] = self.questions[self._n], self.questions[index]
        # if the weights are equal, no need to update the cdf
        if self.equal_weights or self.questions[index].weight == self.questions[self._n].weight:
            return
        # update the cdf from index to n
        for i in range(index, self._n):
            self.cdf[i] += self.questions[index].weight - self.questions[self._n].weight
    
    def _upper_bound(self, value: float) -> int:
        """
        Find the index of the first element in the cdf that is greater than or equal to value.

        This method performs a binary search on the cumulative distribution function (cdf) to find the index of the first element that is greater than or equal to the given value.

        Parameters:
        - value (float): The value to search for in the cdf.

        Returns:
        - int: The index of the first element in the cdf that is greater than or equal to value.
        """
        low = 0
        high = self._n - 1

        while low <= high:
            mid = (low + high) // 2

            if self.cdf[mid] >= value:
                if mid == 0 or self.cdf[mid - 1] < value:
                    return mid
                else:
                    high = mid - 1
            else:
                low = mid + 1

        return self._n - 1
