CAREER_ADVISOR_SYSTEM_INSTRUCTION = """You are an expert career counselor and education advisor with deep knowledge of \
global academic pathways, job markets, and industry trends. You give practical, honest, and specific advice \
tailored to the student's real situation (their education level, marks, budget, and country)."""


def build_career_advisor_prompt(data):
    """
    data: dict with keys -> education_level, marks_cgpa, interests, skills,
          career_goal, budget, country, preferred_industry
    """
    return f"""
Based on the following student profile, generate a detailed career guidance report.

STUDENT PROFILE:
- Education Level: {data.get('education_level')}
- Marks / CGPA: {data.get('marks_cgpa') or 'Not provided'}
- Interests: {data.get('interests')}
- Skills: {data.get('skills') or 'Not provided'}
- Career Goal: {data.get('career_goal') or 'Not specified'}
- Budget: {data.get('budget') or 'Not specified'}
- Country: {data.get('country') or 'Not specified'}
- Preferred Industry: {data.get('preferred_industry') or 'Open to suggestions'}

Respond with ONLY a valid JSON object (no markdown fences, no extra text) in exactly this structure:

{{
  "career_suggestions": ["string", "string", "string"],
  "recommended_degree_programs": ["string", "string"],
  "recommended_universities": ["string", "string", "string"],
  "skills_to_learn": ["string", "string", "string"],
  "certifications": ["string", "string"],
  "job_opportunities": ["string", "string", "string"],
  "salary_estimates": "string describing entry-level to senior salary range in the student's country/currency",
  "future_scope": "string describing 5-10 year outlook for this field",
  "ai_explanation": "string, 2-4 sentences explaining WHY these suggestions fit this specific student's profile",
  "roadmap": ["Step 1 label", "Step 2 label", "Step 3 label", "Step 4 label", "Step 5 label"]
}}

Keep each array to 3-5 concise items. Do not include any text outside the JSON object.
"""