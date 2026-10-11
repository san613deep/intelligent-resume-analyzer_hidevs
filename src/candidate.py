from dataclasses import dataclass, field

@dataclass
class Candidate:
    name: str = ""
    email: str =""
    skills: List[str] = field(default_factory=list)
    experience: float = 0.0
    education: str = ""