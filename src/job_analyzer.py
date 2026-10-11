import re
from dataclasses import dataclass, field

@dataclass
class Job:
    title: str = ""
    required_skills: list[str] = field(default_factory=list)
    min_experience: float = 0.0
    education: str = ""

def analyze_job_description(text: str) -> Job:
    """Extract job requirements from a structured job description."""

    title = ""
    required_skills = []
    min_experience = 0.0
    education = ""

    # Extract job title
    title_match = re.search(
        r"(?im)^\s*Job Title\s*:\s*(.+?)\s*$",
        text
    )
    if title_match:
        title = title_match.group(1).strip()

    # Extract required skills
    skills_match = re.search(
        r"(?im)^\s*Required Skills\s*:\s*(.+?)\s*$",
        text
    )
    if skills_match:
        required_skills = [
            skill.strip()
            for skill in skills_match.group(1).split(",")
            if skill.strip()
        ]

    # Extract minimum experience
    experience_match = re.search(
        r"(?im)^\s*Minimum Experience\s*:\s*(\d+(?:\.\d+)?)\s*years?\s*$",
        text
    )
    if experience_match:
        min_experience = float(experience_match.group(1))

    # Extract education requirement
    education_match = re.search(
        r"(?im)^\s*Education\s*:\s*(.+?)\s*$",
        text
    )
    if education_match:
        education = education_match.group(1).strip()

    return Job(
        title=title,
        required_skills=required_skills,
        min_experience=min_experience,
        education=education
    )
