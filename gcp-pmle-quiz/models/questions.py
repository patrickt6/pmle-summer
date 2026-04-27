from typing import Literal

from pydantic import BaseModel, Field


class Question(BaseModel):
    id: int
    mode: Literal["single_choice", "multiple_choice"]
    question: str
    options: list[str]
    answer: int | list[int]  # index of the correct option
    explanation: str | None = None
    source: str | None = Field(
        default=None,
        description="Bank source: 'AndyTheFactory', 'Google Sample', 'Whizlabs', etc.",
    )
    exam_section: str | None = Field(
        default=None,
        description=(
            "PMLE v3.1 section. Allowed: §1.1, §1.2, §2.1, §2.2, §2.3, "
            "§3.1, §3.2, §3.3, §3.4, §4.1, §4.2, §4.3, §5.1, §5.2, §5.3, §6.1, §6.2."
        ),
    )
    mock_pool: list[str] | None = Field(
        default=None,
        description=(
            "Mock pool tags. Allowed values: 'mock1-pool', 'mock2-pool'. "
            "Default null = available for normal quiz mode."
        ),
    )
