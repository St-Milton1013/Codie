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
from .saved_analysis_listing import (
    SavedAnalysisDetail,
    SavedAnalysisReadError,
    SavedAnalysisSummary,
    get_saved_user_deck_analysis,
    list_saved_user_deck_analyses,
)

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
    "SavedAnalysisDetail",
    "SavedAnalysisReadError",
    "SavedAnalysisSummary",
    "build_user_deck_analysis_input",
    "compare_user_deck_to_evidence",
    "get_saved_user_deck_analysis",
    "list_saved_user_deck_analyses",
    "parse_user_deck_text",
    "save_user_deck_comparison_analysis",
]
