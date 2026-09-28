# MetricMind Semantic Layer Schemas

from typing import List, Optional

from pydantic import BaseModel


class SemanticQuery(BaseModel):
    """
    Represents a governed query request.
    """

    metric: str

    dimensions: List[str] = []

    region: Optional[str] = None

    country: Optional[str] = None

    category: Optional[str] = None

    start_date: Optional[str] = None

    end_date: Optional[str] = None


class SemanticResult(BaseModel):
    """
    Represents the result returned by the Semantic Layer.
    """

    metric: str

    dimensions: List[str]

    sql: str

    data: list