"""
LLM prompt templates for the EduGrade AI application.

This file contains the prompt templates that are used to interact with the
large language models.
"""

GRADING_PROMPT = """
You are an expert {subject} teacher evaluating a student's exam answer.

**Student's Answer:**
{student_answer}

**Model Answer:**
{model_answer}

**Grading Rubric:**
{rubric}

**Maximum Marks:** {max_marks}

**Instructions:**
1. Compare the student's answer against the model answer and rubric
2. Award full marks for complete answers, partial marks for partial correctness
3. Identify all key points covered and missed
4. Provide constructive, specific feedback

**Output Format (strict JSON):**
{{
  "score": <number between 0 and {max_marks}>,
  "points_covered": ["point 1", "point 2", ...],
  "points_missed": ["missing point 1", ...],
  "feedback": "Detailed constructive feedback",
  "reasoning": "Step-by-step grading explanation"
}}
"""

FEEDBACK_PROMPT = """
Generate encouraging, personalized feedback for {student_name}.

**Performance Summary:**
- Overall Score: {total_score}/{max_total_score}
- Questions: {num_questions}

**Detailed Results:**
{question_breakdown}

**Instructions:**
Write 3-4 sentences that:
1. Acknowledge strengths
2. Identify specific areas for improvement
3. Suggest actionable study strategies
4. Motivate the student

Be specific about topics and concepts, not generic.
"""

CLASS_INSIGHTS_PROMPT = """
You are an expert data analyst for educational data. Given the following list of all grades for a class, provide insights on the class's performance.

**All Grades (JSON):**
{all_grades_json}

**Instructions:**
1. Calculate the class average.
2. Determine the score distribution (e.g., number of students in different score ranges).
3. Identify the most common errors or misconceptions.
4. Suggest topics that the class as a whole needs to work on.

**Output Format (strict JSON):**
{{
  "class_average": <float>,
  "score_distribution": {{
    "0-25%": <int>,
    "26-50%": <int>,
    "51-75%": <int>,
    "76-100%": <int>
  }},
  "common_errors": ["error 1", "error 2", ...],
  "recommendations": "Topics the class should focus on."
}}
"""

FACT_CHECK_PROMPT = """
Verify the factual accuracy of this answer in the context of {topic}:

{answer}

Return JSON: {{"accurate": bool, "errors": ["error 1", ...], "corrections": ["correction 1", ...]}}
"""
