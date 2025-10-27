"""
Feedback agent for the EduGrade AI application.

This agent is responsible for generating personalized feedback for students
and class-level insights for teachers.
"""

from .base_agent import BaseAgent
from typing import List, Dict, Any
import google.generativeai as genai
import json
from ..utils.prompt_templates import FEEDBACK_PROMPT, CLASS_INSIGHTS_PROMPT
import re

class FeedbackAgent(BaseAgent):
    """
    Agent for generating feedback.

    This agent uses a large language model to generate personalized feedback
    for students based on their performance and to generate class-level
    insights for teachers.
    """
    def __init__(self, api_key: str, model: str = "gemini-pro"):
        """
        Initializes the feedback agent.

        Args:
            api_key: The API key for the language model service.
            model: The name of the language model to use.
        """
        super().__init__("feedback_agent")
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel(model)

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
            full_prompt = f"You are a helpful and encouraging teacher.\n\n{prompt}"
            response = self.model.generate_content(
                full_prompt,
                generation_config=genai.types.GenerationConfig(
                    temperature=0.7
                )
            )
            return response.text
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
            full_prompt = f"You are an expert data analyst for educational data.\n\n{prompt}"
            response = self.model.generate_content(
                full_prompt,
                generation_config=genai.types.GenerationConfig(
                    temperature=0.5
                )
            )

            # Extracting the json string which is wrapped in ```json ```
            match = re.search(r"```json\n(.*)\n```", response.text, re.DOTALL)
            if match:
                json_string = match.group(1).strip()
            else:
                json_string = response.text.strip()

            return json.loads(json_string)
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
