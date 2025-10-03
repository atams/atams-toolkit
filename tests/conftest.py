"""
Pytest configuration
"""
import pytest
from pathlib import Path


@pytest.fixture
def test_project_dir(tmp_path):
    """Create temporary project directory for testing"""
    return tmp_path / "test_project"


@pytest.fixture
def sample_resource_name():
    """Sample resource name for testing"""
    return "department"


@pytest.fixture
def sample_resource_names():
    """Sample resource naming variations for testing"""
    return {
        'singular': 'department',
        'plural': 'departments',
        'pascal_singular': 'Department',
        'pascal_plural': 'Departments',
        'snake_singular': 'department',
        'snake_plural': 'departments',
        'prefix': 'd',
        'title_singular': 'Department',
        'title_plural': 'Departments',
    }
