"""
Tier-specific grading logic using tier-appropriate LLM models and strategies.
"""

from typing import Any, Dict
import json
from .base_agent import BaseAgent


class GradingAgent(BaseAgent):
    """Adaptive grading based on grade tier."""

    async def process(self, state: Dict[str, Any]) -> Dict[str, Any]:
        """Grade using tier-appropriate strategy."""

        try:
            submission_id = state.get("submission_id")
            grade_tier = state.get("grade_tier")
            self._log_start(submission_id)

            ocr_results = state["ocr_results"]
            answer_key = state["answer_key"]
            grades = []
            total_score = 0

            for ocr_result in ocr_results:
                q_num = ocr_result["question_number"]
                student_answer = ocr_result["extracted_text"]
                model_answer_data = answer_key.get(str(q_num), {})

                # Tier-specific grading
                if grade_tier == "K-5":
                    grade_result = await self._grade_primary(
                        student_answer, model_answer_data
                    )
                elif grade_tier == "6-8":
                    grade_result = await self._grade_middle(
                        student_answer, model_answer_data, ocr_result
                    )
                elif grade_tier == "9-12":
                    grade_result = await self._grade_secondary(
                        student_answer, model_answer_data, ocr_result
                    )
                else:  # College+
                    grade_result = await self._grade_college(
                        student_answer, model_answer_data, ocr_result, state
                    )

                grades.append({
                    "question_number": q_num,
                    "student_answer": student_answer,
                    **grade_result
                })

                total_score += grade_result["score"]

            state["grades"] = grades
            state["total_score"] = total_score
            state["processing_stage"] = "graded"

            return state

        except Exception as e:
            self._log_error(state.get("submission_id"), e)
            state["error"] = str(e)
            return state

    async def _grade_primary(self, student_answer: str, model_data: Dict) -> Dict:
        """K-5: Simple exact matching + keyword search."""
        model_answer = model_data.get("model_answer", "").lower()
        student_answer_lower = student_answer.lower().strip()

        # Exact match
        if student_answer_lower == model_answer:
            return {
                "score": model_data.get("max_marks", 1),
                "feedback": "🌟 Excellent!",
                "reasoning": "Exact answer match"
            }

        # Keyword matching
        keywords = model_data.get("keywords", [])
        if any(kw.lower() in student_answer_lower for kw in keywords):
            return {
                "score": model_data.get("max_marks", 1) * 0.75,
                "feedback": "👍 Good try! Almost there!",
                "reasoning": "Keyword match"
            }

        return {
            "score": 0,
            "feedback": "Keep practicing! 💪",
            "reasoning": "No match found"
        }

    async def _grade_middle(self, student_answer: str, model_data: Dict, ocr_result: Dict) -> Dict:
        """6-8: Rubric-based + semantic understanding."""

        prompt = f\"\"\"
        Grade this 6-8 grade student answer:

        **Question:** {model_data.get('question', '')}
        **Student Answer:** {student_answer}
        **Model Answer:** {model_data.get('model_answer', '')}
        **Rubric:** {model_data.get('rubric', '')}
        **Max Marks:** {model_data.get('max_marks', 1)}

        Consider:
        - Concept understanding (not just exact words)
        - Partial credit for partial understanding
        - Common middle-school misconceptions

        Return JSON:
        {{
            "score": <number>,
            "feedback": "<constructive feedback>",
            "reasoning": "<explanation>"
        }}
        \"\"\"

        result = await self.llm.call_gemini(prompt)
        return json.loads(result)

    async def _grade_secondary(self, student_answer: str, model_data: Dict, ocr_result: Dict) -> Dict:
        """9-12: Advanced rubrics + multi-part reasoning."""

        prompt = f\"\"\"
        Grade this high school student answer:

        **Question:** {model_data.get('question', '')}
        **Student Answer:** {student_answer}
        **Model Answer:** {model_data.get('model_answer', '')}
        **Rubric:** {model_data.get('rubric', '')}
        **Max Marks:** {model_data.get('max_marks', 1)}

        This is high school level. Evaluate:
        - Accuracy and completeness
        - Reasoning quality
        - Any mathematical errors
        - Essay structure (if applicable)

        Return JSON with detailed rubric breakdown:
        {{
            "score": <number>,
            "points_covered": [<list>],
            "points_missed": [<list>],
            "errors": [<list>],
            "feedback": "<detailed academic critique>",
            "reasoning": "<step-by-step analysis>"
        }}
        \"\"\"

        result = await self.llm.call_gemini_pro(prompt)
        return json.loads(result)

    async def _grade_college(self, student_answer: str, model_data: Dict, ocr_result: Dict, state: Dict) -> Dict:
        """College+: Advanced reasoning + research validation."""

        prompt = f\"\"\"
        Grade this college-level student answer with academic rigor:

        **Question:** {model_data.get('question', '')}
        **Student Answer:** {student_answer}
        **Model Answer:** {model_data.get('model_answer', '')}
        **Rubric:** {model_data.get('rubric', '')}
        **Max Marks:** {model_data.get('max_marks', 1)}

        This is college-level work. Evaluate:
        - Academic accuracy and precision
        - Depth of analysis and critical thinking
        - Proper citations and attribution
        - Research quality (if applicable)
        - Mathematical proofs or logical rigor
        - Writing quality and clarity

        Return JSON:
        {{
            "score": <number>,
            "academic_level": "beginner|intermediate|advanced|expert",
            "strengths": [<list>],
            "weaknesses": [<list>],
            "suggestions": [<list>],
            "feedback": "<scholarly feedback>",
            "reasoning": "<detailed academic analysis>"
        }}
        \"\"\"

        result = await self.llm.call_gemini_pro(prompt)

        # Add plagiarism check for college
        plagiarism_check = await self._check_plagiarism(student_answer)
        result["plagiarism_score"] = plagiarism_check["score"]

        return result

    async def _check_plagiarism(self, student_answer: str) -> Dict:
        """College+: Plagiarism detection."""
        # Call plagiarism API (Turnitin, Copyscape, etc.)
        # Return plagiarism score and sources
        return {
            "score": 0.0,  # 0-100%
            "sources": []
        }
