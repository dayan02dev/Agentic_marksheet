"""Pytest configuration and fixtures."""
import pytest
import sys
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))


@pytest.fixture
def temp_file(tmp_path):
    """Create a temporary file."""
    def _make_file(name: str, content: str = "test content"):
        file_path = tmp_path / name
        file_path.write_text(content)
        return file_path
    return _make_file


@pytest.fixture
def temp_image(tmp_path):
    """Create a temporary test image."""
    def _make_image(name: str, size: tuple = (100, 100)):
        from PIL import Image
        img = Image.new('RGB', size, color='white')
        file_path = tmp_path / name
        img.save(file_path, 'PNG')
        return file_path
    return _make_image
