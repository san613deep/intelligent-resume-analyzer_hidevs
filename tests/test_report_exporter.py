
from io import BytesIO

from openpyxl import load_workbook
from pypdf import PdfReader

from src.candidate import Candidate
from src.job_analyzer import Job
from src.matching_engine import analyze_candidate
from src.report_generator import ReportExporter


def sample_data():
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

    return [{
        "candidate": candidate,
        "job": job,
        "result": result,
    }]


def test_export_excel():
    content = ReportExporter.export_excel(sample_data())

    workbook = load_workbook(BytesIO(content))
    sheet = workbook["Candidate Analysis"]

    assert sheet["A2"].value == "Rahul Sharma"
    assert sheet["D2"].value == 85.0


def test_export_pdf():
    content = ReportExporter.export_pdf(sample_data())

    reader = PdfReader(BytesIO(content))

    assert len(reader.pages) >= 1
    assert "Intelligent Resume Analyzer" in reader.pages[0].extract_text()


def test_export_html():
    content = ReportExporter.export_html(sample_data())

    assert "<html" in content
    assert "Rahul Sharma" in content
    assert "Python Developer" in content
    assert "85.0" in content
