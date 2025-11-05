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
