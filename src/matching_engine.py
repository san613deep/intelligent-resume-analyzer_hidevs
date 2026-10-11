
from dataclasses import dataclass
from difflib import SequenceMatcher

from src.candidate import Candidate
from src.job_analyzer import Job


@dataclass
class MatchResult:
    score: float
    matched_skills: list[str]
    missing_skills: list[str]
    skill_matches: dict[str, str]
    experience_match: bool
    education_match: bool
    recommendation: str


def normalize_skill(skill: str) -> str:
    """Normalize skill names for comparison."""
    return " ".join(skill.lower().strip().split())



def skills_are_equivalent(
    candidate_skill: str,
    required_skill: str,
    threshold: float = 0.85
) -> bool:
    """Match exact skills, aliases, and likely spelling mistakes."""

    candidate = normalize_skill(candidate_skill)
    required = normalize_skill(required_skill)

    if candidate == required:
        return True

    aliases = {
        "js": "javascript",
        "py": "python",
        "postgres": "postgresql",
        "ml": "machine learning",
    }

    candidate = aliases.get(candidate, candidate)
    required = aliases.get(required, required)

    if candidate == required:
        return True

    # Avoid fuzzy matching very short terms.
    if min(len(candidate), len(required)) < 5:
        return False

    # Recognize a single adjacent character transposition,
    # such as "pyhton" instead of "python".
    if len(candidate) == len(required):
        differences = [
            i for i in range(len(candidate))
            if candidate[i] != required[i]
        ]

        if (
            len(differences) == 2
            and differences[1] == differences[0] + 1
            and candidate[differences[0]] == required[differences[1]]
            and candidate[differences[1]] == required[differences[0]]
        ):
            return True

    similarity = SequenceMatcher(
        None, candidate, required
    ).ratio()

    return similarity >= threshold



def match_skills(
    candidate_skills: list[str],
    required_skills: list[str]
) -> tuple[list[str], list[str], dict[str, str]]:
    """Find matched and missing job skills."""

    matched_skills = []
    missing_skills = []
    skill_matches = {}

    used_candidate_skills = set()

    for required_skill in required_skills:
        matched_candidate_skill = None

        for candidate_skill in candidate_skills:
            if candidate_skill in used_candidate_skills:
                continue

            if skills_are_equivalent(
                candidate_skill, required_skill
            ):
                matched_candidate_skill = candidate_skill
                break

        if matched_candidate_skill is not None:
            matched_skills.append(required_skill)
            skill_matches[required_skill] = matched_candidate_skill
            used_candidate_skills.add(matched_candidate_skill)
        else:
            missing_skills.append(required_skill)

    return matched_skills, missing_skills, skill_matches


def meets_education_requirement(
    candidate: Candidate,
    job: Job
) -> bool:
    """Perform a basic education keyword comparison."""

    required = normalize_skill(job.education)
    actual = normalize_skill(candidate.education)

    if not required or not actual:
        return False

    if required in actual:
        return True

    # Handle a few common degree-name variations.
    degree_groups = [
        {"b.tech", "btech", "bachelor of technology"},
        {"b.e.", "be", "bachelor of engineering"},
        {"b.sc", "bsc", "bachelor of science"},
        {"bachelor's degree", "bachelors degree", "bachelor degree"},
        {"m.tech", "mtech", "master of technology"},
        {"m.sc", "msc", "master of science"},
    ]

    for group in degree_groups:
        if required in group and actual in group:
            return True

    return False


class ScoringStrategy:
    """Base class for candidate scoring strategies."""

    def calculate(
        self,
        candidate: Candidate,
        job: Job,
        matched_skills: list[str]
    ) -> float:
        raise NotImplementedError


class BasicScoring(ScoringStrategy):
    """Give equal importance to skills, experience, and education."""

    def calculate(
        self,
        candidate: Candidate,
        job: Job,
        matched_skills: list[str]
    ) -> float:
        if not job.required_skills:
            skill_score = 0.0
        else:
            skill_score = (
                len(matched_skills) / len(job.required_skills)
            )

        experience_score = (
            1.0 if candidate.experience >= job.min_experience
            else 0.0
        )

        education_score = (
            1.0 if meets_education_requirement(candidate, job)
            else 0.0
        )

        return (
            skill_score + experience_score + education_score
        ) / 3 * 100


class WeightedScoring(ScoringStrategy):
    """Score skills, experience, and education using fixed weights."""

    def calculate(
        self,
        candidate: Candidate,
        job: Job,
        matched_skills: list[str]
    ) -> float:
        if job.required_skills:
            skill_score = (
                len(matched_skills) / len(job.required_skills)
            )
        else:
            skill_score = 0.0

        if job.min_experience > 0:
            experience_score = min(
                candidate.experience / job.min_experience, 1.0
            )
        else:
            experience_score = 1.0

        education_score = (
            1.0 if meets_education_requirement(candidate, job)
            else 0.0
        )

        score = (
            skill_score * 60
            + experience_score * 25
            + education_score * 15
        )

        return round(score, 2)


def analyze_candidate(
    candidate: Candidate,
    job: Job,
    strategy: ScoringStrategy | None = None
) -> MatchResult:
    """Compare a candidate against a job and explain the result."""

    matched, missing, skill_matches = match_skills(
        candidate.skills, job.required_skills
    )

    if strategy is None:
        strategy = WeightedScoring()

    score = strategy.calculate(candidate, job, matched)

    experience_match = (
        candidate.experience >= job.min_experience
    )
    education_match = meets_education_requirement(candidate, job)

    if score >= 80:
        recommendation = "STRONGLY RECOMMEND"
    elif score >= 60:
        recommendation = "RECOMMEND"
    elif score >= 40:
        recommendation = "MAYBE"
    else:
        recommendation = "NOT RECOMMENDED"

    return MatchResult(
        score=round(score, 2),
        matched_skills=matched,
        missing_skills=missing,
        skill_matches=skill_matches,
        experience_match=experience_match,
        education_match=education_match,
        recommendation=recommendation,
    )
