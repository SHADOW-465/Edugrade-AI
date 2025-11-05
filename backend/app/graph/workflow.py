"""
LangGraph workflow that adapts nodes based on grade tier.
"""

from langgraph.graph import StateGraph, END
from .state import GradingState


class AdaptiveGradingWorkflow:
    """Adaptive multi-grade grading workflow."""

    def build_workflow(self, grade_tier: str):
        """Build workflow tailored to grade tier."""

        workflow = StateGraph(GradingState)

        # Core nodes (all tiers)
        workflow.add_node("preprocess", self.preprocess_node)
        workflow.add_node("segment", self.segment_node)
        workflow.add_node("ocr", self.ocr_node)
        workflow.add_node("grade", self.grade_node)
        workflow.add_node("factcheck", self.factcheck_node)
        workflow.add_node("feedback", self.feedback_node)

        # Conditional nodes (tier-specific)
        if grade_tier in ["9-12", "College"]:
            workflow.add_node("diagram_analysis", self.diagram_node)

        if grade_tier == "College":
            workflow.add_node("plagiarism_check", self.plagiarism_node)
            workflow.add_node("research_validation", self.research_node)

        # Build edges
        workflow.add_edge("preprocess", "segment")
        workflow.add_edge("segment", "ocr")
        workflow.add_edge("ocr", "grade")

        # Diagram analysis (9-12, College)
        if grade_tier in ["9-12", "College"]:
            workflow.add_edge("grade", "diagram_analysis")
            workflow.add_edge("diagram_analysis", "factcheck")
        else:
            workflow.add_edge("grade", "factcheck")

        workflow.add_edge("factcheck", "feedback")

        # Plagiarism (College only)
        if grade_tier == "College":
            workflow.add_edge("feedback", "plagiarism_check")
            workflow.add_edge("plagiarism_check", "research_validation")
            workflow.add_edge("research_validation", END)
        else:
            workflow.add_edge("feedback", END)

        workflow.set_entry_point("preprocess")

        return workflow.compile()

    def preprocess_node(self, state):
        return state

    def segment_node(self, state):
        return state

    def ocr_node(self, state):
        return state

    def grade_node(self, state):
        return state

    def factcheck_node(self, state):
        return state

    def feedback_node(self, state):
        return state

    def diagram_node(self, state):
        return state

    def plagiarism_node(self, state):
        return state

    def research_node(self, state):
        return state
