from abc import ABC, abstractmethod
import inquirer


class Question(ABC):
    def __init__(self):
        self._id = None
        self._message = None
        self._subquestions = None

    def with_id(self, id):
        self._id = id
        return self

    def with_message(self, message):
        self._message = message
        return self


class MultipleChoicesQuestion(Question):
    def __init__(self):
        super().__init__()
        self._choices = []

    def with_action(self, action):
        self._choices.append(action)
        return self

    def build(self):
        return inquirer.List(
            self._id,
            message = self._message,
            choices = self._choices
        )

class ValidationQuestion(Question):
    def __init__(self):
        super().__init__()



    def build(self):
        return inquirer.Confirm(
            self._id, 
            message=self._message
        )


class InputQuestion(Question):
    def __init__(self):
        super().__init__()



    def build(self):
        return inquirer.Text(
            self._id, 
            message=self._message
        )
