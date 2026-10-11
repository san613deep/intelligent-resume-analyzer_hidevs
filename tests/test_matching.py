
from src.candidate import Candidate
from src.job_analyzer import Job
from src.matching_engine import (
    BasicScoring,
    WeightedScoring,
    analyze_candidate,
    skills_are_equivalent,
)


def test_skill_matching():
    assert skills_are_equivalent("Pyhton", "Python")
    assert skills_are_equivalent("JS", "JavaScript")
    assert not skills_are_equivalent("Python", "Photoshop")


def test_weighted_score():
    candidate = Candidate(
        name="Rahul Sharma",
        skills=["Python", "SQL", "Git"],
        experience=2,
        education="Bachelor degree",
    )

    job = Job(
        title="Python Developer",
        required_skills=["Python", "SQL", "Git", "Django"],
        min_experience=2,
        education="Bachelor degree",
    )

    result = analyze_candidate(candidate, job)

    assert result.score == 85.0
    assert result.matched_skills == ["Python", "SQL", "Git"]
    assert result.missing_skills == ["Django"]
    assert result.experience_match is True
    assert result.education_match is True
    assert result.recommendation == "STRONGLY RECOMMEND"


def test_scoring_strategies():
    candidate = Candidate(
        name="Rahul",
        skills=["Python"],
        experience=2,
        education="Bachelor degree",
    )

    job = Job(
        title="Developer",
        required_skills=["Python", "SQL"],
        min_experience=2,
        education="Bachelor degree",
    )

    basic = analyze_candidate(candidate, job, BasicScoring())
    weighted = analyze_candidate(candidate, job, WeightedScoring())

    assert basic.score == 83.33
    assert weighted.score == 70.0
