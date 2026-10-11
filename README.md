# Intelligent Resume Analyzer

An intelligent resume screening application built with Python and Streamlit. It analyzes resumes against job requirements, evaluates candidate suitability, calculates a matching score, and generates downloadable analysis reports.

## Overview

Recruiters often need to review many resumes for a single job opening. This project helps simplify the initial screening process by extracting candidate information from resumes and comparing it with the skills, experience, and education required for a position.

The application provides a simple web interface where users can enter job requirements, upload a resume, review the analysis results, and export the report in different formats.

**Note:** The analyzer uses rule-based parsing and scoring. Its results are intended to support initial screening, not replace human recruitment decisions.

## Features

- **Resume parsing:** Extracts candidate information such as name, email, skills, experience, and education.
- **Multiple file formats:** Supports TXT, PDF, and DOCX resume uploads.
- **Job requirement input:** Enter the job title, required skills, minimum experience, and education requirement.
- **Candidate matching:** Compares resume details with the job requirements.
- **Skill matching:** Supports skill comparison and selected similar skill names.
- **Match score:** Calculates an overall candidate matching score.
- **Analysis report:** Generates a report describing the candidate's match with the job.
- **Multiple export formats:** Download reports as PDF, Excel, or HTML.
- **JSON storage:** Save and load analysis results using JSON files.
- **Interactive interface:** Use the application through a Streamlit web interface.
- **Automated tests:** Includes tests for matching, file handling, and report generation.

## Technologies Used

- Python
- Streamlit
- PyMuPDF for PDF text extraction
- python-docx for DOCX text extraction
- Pandas and OpenPyXL for Excel reports
- ReportLab for PDF report generation
- JSON for saving analysis results
- Pytest for automated testing

## Project Structure

```text
Intelligent-Resume-Analyzer_HiDevs/
├── app.py
├── requirements.txt
├── README.md
├── .gitignore
├── data/
├── sample_resume/
│   └── rahul.txt
├── src/
│   ├── __init__.py
│   ├── candidate.py
│   ├── file_handler.py
│   ├── job_analyzer.py
│   ├── matching_engine.py
│   ├── report_generator.py
│   └── resume_parser.py
└── tests/
    ├── test_file_handler.py
    ├── test_matching.py
    ├── test_report_generator.py
    └── test_report_exporter.py
```

## Installation and Setup

### 1. Clone the repository

```bash
git clone https://github.com/san613deep/Intelligent-Resume-Analyzer_HiDevs.git
cd Intelligent-Resume-Analyzer_HiDevs
```

### 2. Create a virtual environment

```bash
python -m venv .venv
```

Activate it using the command for your operating system.

**Windows:**

```bash
.venv\Scripts\activate
```

**Linux or macOS:**

```bash
source .venv/bin/activate
```

### 3. Install dependencies

```bash
python -m pip install -r requirements.txt
```

## Run the Application

Start the Streamlit application with:

```bash
streamlit run app.py
```

Streamlit will provide a local or forwarded URL. Open that URL in your browser to use the application.

## How to Use

1. Start the application.
2. Enter the job title and required skills.
3. Specify the minimum required experience and education.
4. Upload a candidate's resume in TXT, PDF, or DOCX format.
5. Run the analysis.
6. Review the candidate information, matching score, and analysis report.
7. Download the report in an available format.
8. Save or load analysis results where needed.

A sample resume is provided in `sample_resume/rahul.txt` for testing.

## Matching and Scoring

The matching engine evaluates a candidate against the selected job requirements.

The weighted scoring strategy uses the following components:

| Component | Weight |
|---|---:|
| Skills match | 60% |
| Experience match | 25% |
| Education match | 15% |
| **Total** | **100%** |

The score combines the skills, experience, and education components according to these weights. The matching engine also includes skill normalization and selected similarity matching to handle certain variations in skill names.

The project includes scoring strategies and recommendation thresholds in the matching engine. The final result should be reviewed alongside the candidate's actual resume and the job requirements.

## Report Export and Data Storage

The application supports the following outputs:

- **PDF:** A downloadable analysis report.
- **Excel:** A spreadsheet report.
- **HTML:** An HTML version of the report.
- **JSON:** Save and reload analysis results.

The exact analysis depends on the information successfully extracted from the uploaded resume.

## Running Tests

Run the automated test suite from the project root:

```bash
python -m pytest -v
```

The tests cover areas including resume file handling, candidate matching, report generation, and report exports.

## Current Limitations

- Resume parsing relies on recognizable text and expected labels or sections. Resumes with unusual layouts may not be parsed accurately.
- Scanned PDFs may require OCR before their text can be extracted.
- The matching score is a rule-based estimate, not a guarantee of candidate suitability.
- Similarity matching may not recognize every variation of a skill or job title.
- Candidate details and generated reports should be checked for accuracy before making recruitment decisions.

## Future Improvements

- Improve parsing for resumes with different layouts and section headings.
- Add OCR support for scanned resumes.
- Expand skill normalization and job-specific matching.
- Add more comprehensive validation and error handling.
- Introduce optional AI-assisted analysis with appropriate evaluation and safeguards.

## Demo

**YouTube demonstration:** Add the public YouTube link here after recording and uploading the project demonstration.

## Author

**Sandeep**

## License

This project was created as part of the HiDevs Day 10 project challenge. No separate open-source license has been specified.
