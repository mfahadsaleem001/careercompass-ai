import json
import re
from flask import current_app
from app.prompts.career_advisor_prompt import (
    CAREER_ADVISOR_SYSTEM_INSTRUCTION,
    build_career_advisor_prompt,
)


class GeminiServiceError(Exception):
    pass


def _extract_json(text):
    """Gemini sometimes wraps JSON in ```json fences despite instructions. Strip them safely."""
    cleaned = text.strip()
    cleaned = re.sub(r'^```(?:json)?', '', cleaned).strip()
    cleaned = re.sub(r'```$', '', cleaned).strip()
    return json.loads(cleaned)


def _mock_career_advisor_response(data):
    """Used when GEMINI_API_KEY is not configured, so the flow can be built/tested end-to-end."""
    education = data.get('education_level', 'your current level')
    interests = data.get('interests', 'your interests')

    return {
        "career_suggestions": [
            "Software Engineer",
            "Data Analyst",
            "UI/UX Designer"
        ],
        "recommended_degree_programs": [
            "BS Computer Science",
            "BS Software Engineering"
        ],
        "recommended_universities": [
            "FAST NUCES",
            "NUST",
            "COMSATS University"
        ],
        "skills_to_learn": [
            "Python Programming",
            "Data Structures & Algorithms",
            "Git & Version Control"
        ],
        "certifications": [
            "Google Data Analytics Certificate",
            "AWS Cloud Practitioner"
        ],
        "job_opportunities": [
            "Junior Software Developer",
            "Data Analyst Intern",
            "Frontend Developer"
        ],
        "salary_estimates": "Entry-level: PKR 60,000–100,000/month. Mid-level (3-5 yrs): PKR 150,000–300,000/month.",
        "future_scope": "Strong long-term demand as digital transformation continues across industries over the next decade.",
        "ai_explanation": (
            f"This is DEMO data (no Gemini API key configured yet) — shown so you can test the full flow. "
            f"Based on your {education} background and interest in {interests}, real AI suggestions will "
            f"appear here once GEMINI_API_KEY is added to your .env file."
        ),
        "roadmap": [
            f"{education}",
            "Choose Relevant Degree Program",
            "Build Core Technical Skills",
            "Internship / Practical Project",
            "Land First Job Role"
        ],
        "_is_mock": True
    }


def generate_career_advice(data):
    """
    data: dict with the student's profile fields.
    Returns a dict matching the JSON schema defined in the prompt template.
    Raises GeminiServiceError on API/parsing failure (caller should handle gracefully).
    """
    api_key = current_app.config.get('GEMINI_API_KEY')

    if not api_key:
        return _mock_career_advisor_response(data)

    try:
        import google.generativeai as genai

        genai.configure(api_key=api_key)
        model = genai.GenerativeModel(
            model_name='gemini-3.5-flash-lite',
            system_instruction=CAREER_ADVISOR_SYSTEM_INSTRUCTION
        )

        prompt = build_career_advisor_prompt(data)
        response = model.generate_content(prompt)

        return _extract_json(response.text)

    except json.JSONDecodeError as e:
        raise GeminiServiceError(f"AI returned invalid JSON: {e}")
    except Exception as e:
        raise GeminiServiceError(f"Gemini API request failed: {e}")