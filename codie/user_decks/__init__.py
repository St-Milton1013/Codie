"""User deck import and analysis-session helpers."""

from .analysis_input import (
    UserDeckAnalysisCard,
    UserDeckAnalysisInput,
    UserDeckAnalysisInputError,
    build_user_deck_analysis_input,
)
from .evidence_comparison import (
    UserDeckEvidenceCandidate,
    UserDeckEvidenceComparison,
    UserDeckEvidenceComparisonRow,
    compare_user_deck_to_evidence,
)
from .importer import (
    ParsedUserDeck,
    ParsedUserDeckCard,
    UserDeckImportError,
    UserDeckImportResult,
    UserDeckImporter,
    parse_user_deck_text,
)
from .saved_analysis import SavedUserDeckAnalysisResult, save_user_deck_comparison_analysis

__all__ = [
    "ParsedUserDeck",
    "ParsedUserDeckCard",
    "UserDeckAnalysisCard",
    "UserDeckAnalysisInput",
    "UserDeckAnalysisInputError",
    "UserDeckEvidenceCandidate",
    "UserDeckEvidenceComparison",
    "UserDeckEvidenceComparisonRow",
    "UserDeckImportError",
    "UserDeckImportResult",
    "UserDeckImporter",
    "SavedUserDeckAnalysisResult",
    "build_user_deck_analysis_input",
    "compare_user_deck_to_evidence",
    "parse_user_deck_text",
    "save_user_deck_comparison_analysis",
]
