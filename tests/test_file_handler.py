
import json

from src.candidate import Candidate
from src.job_analyzer import Job
from src.matching_engine import analyze_candidate
from src.file_handler import (
    save_analysis_result,
    load_analysis_results,
)


def test_save_and_load_analysis(tmp_path):
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
    filename = tmp_path / "analysis_results.json"

    save_analysis_result(candidate, job, result, str(filename))
    save_analysis_result(candidate, job, result, str(filename))

    saved = load_analysis_results(str(filename))

    assert len(saved) == 2
    assert saved[0]["candidate"]["name"] == "Rahul Sharma"
    assert saved[0]["job"]["title"] == "Python Developer"
    assert saved[0]["result"]["score"] == 85.0


def test_missing_json_file_returns_empty_list(tmp_path):
    filename = tmp_path / "missing.json"

    assert load_analysis_results(str(filename)) == []
