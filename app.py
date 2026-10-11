
import tempfile
from pathlib import Path


import streamlit as st

from src.file_handler import (
    extract_text_from_file,
    save_analysis_result,
    load_analysis_results,
)
from src.resume_parser import parse_resume
from src.job_analyzer import Job
from src.matching_engine import (
    BasicScoring,
    WeightedScoring,
    analyze_candidate,
)
from src.report_generator import (
    generate_analysis_report,
    ReportExporter,
)


st.set_page_config(
    page_title="Intelligent Resume Analyzer",
    page_icon="📄",
    layout="wide",
)

st.title("📄 Intelligent Resume Analyzer")
st.write(
    "Upload resumes, compare qualifications against a job, "
    "and generate explainable candidate assessments."
)

st.info(
    "This application provides decision support. "
    "Review candidate information and recommendations yourself."
)


# -------------------------------
# Job requirements
# -------------------------------

st.header("1. Define the job")

with st.form("job_form"):
    job_title = st.text_input(
        "Job title",
        value="Python Developer",
    )

    required_skills_text = st.text_input(
        "Required skills (comma-separated)",
        value="Python, SQL, Git, Django",
    )

    min_experience = st.number_input(
        "Minimum experience (years)",
        min_value=0.0,
        max_value=50.0,
        value=2.0,
        step=0.5,
    )

    education = st.text_input(
        "Education requirement",
        value="Bachelor degree",
    )

    scoring_method = st.selectbox(
        "Scoring algorithm",
        ["Weighted scoring", "Basic scoring"],
    )

    submitted = st.form_submit_button("Save job requirements")


if submitted:
    st.session_state["job"] = Job(
        title=job_title.strip(),
        required_skills=[
            skill.strip()
            for skill in required_skills_text.split(",")
            if skill.strip()
        ],
        min_experience=min_experience,
        education=education.strip(),
    )
    st.session_state["scoring_method"] = scoring_method


# -------------------------------
# Resume uploads
# -------------------------------

st.header("2. Upload resumes")

uploaded_files = st.file_uploader(
    "Choose one or more resumes",
    type=["pdf", "docx", "txt"],
    accept_multiple_files=True,
    help="Supported formats: PDF, DOCX, and TXT.",
)

if st.button(
    "Analyze candidates",
    type="primary",
    disabled=not uploaded_files,
):
    job = st.session_state.get("job")

    if job is None:
        st.error("Please save the job requirements first.")

    elif not job.title:
        st.error("Please provide a job title.")

    elif not job.required_skills:
        st.error("Please provide at least one required skill.")

    else:
        strategy_name = st.session_state.get(
            "scoring_method",
            "Weighted scoring",
        )

        if strategy_name == "Basic scoring":
            strategy = BasicScoring()
        else:
            strategy = WeightedScoring()

        results = []

        for uploaded_file in uploaded_files:
            try:
                suffix = Path(uploaded_file.name).suffix.lower()

                # Save the upload temporarily so the existing
                # file handler can read PDF, DOCX, or TXT.
                with tempfile.NamedTemporaryFile(
                    suffix=suffix,
                    delete=False,
                ) as temporary_file:
                    temporary_file.write(uploaded_file.getvalue())
                    temporary_path = Path(temporary_file.name)

                try:
                    text = extract_text_from_file(
                        str(temporary_path)
                    )
                finally:
                    temporary_path.unlink(missing_ok=True)

                if not text.strip():
                    st.warning(
                        f"{uploaded_file.name}: "
                        "No readable text was found."
                    )
                    continue

                candidate = parse_resume(text)

                if not candidate.name:
                    candidate.name = Path(
                        uploaded_file.name
                    ).stem

                result = analyze_candidate(
                    candidate,
                    job,
                    strategy,
                )

                report = generate_analysis_report(
                    candidate,
                    job,
                    result,
                )

                results.append(
                    {
                        "filename": uploaded_file.name,
                        "candidate": candidate,
                        "result": result,
                        "report": report,
                    }
                )

            except Exception as exc:
                st.warning(
                    f"Could not process {uploaded_file.name}: {exc}"
                )

        st.session_state["analysis_results"] = results
        st.session_state["analysis_job"] = job

        st.success(
            f"Analysis completed for {len(results)} candidate(s)."
        )


# -------------------------------
# Candidate results
# -------------------------------

results = st.session_state.get("analysis_results", [])
job = st.session_state.get("analysis_job")

if results and job:
    st.header("3. Candidate analysis")

    # Highest-scoring candidates appear first.
    results = sorted(
        results,
        key=lambda item: item["result"].score,
        reverse=True,
    )

    summary_columns = st.columns(3)

    summary_columns[0].metric(
        "Candidates analyzed",
        len(results),
    )

    summary_columns[1].metric(
        "Highest match score",
        f"{results[0]['result'].score:.1f}/100",
    )

    summary_columns[2].metric(
        "Average match score",
        f"{sum(item['result'].score for item in results) / len(results):.1f}/100",
    )

    for index, item in enumerate(results, start=1):
        candidate = item["candidate"]
        result = item["result"]

        with st.expander(
            f"{index}. {candidate.name} — {result.score:.1f}/100",
            expanded=(index == 1),
        ):
            left, right = st.columns(2)

            with left:
                st.subheader("Candidate details")
                st.write(f"**Email:** {candidate.email or 'Not provided'}")
                st.write(
                    f"**Experience:** {candidate.experience} years"
                )
                st.write(
                    f"**Education:** {candidate.education or 'Not provided'}"
                )

            with right:
                st.subheader("Assessment")
                st.metric("Match score", f"{result.score:.1f}/100")
                st.write(
                    f"**Recommendation:** {result.recommendation}"
                )
                st.write(
                    f"**Experience:** "
                    f"{'Meets requirement' if result.experience_match else 'Does not meet requirement'}"
                )
                st.write(
                    f"**Education:** "
                    f"{'Meets requirement' if result.education_match else 'Does not meet requirement'}"
                )

            st.subheader("Skills analysis")

            skill_columns = st.columns(2)

            with skill_columns[0]:
                st.write("**Matched skills**")
                if result.matched_skills:
                    for skill in result.matched_skills:
                        source_skill = result.skill_matches[skill]
                        st.write(f"✅ {skill} (resume: {source_skill})")
                else:
                    st.write("No matching skills found.")

            with skill_columns[1]:
                st.write("**Missing skills**")
                if result.missing_skills:
                    for skill in result.missing_skills:
                        st.write(f"⚠️ {skill}")
                else:
                    st.write("No required skills are missing.")

            st.subheader("Full report")
            st.text(item["report"])

            st.download_button(
                "Download text report",
                data=item["report"],
                file_name=f"candidate_report_{index}.txt",
                mime="text/plain",
                key=f"report_download_{index}",
            )

    
    st.header("5. Export analysis results")

    export_data = [
        {
            "candidate": item["candidate"],
            "job": job,
            "result": item["result"],
        }
        for item in results
    ]

    col_pdf, col_excel, col_html = st.columns(3)

    try:
        with col_pdf:
            pdf_data = ReportExporter.export_pdf(export_data)

            st.download_button(
                "Download PDF",
                data=pdf_data,
                file_name="candidate_analysis.pdf",
                mime="application/pdf",
                key="export_pdf",
            )

        with col_excel:
            excel_data = ReportExporter.export_excel(export_data)

            st.download_button(
                "Download Excel",
                data=excel_data,
                file_name="candidate_analysis.xlsx",
                mime=(
                    "application/vnd.openxmlformats-officedocument."
                    "spreadsheetml.sheet"
                ),
                key="export_excel",
            )

        with col_html:
            html_data = ReportExporter.export_html(export_data)

            st.download_button(
                "Download HTML",
                data=html_data,
                file_name="candidate_analysis.html",
                mime="text/html",
                key="export_html",
            )

    except Exception as exc:
        st.error(f"Could not generate exports: {exc}")


    # Save results only when the user clicks the button.
    if st.button("Save all results to JSON"):
        try:
            for item in results:
                save_analysis_result(
                    item["candidate"],
                    job,
                    item["result"],
                )

            st.success("Analysis results saved to data/analysis_results.json")

        except (OSError, ValueError) as exc:
            st.error(f"Could not save results: {exc}")


# -------------------------------
# Previously saved analyses
# -------------------------------

st.header("4. Saved analysis history")

if st.button("Load saved JSON results"):
    try:
        saved_results = load_analysis_results()
        st.session_state["saved_results"] = saved_results
    except (OSError, ValueError) as exc:
        st.error(f"Could not load saved results: {exc}")

saved_results = st.session_state.get("saved_results", [])

if saved_results:
    st.write(f"Saved analysis records: {len(saved_results)}")
    st.json(saved_results)
elif "saved_results" in st.session_state:
    st.caption("No saved analyses were found.")
