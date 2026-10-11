
from src.candidate import Candidate
from src.job_analyzer import Job
from src.matching_engine import MatchResult


def generate_analysis_report(
    candidate: Candidate,
    job: Job,
    result: MatchResult
) -> str:
    """Generate a readable candidate analysis report."""

    matched_skills = (
        ", ".join(result.matched_skills) or "None"
    )
    missing_skills = (
        ", ".join(result.missing_skills) or "None"
    )

    experience_status = (
        "Meets requirement"
        if result.experience_match
        else "Does not meet requirement"
    )

    education_status = (
        "Meets requirement"
        if result.education_match
        else "Does not meet requirement"
    )

    report = f"""
==================================================
           CANDIDATE ANALYSIS REPORT
==================================================

CANDIDATE DETAILS
-----------------
Name: {candidate.name or "Not provided"}
Email: {candidate.email or "Not provided"}
Experience: {candidate.experience} years
Education: {candidate.education or "Not provided"}

JOB DETAILS
-----------
Job Title: {job.title or "Not provided"}
Minimum Experience Required: {job.min_experience} years
Required Skills: {", ".join(job.required_skills) or "None"}
Required Education: {job.education or "Not specified"}

MATCH ANALYSIS
--------------
Match Score: {result.score}/100
Matched Skills: {len(result.matched_skills)}/{len(job.required_skills)}
Matched Skill Names: {matched_skills}
Missing Skills: {missing_skills}
Experience Assessment: {experience_status}
Education Assessment: {education_status}

RECOMMENDATION
--------------
{result.recommendation}

IMPORTANT
---------
This report supports human review. The score is based on
the configured matching rules and is not a guarantee of
candidate suitability.

==================================================
"""

    return report.strip()



from html import escape
from io import BytesIO

import pandas as pd
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle,
)


class ReportExporter:
    """Export candidate analysis results to PDF, Excel, and HTML."""

    @staticmethod
    def _get_value(item, key, default=""):
        """Read a value from either a dictionary or an object."""
        if isinstance(item, dict):
            return item.get(key, default)
        return getattr(item, key, default)

    @classmethod
    def _prepare_rows(cls, data):
        """Convert analysis records into rows for exporting."""
        rows = []

        for item in data:
            candidate = cls._get_value(item, "candidate", {})
            job = cls._get_value(item, "job", {})
            result = cls._get_value(item, "result", {})

            rows.append({
                "Candidate": cls._get_value(candidate, "name", "")
                    or "Not provided",
                "Email": cls._get_value(candidate, "email", "")
                    or "Not provided",
                "Job Title": cls._get_value(job, "title", "")
                    or "Not provided",
                "Match Score": cls._get_value(result, "score", 0),
                "Matched Skills": ", ".join(
                    cls._get_value(result, "matched_skills", []) or []
                ),
                "Missing Skills": ", ".join(
                    cls._get_value(result, "missing_skills", []) or []
                ),
                "Experience (years)": cls._get_value(
                    candidate, "experience", 0
                ),
                "Education": cls._get_value(candidate, "education", "")
                    or "Not provided",
                "Recommendation": cls._get_value(
                    result, "recommendation", ""
                ),
            })

        return rows

    @classmethod
    def export_excel(cls, data) -> bytes:
        """Create an Excel workbook and return its bytes."""
        rows = cls._prepare_rows(data)
        output = BytesIO()

        with pd.ExcelWriter(output, engine="openpyxl") as writer:
            pd.DataFrame(rows).to_excel(
                writer,
                index=False,
                sheet_name="Candidate Analysis",
            )

        return output.getvalue()

    @classmethod
    def export_pdf(cls, data) -> bytes:
        """Create a PDF report containing candidate assessments."""
        rows = cls._prepare_rows(data)
        output = BytesIO()

        document = SimpleDocTemplate(
            output,
            pagesize=A4,
            rightMargin=36,
            leftMargin=36,
            topMargin=36,
            bottomMargin=36,
        )

        styles = getSampleStyleSheet()
        story = [
            Paragraph("Intelligent Resume Analyzer", styles["Title"]),
            Spacer(1, 12),
            Paragraph(
                f"Candidate analysis report: {len(rows)} candidate(s)",
                styles["Normal"],
            ),
            Spacer(1, 16),
        ]

        table_data = [[
            "Candidate", "Job", "Score", "Matched Skills",
            "Missing Skills", "Recommendation"
        ]]

        for row in rows:
            table_data.append([
                row["Candidate"],
                row["Job Title"],
                f'{row["Match Score"]}/100',
                row["Matched Skills"] or "None",
                row["Missing Skills"] or "None",
                row["Recommendation"],
            ])

        table = Table(
            table_data,
            repeatRows=1,
            colWidths=[85, 65, 45, 100, 90, 85],
        )

        table.setStyle(TableStyle([
            ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#433878")),
            ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
            ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
            ("FONTSIZE", (0, 0), (-1, -1), 7),
            ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
            ("VALIGN", (0, 0), (-1, -1), "TOP"),
            ("LEFTPADDING", (0, 0), (-1, -1), 5),
            ("RIGHTPADDING", (0, 0), (-1, -1), 5),
            ("TOPPADDING", (0, 0), (-1, -1), 6),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
        ]))

        story.append(table)
        document.build(story)

        return output.getvalue()

    @classmethod
    def export_html(cls, data) -> str:
        """Create a standalone HTML report."""
        rows = cls._prepare_rows(data)

        columns = [
            "Candidate",
            "Email",
            "Job Title",
            "Match Score",
            "Matched Skills",
            "Missing Skills",
            "Experience (years)",
            "Education",
            "Recommendation",
        ]

        header_html = "".join(
            f"<th>{escape(column)}</th>" for column in columns
        )

        body_html = ""

        for row in rows:
            cells = "".join(
                f"<td>{escape(str(row[column]))}</td>"
                for column in columns
            )
            body_html += f"<tr>{cells}</tr>"

        return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Candidate Analysis Report</title>
<style>
body {{ font-family: Arial, sans-serif; margin: 32px; color: #222; }}
h1 {{ color: #433878; }}
.table-wrap {{ overflow-x: auto; }}
table {{ border-collapse: collapse; width: 100%; }}
th, td {{ border: 1px solid #ddd; padding: 10px; text-align: left; }}
th {{ background: #433878; color: white; }}
tr:nth-child(even) {{ background: #f4f4f8; }}
</style>
</head>
<body>
<h1>Intelligent Resume Analyzer</h1>
<p>Candidate analysis report: {len(rows)} candidate(s)</p>
<div class="table-wrap">
<table>
<thead><tr>{header_html}</tr></thead>
<tbody>{body_html}</tbody>
</table>
</div>
</body>
</html>"""
