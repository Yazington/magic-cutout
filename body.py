from dataclasses import dataclass, asdict
import json


@dataclass
class ApplicationSubmission:
    timestamp: str
    name: str
    email: str
    resume_link: str
    repository_link: str
    action_run_link: str

    def to_json(self) -> str:
        """Serialize to compact UTF-8 JSON with sorted keys"""
        return json.dumps(
            asdict(self), separators=(",", ":"), sort_keys=True, ensure_ascii=False
        )
