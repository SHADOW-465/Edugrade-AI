# EduGrade AI: Adaptive Multi-Grade Automated Grading System
## Comprehensive Development Guide (K-12 + College) with Failsafe Architecture

**Last Updated**: November 5, 2025  
**Status**: Production-Ready for Implementation  
**Target Grades**: Kindergarten to College (18+ years)  
**Target Environment**: Cursor IDE / VS Code

---

## TABLE OF CONTENTS

1. [Project Overview](#project-overview)
2. [Grade-Adaptive Architecture](#grade-adaptive-architecture)
3. [Updated Project Structure](#updated-project-structure)
4. [Core Implementation Requirements](#core-implementation-requirements)
5. [Adaptive Agent Implementation](#adaptive-agent-implementation)
6. [LangGraph Workflow (Adaptive)](#langgraph-workflow-adaptive)
7. [FastAPI Endpoints](#fastapi-endpoints)
8. [Services Layer](#services-layer)
9. [Streamlit Dashboard](#streamlit-dashboard)
10. [Database Schema](#database-schema)
11. [Environment Configuration](#environment-configuration)
12. [Testing Strategy](#testing-strategy)
13. [Deployment](#deployment)
14. [Success Criteria](#success-criteria)

---

## PROJECT OVERVIEW

Build a **production-grade, adaptive automated answer sheet grading system** called "EduGrade AI" that intelligently scales from **Kindergarten through College** students by adjusting:

✅ **OCR Complexity**: Simple text (K-5) → Cursive/Script (6-8) → Cursive+Math+Diagrams (9-12) → Complex notation/equations (College)  
✅ **Grading Logic**: Exact matching (K-5) → Flexible rubrics (6-8) → Semantic understanding (9-12) → Advanced LLM reasoning (College)  
✅ **Answer Validation**: Simple keywords (K-5) → Concept verification (6-8) → Multi-part reasoning (9-12) → Research-level assessment (College)  
✅ **Fact-Checking Depth**: Basic facts (K-5) → Subject-specific accuracy (6-8) → Deep domain knowledge (9-12) → Academic rigor (College)  
✅ **Feedback Quality**: Encouragement (K-5) → Guidance (6-8) → Detailed critique (9-12) → Scholarly suggestions (College)

### **Key Capabilities**

- Upload scanned answer sheets (PDF, JPG, PNG) at any education level
- Auto-detect grade level from content analysis
- Dynamically adjust OCR, grading, and evaluation pipeline
- Multi-stage teacher approval workflow
- Parent-only access post-approval
- Robust failsafe with SQLite queue + Convex sync
- Supports both Streamlit (hackathon) and REST API (production)

---

## GRADE-ADAPTIVE ARCHITECTURE

### **Grade Level Classifications**

```
┌─────────────────────────────────────────────────────────────┐
│ GRADE LEVEL TIERS & REQUIREMENTS                            │
├─────────────────────────────────────────────────────────────┤
│ TIER 1: K-5 (Primary)                                       │
│ - Simple handwriting, printed letters                       │
│ - MCQ, fill-in-blanks, 1-word answers                       │
│ - Exact answer matching, partial credit                     │
│ - Encouragement-focused feedback                            │
│ - TrOCR (small) + basic Gemini grading                      │
│                                                              │
│ TIER 2: 6-8 (Middle School)                                 │
│ - Mixed print & cursive, cleaner handwriting               │
│ - Short paragraphs, diagrams, graphs                        │
│ - Rubric-based scoring, semantic understanding             │
│ - Constructive feedback with improvement tips              │
│ - TrOCR (base) + diagram detection + Gemini                │
│                                                              │
│ TIER 3: 9-12 (High School)                                  │
│ - Complex cursive, mathematical notation, formulas          │
│ - Multi-part answers, essays, problem-solving             │
│ - Advanced rubrics, partial marking, deductions            │
│ - Detailed explanations & academic critique               │
│ - Ensemble OCR + Math notation + Gemini Pro               │
│                                                              │
│ TIER 4: College+                                            │
│ - Advanced notation (LaTeX, matrices), research writing     │
│ - Complex problem-solving, proofs, essays                  │
│ - Strict academic evaluation, plagiarism checks             │
│ - Scholarly feedback, research-level guidance              │
│ - Full OCR ensemble + Advanced LLM + Plagiarism API       │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

### **Adaptive Processing Pipeline**

```
1. INTAKE & DETECTION
   ↓
   Grade Detection Engine
   (Analyzes content complexity, handwriting, notation)
   ↓
   
2. ADAPTIVE PREPROCESSING
   ├─ Tier 1: Basic deskew + denoise
   ├─ Tier 2: Advanced denoise + diagram preservation
   ├─ Tier 3: Math notation detection + formula isolation
   └─ Tier 4: Scientific notation + advanced OCR prep
   ↓
   
3. ADAPTIVE SEGMENTATION
   ├─ Tier 1: Simple grid-based detection
   ├─ Tier 2: Grid + diagram box detection
   ├─ Tier 3: Complex layout + equation zones
   └─ Tier 4: Full-page semantic segmentation
   ↓
   
4. ADAPTIVE OCR
   ├─ Tier 1: TrOCR-small (lightweight)
   ├─ Tier 2: TrOCR-base + diagram analysis
   ├─ Tier 3: TrOCR + PaddleOCR + Math notation parser
   └─ Tier 4: Full ensemble + LaTeX parser + formula recognition
   ↓
   
5. ADAPTIVE GRADING
   ├─ Tier 1: String matching + keyword search (Gemini Flash)
   ├─ Tier 2: Semantic similarity + rubric matching (Gemini Flash)
   ├─ Tier 3: Multi-part evaluation + LLM reasoning (Gemini Pro)
   └─ Tier 4: Advanced reasoning + academic standards (Gemini Pro + Custom prompts)
   ↓
   
6. ADAPTIVE FEEDBACK
   ├─ Tier 1: Encouraging, simple language
   ├─ Tier 2: Constructive with specific suggestions
   ├─ Tier 3: Detailed academic critique
   └─ Tier 4: Scholarly guidance with research pointers
   ↓
   
7. TEACHER REVIEW & APPROVAL
   ↓
   
8. PARENT/STUDENT ACCESS
```

---

## UPDATED PROJECT STRUCTURE

```
edugrade-ai/
├── backend/
│   ├── app/
│   │   ├── __init__.py
│   │   ├── main.py                      # FastAPI + lifespan + scheduler
│   │   ├── config.py                    # Pydantic settings
│   │   │
│   │   ├── core/
│   │   │   ├── __init__.py
│   │   │   ├── security.py              # JWT, password hashing
│   │   │   ├── logging.py               # Structured logging
│   │   │   ├── exceptions.py            # Custom exceptions
│   │   │   ├── constants.py             # Enums & constants
│   │   │   └── grade_levels.py          # Grade tier definitions
│   │   │
│   │   ├── models/
│   │   │   ├── __init__.py
│   │   │   ├── grade_detector.py        # AI-based grade detection
│   │   │   ├── tier_classifier.py       # Classify into K-5, 6-8, 9-12, College
│   │   │   └── schemas.py               # Pydantic models
│   │   │
│   │   ├── agents/
│   │   │   ├── __init__.py
│   │   │   ├── base_agent.py            # Abstract base
│   │   │   ├── preprocessing_agent.py   # Tier-aware preprocessing
│   │   │   ├── segmentation_agent.py    # Tier-aware segmentation
│   │   │   ├── ocr_agent.py             # Tier-aware OCR ensemble
│   │   │   ├── grading_agent.py         # Tier-aware grading logic
│   │   │   ├── feedback_agent.py        # Tier-aware feedback generation
│   │   │   ├── factcheck_agent.py       # Tier-aware fact verification
│   │   │   └── plagiarism_agent.py      # College-level plagiarism check (NEW)
│   │   │
│   │   ├── graph/
│   │   │   ├── __init__.py
│   │   │   ├── state.py                 # Tier-aware GradingState
│   │   │   ├── nodes.py                 # Adaptive node functions
│   │   │   └── workflow.py              # Tier-adaptive LangGraph
│   │   │
│   │   ├── api/
│   │   │   ├── __init__.py
│   │   │   ├── v1/
│   │   │   │   ├── __init__.py
│   │   │   │   ├── endpoints/
│   │   │   │   │   ├── __init__.py
│   │   │   │   │   ├── exams.py         # Exam with tier config
│   │   │   │   │   ├── submissions.py   # Upload + auto-grading
│   │   │   │   │   ├── approvals.py     # Teacher approval
│   │   │   │   │   ├── analytics.py     # Dashboard data
│   │   │   │   │   └── health.py        # Health checks
│   │   │   │   └── dependencies.py      # DI
│   │   │
│   │   ├── services/
│   │   │   ├── __init__.py
│   │   │   ├── tier_service.py          # Tier detection & config (NEW)
│   │   │   ├── convex_service.py        # Convex wrapper
│   │   │   ├── local_queue_service.py   # SQLite queue
│   │   │   ├── failsafe_service.py      # Failsafe orchestration
│   │   │   ├── grading_service.py       # Workflow orchestration
│   │   │   ├── llm_service.py           # Generic LLM wrapper
│   │   │   ├── plagiarism_service.py    # College-level plagiarism (NEW)
│   │   │   └── storage_service.py       # File operations
│   │   │
│   │   └── utils/
│   │       ├── __init__.py
│   │       ├── image_utils.py
│   │       ├── prompt_templates.py      # Tier-specific prompts
│   │       ├── validators.py
│   │       ├── math_parser.py           # LaTeX/formula parsing (NEW)
│   │       └── diagram_detector.py      # Diagram/graph detection (NEW)
│   │
│   ├── convex/
│   │   ├── schema.ts                    # Enhanced schema with grade_tier
│   │   ├── submissions.ts
│   │   ├── exams.ts
│   │   └── .env.local
│   │
│   ├── tests/
│   │   ├── test_tier_detection.py       # (NEW)
│   │   ├── test_adaptive_agents.py      # (NEW)
│   │   ├── test_failsafe.py
│   │   └── test_workflow.py
│   │
│   ├── requirements.txt
│   ├── .env.example
│   └── README.md
│
├── frontend/
│   ├── streamlit_dashboard.py           # Tier-aware multi-page UI
│   ├── requirements.txt
│   ├── pages/
│   │   ├── 1_teacher_upload.py          # Grade-level specific UI
│   │   ├── 2_teacher_review.py          # Tier-aware review interface
│   │   ├── 3_parent_report.py           # Grade-level appropriate report
│   │   ├── 4_student_dashboard.py       # (NEW) College student view
│   │   ├── 5_analytics.py
│   │   └── 6_admin_settings.py
│   └── components/
│       ├── grade_selector.py            # (NEW) Grade tier selector
│       ├── tier_adaptive_card.py        # (NEW) Dynamic UI per tier
│       └── feedback_display.py          # Tier-appropriate feedback
│
├── data/
│   ├── uploads/
│   ├── processed/
│   ├── models/
│   │   ├── yolov8n.pt                  # YOLOv8 Nano (K-8)
│   │   ├── yolov8m.pt                  # YOLOv8 Medium (9-12)
│   │   ├── math_notation_model/         # (NEW) Math formula detection
│   │   └── .gitignore
│   └── sample_data/
│
├── docker-compose.yml
├── Dockerfile
└── README.md
```

---

## CORE IMPLEMENTATION REQUIREMENTS

### **A. Grade Detection Service (`backend/app/services/tier_service.py`)**

```python
"""
Automatically detect student grade level from answer sheet content.
Used to configure entire grading pipeline.
"""

from enum import Enum
from typing import Dict, Tuple
from PIL import Image
import numpy as np

class GradeTier(Enum):
    """Grade level classification."""
    PRIMARY = "K-5"           # Kindergarten to 5th
    MIDDLE = "6-8"            # Middle school
    SECONDARY = "9-12"        # High school
    COLLEGE = "College+"      # College and above

class TierService:
    """Detect and configure grade tier."""
    
    @staticmethod
    async def detect_tier_from_image(image: np.ndarray) -> Tuple[GradeTier, float]:
        """
        Analyze image to detect grade tier.
        
        Heuristics:
        - Image complexity (detailed drawings/diagrams = higher tier)
        - Text complexity (mathematical notation = higher tier)
        - Handwriting maturity (cursive quality = higher tier)
        - Layout sophistication (multi-column = higher tier)
        
        Returns: (GradeTier, confidence: 0-1)
        """
        
        # Extract features
        text_complexity = await TierService._analyze_text_complexity(image)
        handwriting_quality = await TierService._analyze_handwriting_quality(image)
        diagram_presence = await TierService._detect_diagrams(image)
        notation_complexity = await TierService._detect_notation(image)
        
        # Decision logic
        if notation_complexity > 0.7:  # Mathematical notation detected
            return (GradeTier.COLLEGE, 0.9)
        elif notation_complexity > 0.4:  # Some formulas
            return (GradeTier.SECONDARY, 0.85)
        elif handwriting_quality > 0.8 and diagram_presence > 0.5:
            return (GradeTier.MIDDLE, 0.8)
        elif diagram_presence > 0.3:
            return (GradeTier.MIDDLE, 0.75)
        else:
            return (GradeTier.PRIMARY, 0.85)
    
    @staticmethod
    async def _analyze_text_complexity(image: np.ndarray) -> float:
        """Analyze text for complexity indicators."""
        # Check for cursive, multiple languages, technical terms
        return np.random.random()  # Placeholder
    
    @staticmethod
    async def _analyze_handwriting_quality(image: np.ndarray) -> float:
        """Assess handwriting maturity."""
        # Cursive detection, consistency, size uniformity
        return np.random.random()  # Placeholder
    
    @staticmethod
    async def _detect_diagrams(image: np.ndarray) -> float:
        """Detect presence and complexity of diagrams."""
        # Circle detection, line drawing, chart detection
        return np.random.random()  # Placeholder
    
    @staticmethod
    async def _detect_notation(image: np.ndarray) -> float:
        """Detect mathematical/scientific notation."""
        # LaTeX, Greek symbols, fractions, exponents
        return np.random.random()  # Placeholder
    
    @staticmethod
    def get_tier_config(tier: GradeTier) -> Dict:
        """Return processing configuration for tier."""
        
        configs = {
            GradeTier.PRIMARY: {
                "ocr_model": "trocr-small",
                "yolo_model": "yolov8n.pt",
                "llm_model": "gemini-2.0-flash",
                "llm_temperature": 0.3,
                "grading_strategy": "exact_match",
                "max_attempts_per_question": 1,
                "supports_diagrams": False,
                "supports_equations": False,
                "feedback_style": "encouraging"
            },
            GradeTier.MIDDLE: {
                "ocr_model": "trocr-base",
                "yolo_model": "yolov8m.pt",
                "llm_model": "gemini-2.0-flash",
                "llm_temperature": 0.5,
                "grading_strategy": "semantic",
                "max_attempts_per_question": 2,
                "supports_diagrams": True,
                "supports_equations": False,
                "feedback_style": "constructive"
            },
            GradeTier.SECONDARY: {
                "ocr_model": "trocr-large",
                "yolo_model": "yolov8m.pt",
                "llm_model": "gemini-pro",
                "llm_temperature": 0.6,
                "grading_strategy": "advanced_rubric",
                "max_attempts_per_question": 3,
                "supports_diagrams": True,
                "supports_equations": True,
                "feedback_style": "academic_critique"
            },
            GradeTier.COLLEGE: {
                "ocr_model": "ensemble",  # TrOCR + PaddleOCR + custom
                "yolo_model": "yolov8l.pt",
                "llm_model": "gemini-pro",
                "llm_temperature": 0.7,
                "grading_strategy": "advanced_reasoning",
                "max_attempts_per_question": 5,
                "supports_diagrams": True,
                "supports_equations": True,
                "supports_code": True,
                "supports_research": True,
                "plagiarism_check": True,
                "feedback_style": "scholarly"
            }
        }
        
        return configs.get(tier, configs[GradeTier.PRIMARY])
```

### **B. Enhanced Database Schema (`backend/convex/schema.ts`)**

```typescript
import { defineSchema, defineTable, s } from "convex/server";

export default defineSchema({
  exams: defineTable({
    title: s.string(),
    subject: s.string(),
    grade_level: s.string(),  // "K-5", "6-8", "9-12", "College"
    grade_tier: s.string(),    // Auto-detected or manually set
    teacher_id: s.string(),
    answer_key: s.any(),
    rubric: s.any(),
    status: s.string(),
    supports_diagrams: s.boolean(),
    supports_equations: s.boolean(),
    created_at: s.number(),
    updated_at: s.number(),
  })
    .index("by_teacher_id", ["teacher_id"])
    .index("by_grade_tier", ["grade_tier"]),

  submissions: defineTable({
    exam_id: s.id("exams"),
    student_id: s.string(),
    student_name: s.string(),
    student_grade_level: s.string(),  // Actual grade of student
    detected_grade_tier: s.string(),   // Auto-detected from content
    grade_tier_confidence: s.number(), // 0-1 confidence score
    teacher_id: s.string(),
    file_paths: s.array(s.string()),
    status: s.string(),
    processing_stage: s.string(),
    progress_percentage: s.optional(s.number()),
    created_at: s.number(),
    processed_at: s.optional(s.number()),
    
    // Tier-specific results
    results: s.optional(s.any()),
    grades: s.optional(s.array(s.any())),
    total_score: s.optional(s.number()),
    max_score: s.optional(s.number()),
    percentage: s.optional(s.number()),
    
    // College-specific fields
    plagiarism_score: s.optional(s.number()),
    plagiarism_report: s.optional(s.string()),
    
    // Approval
    approved: s.boolean(),
    approved_by: s.optional(s.string()),
    approved_at: s.optional(s.number()),
    approval_notes: s.optional(s.string()),
  })
    .index("by_exam_id", ["exam_id"])
    .index("by_grade_tier", ["detected_grade_tier"])
    .index("by_status", ["status"]),

  grades: defineTable({
    submission_id: s.id("submissions"),
    exam_id: s.id("exams"),
    grade_tier: s.string(),
    question_number: s.number(),
    student_answer: s.string(),
    extracted_text: s.string(),
    
    score: s.number(),
    max_score: s.number(),
    feedback: s.string(),
    reasoning: s.string(),
    
    // Tier-specific evaluations
    diagram_analysis: s.optional(s.any()),  // For 6+
    equation_breakdown: s.optional(s.any()), // For 9+
    code_review: s.optional(s.any()),       // For College+
    research_assessment: s.optional(s.any()), // For College+
    
    // Plagiarism detection (College+)
    plagiarism_percentage: s.optional(s.number()),
    plagiarism_sources: s.optional(s.array(s.string())),
    
    fact_check_result: s.optional(s.any()),
    
    hash_signature: s.string(),
    teacher_override: s.boolean(),
    override_reason: s.optional(s.string()),
    
    created_at: s.number(),
    updated_at: s.number(),
  })
    .index("by_submission_id", ["submission_id"])
    .index("by_grade_tier", ["grade_tier"]),

  users: defineTable({
    email: s.string(),
    hashed_password: s.string(),
    role: s.string(),  // "teacher", "parent", "student", "admin"
    grade_tier: s.optional(s.string()),  // For students, their grade
    school_id: s.optional(s.string()),
    created_at: s.number(),
  })
    .index("by_email", ["email"]),
});
```

---

## ADAPTIVE AGENT IMPLEMENTATION

### **A. Tier-Aware Preprocessing Agent**

```python
"""
Adaptive preprocessing based on grade tier.
K-5: Basic cleaning
College: Advanced math notation preservation
"""

class PreprocessingAgent(BaseAgent):
    """Tier-aware preprocessing."""
    
    async def process(self, state: Dict[str, Any]) -> Dict[str, Any]:
        """Execute tier-appropriate preprocessing."""
        
        try:
            submission_id = state.get("submission_id")
            grade_tier = state.get("grade_tier")
            self._log_start(submission_id)
            
            image_path = state["file_paths"][0]
            image = cv2.imread(image_path)
            
            if grade_tier == "K-5":
                image = await self._preprocess_primary(image)
            elif grade_tier == "6-8":
                image = await self._preprocess_middle(image)
            elif grade_tier == "9-12":
                image = await self._preprocess_secondary(image)
            else:  # College+
                image = await self._preprocess_college(image)
            
            processed_path = self._save_processed(image, submission_id)
            state["preprocessed_image_path"] = processed_path
            state["processing_stage"] = "preprocessed"
            
            return state
            
        except Exception as e:
            self._log_error(state.get("submission_id"), e)
            state["error"] = str(e)
            return state
    
    async def _preprocess_primary(self, image: np.ndarray) -> np.ndarray:
        """K-5: Basic cleaning."""
        image = self._deskew(image, max_angle=15)
        image = self._denoise(image, h=10)
        image = self._binarize(image)
        return image
    
    async def _preprocess_middle(self, image: np.ndarray) -> np.ndarray:
        """6-8: Enhanced cleaning + diagram preservation."""
        image = self._deskew(image, max_angle=20)
        image = self._denoise(image, h=8)  # Less aggressive
        image = self._binarize(image)
        return image
    
    async def _preprocess_secondary(self, image: np.ndarray) -> np.ndarray:
        """9-12: Advanced cleaning + equation preservation."""
        image = self._deskew(image, max_angle=25)
        image = self._denoise(image, h=6)  # Minimal noise
        # Preserve formulas and complex structures
        image = self._adaptive_thresholding(image)
        return image
    
    async def _preprocess_college(self, image: np.ndarray) -> np.ndarray:
        """College+: Full preservation + math notation handling."""
        image = self._deskew(image, max_angle=30)
        image = self._advanced_denoise(image)
        # Detect and preserve math regions
        image = self._preserve_mathematical_regions(image)
        return image
    
    def _preserve_mathematical_regions(self, image: np.ndarray) -> np.ndarray:
        """Preserve mathematical notation and complex symbols."""
        # Mark regions with mathematical symbols for special handling
        # Apply minimal processing to these regions
        return image
```

### **B. Tier-Aware Grading Agent**

```python
"""
Tier-specific grading logic using tier-appropriate LLM models and strategies.
"""

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
        
        prompt = f"""
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
        """
        
        result = await self.llm.call_gemini(prompt)
        return json.loads(result)
    
    async def _grade_secondary(self, student_answer: str, model_data: Dict, ocr_result: Dict) -> Dict:
        """9-12: Advanced rubrics + multi-part reasoning."""
        
        prompt = f"""
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
        """
        
        result = await self.llm.call_gemini_pro(prompt)
        return json.loads(result)
    
    async def _grade_college(self, student_answer: str, model_data: Dict, ocr_result: Dict, state: Dict) -> Dict:
        """College+: Advanced reasoning + research validation."""
        
        prompt = f"""
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
        """
        
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
```

### **C. Tier-Aware OCR Agent**

```python
"""
Adaptive OCR using tier-appropriate models and ensemble strategies.
"""

class OCRAgent(BaseAgent):
    """Tier-aware OCR extraction."""
    
    async def process(self, state: Dict[str, Any]) -> Dict[str, Any]:
        """Extract text using tier-appropriate OCR."""
        
        try:
            submission_id = state.get("submission_id")
            grade_tier = state.get("grade_tier")
            self._log_start(submission_id)
            
            regions = state["segmented_regions"]
            ocr_results = []
            
            for region in regions:
                if grade_tier == "K-5":
                    text, conf = await self._ocr_primary(region["image"])
                elif grade_tier == "6-8":
                    text, conf = await self._ocr_middle(region["image"])
                elif grade_tier == "9-12":
                    text, conf = await self._ocr_secondary(region["image"])
                else:  # College+
                    text, conf = await self._ocr_college(region["image"])
                
                ocr_results.append({
                    "question_number": region["question_number"],
                    "extracted_text": text,
                    "confidence": conf,
                    "coordinates": region["coordinates"]
                })
            
            state["ocr_results"] = ocr_results
            state["processing_stage"] = "ocr_completed"
            
            return state
            
        except Exception as e:
            self._log_error(state.get("submission_id"), e)
            state["error"] = str(e)
            return state
    
    async def _ocr_primary(self, image: np.ndarray) -> Tuple[str, float]:
        """K-5: TrOCR-small (lightweight)."""
        from transformers import TrOCRProcessor, VisionEncoderDecoderModel
        
        processor = TrOCRProcessor.from_pretrained("microsoft/trocr-small-handwritten")
        model = VisionEncoderDecoderModel.from_pretrained("microsoft/trocr-small-handwritten")
        
        pil_image = Image.fromarray(image.astype('uint8'))
        pixel_values = processor(pil_image, return_tensors="pt").pixel_values
        
        with torch.no_grad():
            generated_ids = model.generate(pixel_values, max_length=128)
        
        text = processor.batch_decode(generated_ids, skip_special_tokens=True)[0]
        confidence = min(1.0, len(text) / 40)
        
        return text, confidence
    
    async def _ocr_middle(self, image: np.ndarray) -> Tuple[str, float]:
        """6-8: TrOCR-base + diagram detection."""
        # Use TrOCR base model
        # Also detect diagrams and handle separately
        text, conf = await self._ocr_with_model(image, "microsoft/trocr-base-handwritten")
        
        # Check for diagram elements
        diagram_detected = await self._detect_diagram_region(image)
        if diagram_detected:
            text += "[DIAGRAM DETECTED]"
        
        return text, conf
    
    async def _ocr_secondary(self, image: np.ndarray) -> Tuple[str, float]:
        """9-12: Ensemble OCR + Math notation parsing."""
        # TrOCR + PaddleOCR ensemble
        text1, conf1 = await self._ocr_with_model(image, "microsoft/trocr-large-handwritten")
        text2, conf2 = await self._ocr_paddleocr(image)
        
        # Ensemble result
        text = self._ensemble_ocr_results([text1, text2])
        
        # Parse mathematical notation
        math_text = await self._parse_math_notation(text)
        
        return math_text, max(conf1, conf2)
    
    async def _ocr_college(self, image: np.ndarray) -> Tuple[str, float]:
        """College+: Full ensemble + LaTeX parsing + code detection."""
        
        # Multiple OCR passes
        ocr_results = []
        ocr_results.append(await self._ocr_with_model(image, "microsoft/trocr-large-handwritten"))
        ocr_results.append(await self._ocr_paddleocr(image))
        
        # Weighted ensemble
        text = await self._weighted_ocr_ensemble(ocr_results)
        
        # Parse LaTeX/math
        text = await self._parse_latex(text)
        
        # Detect code blocks
        if self._is_code_block(image):
            text += "\n[CODE BLOCK DETECTED]\n"
        
        confidence = max([r[1] for r in ocr_results])
        
        return text, confidence
```

### **D. College-Specific Plagiarism Agent**

```python
"""
College-level plagiarism detection (NEW).
"""

class PlagiarismAgent(BaseAgent):
    """Detect plagiarism in college submissions."""
    
    async def process(self, state: Dict[str, Any]) -> Dict[str, Any]:
        """Check for plagiarism (College+ only)."""
        
        try:
            grade_tier = state.get("grade_tier")
            
            if grade_tier != "College":
                return state  # Skip for non-college
            
            submission_id = state.get("submission_id")
            self._log_start(submission_id)
            
            grades = state.get("grades", [])
            
            for grade in grades:
                plagiarism_result = await self._check_plagiarism(grade["student_answer"])
                grade["plagiarism_score"] = plagiarism_result["score"]
                grade["plagiarism_sources"] = plagiarism_result["sources"]
            
            state["processing_stage"] = "plagiarism_checked"
            
            return state
            
        except Exception as e:
            self._log_error(state.get("submission_id"), e)
            # Don't fail - plagiarism is optional
            return state
    
    async def _check_plagiarism(self, text: str) -> Dict:
        """Check text against plagiarism detection service."""
        
        # Call Turnitin, Copyscape, or similar API
        # This is a placeholder
        
        plagiarism_score = 0.0  # 0-100%
        sources = []
        
        return {
            "score": plagiarism_score,
            "sources": sources
        }
```

---

## LANGGRAPH WORKFLOW (ADAPTIVE)

### **Tier-Aware State Definition**

```python
"""
Adaptive state that changes based on grade tier.
"""

class GradingState(TypedDict):
    # Metadata
    submission_id: str
    exam_id: str
    student_name: str
    student_id: str
    student_grade_level: str
    grade_tier: str  # K-5, 6-8, 9-12, College
    grade_tier_confidence: float
    file_paths: List[str]
    answer_key: Dict[str, Any]
    
    # Processing
    status: str
    processing_stage: str
    
    # Agent outputs
    preprocessed_image_path: Optional[str]
    segmented_regions: Optional[List[Dict]]
    answer_boxes: Optional[List[Dict]]
    ocr_results: Optional[List[Dict]]
    grades: Optional[List[Dict]]
    feedback: Optional[str]
    
    # College-specific
    plagiarism_checked: Optional[bool]
    plagiarism_score: Optional[float]
    
    # Errors
    error: Optional[str]
    created_at: float
    teacher_id: str
```

### **Adaptive Workflow Construction**

```python
"""
LangGraph workflow that adapts nodes based on grade tier.
"""

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
```

---

## ENHANCED FEATURES FOR EACH TIER

### **K-5 Features**
- ✅ Simple answer matching
- ✅ Encouragement-focused feedback
- ✅ Visual progress indicators (stars, badges)
- ✅ Large, easy-to-read results
- ✅ Parent-friendly language

### **6-8 Features**
- ✅ Diagram recognition and analysis
- ✅ Graph interpretation
- ✅ Constructive feedback with tips
- ✅ Subject-specific vocabulary checking
- ✅ Peer comparison analytics (anonymized)

### **9-12 Features**
- ✅ Mathematical equation parsing
- ✅ Advanced multi-part answer grading
- ✅ Essay evaluation with structure analysis
- ✅ Detailed academic feedback
- ✅ Deduction logic (for errors)
- ✅ Lab report evaluation

### **College Features**
- ✅ Advanced mathematical/scientific notation
- ✅ Code snippet recognition and analysis
- ✅ Research paper evaluation
- ✅ Plagiarism detection
- ✅ Citation verification
- ✅ Academic integrity checks
- ✅ Scholarly feedback with research pointers
- ✅ Graduate-level assessment criteria

---

## UPDATED REQUIREMENTS

### **backend/requirements.txt** (additions for multi-grade):

```txt
# Core (existing)
fastapi
uvicorn[standard]
pydantic
pydantic-settings

# Multi-agent
langgraph
langchain

# Advanced OCR (College)
paddleocr  # For equation/complex text
sympy  # Math formula parsing
latex2mathml  # LaTeX conversion

# Advanced LLM
google-generativeai
openai

# Computer Vision
opencv-python
ultralytics
transformers
torch
torchvision
Pillow
pdf2image

# Plagiarism API (College)
requests

# Database & Failsafe
convex-client-python
apscheduler
tenacity
sqlite3

# Utilities
python-dotenv
numpy
pandas
```

---

## SUCCESS CRITERIA

✅ Backend supports K-5, 6-8, 9-12, and College tiers  
✅ Automatic grade tier detection with confidence scoring  
✅ Adaptive agents adjust behavior per tier  
✅ LangGraph workflow scales dynamically  
✅ College plagiarism detection integrated  
✅ Tier-appropriate feedback generation  
✅ Failsafe mechanism handles all tiers  
✅ Streamlit UI adapts to student grade level  
✅ Teacher can manually override detected tier  
✅ All 6 core agents + plagiarism agent working  
✅ API documentation auto-generated  
✅ Error handling and logging comprehensive  

---

**This production-ready guide supports K-12 and College students with fully adaptive grading, feedback, and assessment mechanisms.**