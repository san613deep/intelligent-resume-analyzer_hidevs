import re
from src.candidate import Candidate

def parse_resume(text: str) -> Candidate:
    """Extract candidate information from plain resume text."""
    name = ""
    email = ""
    skills = []
    experience = 0.0
    education = ""

    # extract email
    email_match = re.search(
        r"\b[A-Za-z0-9._%+-+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}]\b",
        text
    )

    if email_match:
        email = email_match.group(0)

    #extract name
    name_match = re.search(
        r"(?im)^\s*Name\s*:\s*(.+?)\s*$",
        text
    )

    if name_match:
        name = name_match.group(1).strip()

    # Extract skills from a labeled line
    skills_match = re.search(
        r"(?im)^\s*Skills\s*:\s*(.+?)\s*$",
        text
    )

    if skills_match:
        skills = [
            skill.strip()
            for skill in skills_match.group(1).split(",")
            if skill.strip()
        ]
    
    # Extract years of experience
    experience_match = re.search(
        r"(?i)(\d+(?:\.\d+)?)\s*\+?\s*years?\s+of\s+experience",
        text
    )

    if not experience_match:
        experience_match = re.search(
            r"(?i)Experience\s*:\s*(\d+(?:\.\d+)?)\s*\+?\s*years?",
            text
        )

    if experience_match:
        experience = float(experience_match.group(1))

    # Extract education from a labeled line
    education_match = re.search(
        r"(?im)^\s*Education\s*:\s*(.+?)\s*$",
        text
    )

    if education_match:
        education = education_match.group(1).strip()

    return Candidate(
        name=name,
        email=email,
        skills=skills,
        experience=experience,
        education=education
    )