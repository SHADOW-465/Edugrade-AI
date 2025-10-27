"""
Feedback agent for the EduGrade AI application.

This agent is responsible for generating personalized feedback for students
and class-level insights for teachers.
"""

from .base_agent import BaseAgent
from typing import List, Dict, Any
import openai
import json
from ..utils.prompt_templates import FEEDBACK_PROMPT, CLASS_INSIGHTS_PROMPT

class FeedbackAgent(BaseAgent):
    """
    Agent for generating feedback.

    This agent uses a large language model to generate personalized feedback
    for students based on their performance and to generate class-level
    insights for teachers.
    """
    def __init__(self, api_key: str, model: str = "gpt-4o"):
        """
        Initializes the feedback agent.

        Args:
            api_key: The API key for the language model service.
            model: The name of the language model to use.
        """
        super().__init__("feedback_agent")
        self.client = openai.OpenAI(api_key=api_key)
        self.model = model

    def generate_feedback(
        self,
        student_name: str,
        grade_results: List[Dict[str, Any]],
        overall_score: float,
        max_score: float
    ) -> str:
        """
        Generates personalized feedback for a student.

        Args:
            student_name: The name of the student.
            grade_results: A list of the student's grade results.
            overall_score: The student's overall score.
            max_score: The maximum possible score.

        Returns:
            The personalized feedback for the student.
        """
        question_breakdown = ""
        for grade in grade_results:
            question_breakdown += f"- Question {grade['question_number']}: {grade['score']}/{grade['max_marks']}\n"

        prompt = FEEDBACK_PROMPT.format(
            student_name=student_name,
            total_score=overall_score,
            max_total_score=max_score,
            num_questions=len(grade_results),
            question_breakdown=question_breakdown
        )
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are a helpful and encouraging teacher."},
                    {"role": "user", "content": prompt},
                ],
                temperature=0.7
            )
            return response.choices[0].message.content
        except Exception as e:
            self.logger.error(f"Error generating feedback for {student_name}: {e}")
            return "Could not generate feedback due to an internal error."

    def generate_class_insights(self, all_grades: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Generates class-level insights.

        Args:
            all_grades: A list of all the grades for the class.

        Returns:
            A dictionary containing the class-level insights.
        """
        prompt = CLASS_INSIGHTS_PROMPT.format(all_grades_json=json.dumps(all_grades))
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are an expert data analyst for educational data."},
                    {"role": "user", "content": prompt},
                ],
                response_format={"type": "json_object"},
                temperature=0.5
            )
            return json.loads(response.choices[0].message.content)
        except Exception as e:
            self.logger.error(f"Error generating class insights: {e}")
            return {"error": "Could not generate class insights."}

    def process(self, grading_results: Dict[str, Any]) -> Dict[str, Any]:
        """
        Processes the grading results to generate feedback.

        Args:
            grading_results: A dictionary containing the grading results.

        Returns:
            A dictionary containing the grading results with the feedback
            added and the status of the operation.
        """
        try:
            feedback = self.generate_feedback(
                student_name=grading_results["student_name"],
                grade_results=grading_results["grades"],
                overall_score=grading_results["overall_score"],
                max_score=grading_results["max_score"]
            )
            grading_results["feedback"] = feedback
            return {
                "results_with_feedback": grading_results,
                "status": "success"
            }
        except Exception as e:
            self.logger.error(f"Error in feedback generation process: {e}")
            return {
                "results_with_feedback": None,
                "status": "error",
                "error_message": str(e)
            }
