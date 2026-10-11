
from src.candidate import Candidate
from src.job_analyzer import Job
from src.matching_engine import analyze_candidate
from src.report_generator import generate_analysis_report


def test_generate_analysis_report():
    candidate = Candidate(
        name="Rahul Sharma",
        email="rahul@example.com",
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
    report = generate_analysis_report(candidate, job, result)

    assert "Rahul Sharma" in report
    assert "Python Developer" in report
    assert "Match Score: 85.0/100" in report
    assert "Matched Skills: 3/4" in report
    assert "Django" in report
    assert "STRONGLY RECOMMEND" in report
