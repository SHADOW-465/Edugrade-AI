"""
Grading agent for the EduGrade AI application.

This agent is responsible for grading the extracted text from the answer
sheets using a large language model.
"""

from .base_agent import BaseAgent
from typing import List, Dict, Any
import openai
import json
from ..utils.prompt_templates import GRADING_PROMPT

class GradingAgent(BaseAgent):
    """
    Agent for grading student answers.

    This agent uses a large language model to grade the extracted text from
    the answer sheets based on the provided rubric.
    """
    def __init__(self, api_key: str, model: str = "gpt-4o"):
        """
        Initializes the grading agent.

        Args:
            api_key: The API key for the language model service.
            model: The name of the language model to use.
        """
        super().__init__("grading_agent")
        self.client = openai.OpenAI(api_key=api_key)
        self.model = model

    def grade_answer(
        self,
        student_answer: str,
        model_answer: str,
        rubric: str,
        max_marks: int,
        subject: str
    ) -> Dict[str, Any]:
        """
        Grades a single answer.

        Args:
            student_answer: The student's answer.
            model_answer: The model answer.
            rubric: The rubric for the question.
            max_marks: The maximum marks for the question.
            subject: The subject of the exam.

        Returns:
            A dictionary containing the grade, feedback, and reasoning.
        """
        prompt = GRADING_PROMPT.format(
            subject=subject,
            student_answer=student_answer,
            model_answer=model_answer,
            rubric=rubric,
            max_marks=max_marks
        )
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are an expert exam evaluator."},
                    {"role": "user", "content": prompt},
                ],
                response_format={"type": "json_object"},
                temperature=0.3
            )
            return json.loads(response.choices[0].message.content)
        except Exception as e:
            self.logger.error(f"Error grading answer: {e}")
            return {
                "score": 0,
                "points_covered": [],
                "points_missed": ["Error in grading process"],
                "feedback": "Could not grade this answer due to an internal error.",
                "reasoning": str(e),
            }

    def batch_grade(self, answers: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Grades a batch of answers.

        Args:
            answers: A list of dictionaries, where each dictionary contains
                     the student's answer, the model answer, the rubric, and
                     the maximum marks for a question.

        Returns:
            A list of dictionaries, where each dictionary contains the grade,
            feedback, and reasoning for an answer.
        """
        graded_answers = []
        for answer in answers:
            graded_answer = self.grade_answer(
                student_answer=answer["student_answer"],
                model_answer=answer["model_answer"],
                rubric=answer["rubric"],
                max_marks=answer["max_marks"],
                subject=answer["subject"]
            )
            graded_answers.append(graded_answer)
        return graded_answers

    def process(self, answers_to_grade: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Processes a list of answers to grade.

        Args:
            answers_to_grade: A list of dictionaries, where each dictionary
                              contains the student's answer, the model answer,
                              the rubric, and the maximum marks for a question.

        Returns:
            A dictionary containing the graded results and the status of the
            operation.
        """
        try:
            graded_results = self.batch_grade(answers_to_grade)
            return {
                "grades": graded_results,
                "status": "success"
            }
        except Exception as e:
            self.logger.error(f"Error in batch grading process: {e}")
            return {
                "grades": [],
                "status": "error",
                "error_message": str(e)
            }
