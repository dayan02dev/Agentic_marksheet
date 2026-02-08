"""Tests for subject normalization."""
import pytest
from app.services.normalize import (
    normalize_subject_name,
    normalize_subjects,
    compute_overall_percent,
    compute_pcm_percent,
    get_pcm_subjects,
    compute_review_reasons
)
from app.models import SubjectNormalized, SubjectStatus


class TestSubjectNormalization:
    """Test subject name normalization."""

    def test_normalize_english_variants(self):
        """Test various English subject name variants."""
        test_cases = [
            ("ENGLISH CORE", "ENGLISH"),
            ("English Language", "ENGLISH"),
            ("eng", "ENGLISH"),
            ("English Communicative", "ENGLISH"),
        ]

        for raw, expected in test_cases:
            normalized, category = normalize_subject_name(raw)
            assert normalized == expected
            assert category == "ENGLISH"

    def test_normalize_physics_variants(self):
        """Test various Physics subject name variants."""
        test_cases = [
            ("PHYSICS", "PHYSICS"),
            ("Physics (042)", "PHYSICS"),
            ("Physics Theory", "PHYSICS"),
        ]

        for raw, expected in test_cases:
            normalized, category = normalize_subject_name(raw)
            assert normalized == expected
            assert category == "PHYSICS"

    def test_normalize_unknown_subject(self):
        """Test unknown subject returns original name."""
        normalized, category = normalize_subject_name("Unknown Subject XYZ")
        assert normalized == "Unknown Subject XYZ"
        assert category == "OTHER"

    def test_normalize_empty_subject(self):
        """Test empty subject handling."""
        normalized, category = normalize_subject_name(None)
        assert normalized == "UNKNOWN"
        assert category == "OTHER"

    def test_normalize_subjects_list(self):
        """Test normalizing a list of subjects."""
        raw_subjects = [
            {"subject_name": "ENGLISH CORE", "obtained_marks": 85, "max_marks": 100, "status": "OK"},
            {"subject_name": "PHYSICS (042)", "obtained_marks": 78, "max_marks": 100, "status": "OK"},
            {"subject_name": "Chemistry", "obtained_marks": 82, "max_marks": 100, "status": "OK"},
            {"subject_name": "MATHEMATICS", "obtained_marks": 90, "max_marks": 100, "status": "OK"},
            {"subject_name": "Computer Science", "obtained_marks": 88, "max_marks": 100, "status": "OK"},
        ]

        normalized = normalize_subjects(raw_subjects)

        assert len(normalized) == 5
        assert normalized[0].normalized_name == "ENGLISH"
        assert normalized[1].normalized_name == "PHYSICS"
        assert normalized[2].normalized_name == "CHEMISTRY"
        assert normalized[3].normalized_name == "MATHEMATICS"


class TestComputations:
    """Test percentage computations."""

    def test_overall_percent(self):
        """Test overall percentage calculation."""
        subjects = [
            SubjectNormalized(
                raw_name="English", normalized_name="ENGLISH", category="ENGLISH",
                obtained_marks=85, max_marks=100, status=SubjectStatus.OK
            ),
            SubjectNormalized(
                raw_name="Physics", normalized_name="PHYSICS", category="PHYSICS",
                obtained_marks=78, max_marks=100, status=SubjectStatus.OK
            ),
            SubjectNormalized(
                raw_name="Chemistry", normalized_name="CHEMISTRY", category="CHEMISTRY",
                obtained_marks=82, max_marks=100, status=SubjectStatus.OK
            ),
            SubjectNormalized(
                raw_name="Mathematics", normalized_name="MATHEMATICS", category="MATHEMATICS",
                obtained_marks=90, max_marks=100, status=SubjectStatus.OK
            ),
            SubjectNormalized(
                raw_name="CS", normalized_name="COMPUTER SCIENCE", category="ELECTIVE",
                obtained_marks=88, max_marks=100, status=SubjectStatus.OK
            ),
        ]

        percent = compute_overall_percent(subjects)
        expected = (85 + 78 + 82 + 90 + 88) / 500 * 100
        assert percent == round(expected, 2)
        assert percent == 84.6

    def test_overall_percent_with_missing(self):
        """Test overall percent with missing values."""
        subjects = [
            SubjectNormalized(
                raw_name="English", normalized_name="ENGLISH", category="ENGLISH",
                obtained_marks=85, max_marks=100, status=SubjectStatus.OK
            ),
            SubjectNormalized(
                raw_name="Physics", normalized_name="PHYSICS", category="PHYSICS",
                obtained_marks=None, max_marks=100, status=SubjectStatus.AB
            ),
        ]

        percent = compute_overall_percent(subjects)
        # Should compute based on available subjects
        assert percent == 85.0

    def test_overall_percent_all_missing(self):
        """Test overall percent when all missing."""
        subjects = [
            SubjectNormalized(
                raw_name="English", normalized_name="ENGLISH", category="ENGLISH",
                obtained_marks=None, max_marks=None, status=SubjectStatus.AB
            ),
        ]

        percent = compute_overall_percent(subjects)
        assert percent is None

    def test_pcm_percent(self):
        """Test PCM percentage calculation."""
        subjects = [
            SubjectNormalized(
                raw_name="English", normalized_name="ENGLISH", category="ENGLISH",
                obtained_marks=85, max_marks=100, status=SubjectStatus.OK
            ),
            SubjectNormalized(
                raw_name="Physics", normalized_name="PHYSICS", category="PHYSICS",
                obtained_marks=80, max_marks=100, status=SubjectStatus.OK
            ),
            SubjectNormalized(
                raw_name="Chemistry", normalized_name="CHEMISTRY", category="CHEMISTRY",
                obtained_marks=70, max_marks=100, status=SubjectStatus.OK
            ),
            SubjectNormalized(
                raw_name="Mathematics", normalized_name="MATHEMATICS", category="MATHEMATICS",
                obtained_marks=90, max_marks=100, status=SubjectStatus.OK
            ),
            SubjectNormalized(
                raw_name="CS", normalized_name="COMPUTER SCIENCE", category="ELECTIVE",
                obtained_marks=88, max_marks=100, status=SubjectStatus.OK
            ),
        ]

        percent = compute_pcm_percent(subjects)
        expected = (80 + 70 + 90) / 3  # Average of percents
        assert percent == round(expected, 2)

    def test_pcm_percent_missing_physics(self):
        """Test PCM percent when Physics is missing."""
        subjects = [
            SubjectNormalized(
                raw_name="English", normalized_name="ENGLISH", category="ENGLISH",
                obtained_marks=85, max_marks=100, status=SubjectStatus.OK
            ),
            SubjectNormalized(
                raw_name="Chemistry", normalized_name="CHEMISTRY", category="CHEMISTRY",
                obtained_marks=70, max_marks=100, status=SubjectStatus.OK
            ),
            SubjectNormalized(
                raw_name="Mathematics", normalized_name="MATHEMATICS", category="MATHEMATICS",
                obtained_marks=90, max_marks=100, status=SubjectStatus.OK
            ),
        ]

        percent = compute_pcm_percent(subjects)
        assert percent is None

    def test_get_pcm_subjects(self):
        """Test extracting PCM subjects."""
        subjects = [
            SubjectNormalized(
                raw_name="English", normalized_name="ENGLISH", category="ENGLISH",
                obtained_marks=85, max_marks=100, status=SubjectStatus.OK
            ),
            SubjectNormalized(
                raw_name="Physics", normalized_name="PHYSICS", category="PHYSICS",
                obtained_marks=80, max_marks=100, status=SubjectStatus.OK
            ),
            SubjectNormalized(
                raw_name="Chemistry", normalized_name="CHEMISTRY", category="CHEMISTRY",
                obtained_marks=70, max_marks=100, status=SubjectStatus.OK
            ),
            SubjectNormalized(
                raw_name="Mathematics", normalized_name="MATHEMATICS", category="MATHEMATICS",
                obtained_marks=90, max_marks=100, status=SubjectStatus.OK
            ),
        ]

        pcm = get_pcm_subjects(subjects)

        assert pcm["physics"] is not None
        assert pcm["chemistry"] is not None
        assert pcm["mathematics"] is not None
        assert pcm["physics"].obtained_marks == 80
        assert pcm["chemistry"].obtained_marks == 70
        assert pcm["mathematics"].obtained_marks == 90


class TestReviewReasons:
    """Test review reason generation."""

    def test_review_reasons_for_ab_subject(self):
        """Test review reasons for absent subject."""
        subjects = [
            SubjectNormalized(
                raw_name="English", normalized_name="ENGLISH", category="ENGLISH",
                obtained_marks=None, max_marks=100, status=SubjectStatus.AB
            ),
        ]

        reasons = compute_review_reasons(subjects)
        assert len(reasons) > 0
        assert any("AB" in r for r in reasons)

    def test_review_reasons_for_missing_marks(self):
        """Test review reasons for missing marks."""
        subjects = [
            SubjectNormalized(
                raw_name="English", normalized_name="ENGLISH", category="ENGLISH",
                obtained_marks=None, max_marks=None, status=SubjectStatus.UNKNOWN
            ),
        ]

        reasons = compute_review_reasons(subjects)
        assert len(reasons) > 0
        assert any("Missing" in r for r in reasons)

    def test_review_reasons_clean_record(self):
        """Test review reasons for clean record."""
        subjects = [
            SubjectNormalized(
                raw_name="English", normalized_name="ENGLISH", category="ENGLISH",
                obtained_marks=85, max_marks=100, status=SubjectStatus.OK
            ),
        ]

        reasons = compute_review_reasons(subjects)
        assert len(reasons) == 0
