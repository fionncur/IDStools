#!/usr/bin/env python3
"""
Test to verify that all configured test files are present and accessible with IMAS.

This test file ensures that:
1. All test files in TEST_FILES configuration are present
2. All test files can be opened with IMAS
3. All test files contain valid IDS data

Usage:
    pytest tests/test_verify_files.py -v
    pytest tests/test_verify_files.py -v --tb=short
"""

import pytest
import logging

from test_utils import verify_test_files_accessible, TEST_FILES

logger = logging.getLogger(__name__)


class TestVerifyTestFiles:
    """Test suite to verify test file availability and accessibility."""

    def test_test_files_configured(self):
        """Verify that TEST_FILES is not empty."""
        assert TEST_FILES, "No test files configured in TEST_FILES. Check test configuration."
        logger.info(f"✓ {len(TEST_FILES)} test files configured")

    def test_all_test_files_accessible_with_imas(self):
        """
        Verify that all configured test files are present and accessible with IMAS.

        This test:
        - Downloads missing test files if URLs are available
        - Attempts to open each file with IMAS
        - Verifies that each file contains valid IDS data
        """
        results = verify_test_files_accessible()

        # Log summary
        logger.info(f"\n{'='*70}")
        logger.info(f"Test File Verification Summary")
        logger.info(f"{'='*70}")
        logger.info(f"Total files:         {results['total']}")
        logger.info(f"Accessible:          {results['accessible_count']}")
        logger.info(f"Inaccessible:        {results['inaccessible_count']}")
        logger.info(f"{'='*70}")

        # Log accessible files
        if results["accessible"]:
            logger.info("\n✓ Accessible Files:")
            for file_info in results["accessible"]:
                logger.info(f"  - {file_info['file']}")
                logger.info(f"    Path: {file_info['path']}")
                logger.info(f"    IDS count: {file_info['ids_count']}")

        # Log inaccessible files
        if results["inaccessible"]:
            logger.error("\n✗ Inaccessible Files:")
            for file_info in results["inaccessible"]:
                logger.error(f"  - {file_info['file']}")
                logger.error(f"    Error: {file_info['error']}")

        # Assert all files are accessible
        assert results["inaccessible_count"] == 0, (
            f"Some test files are not accessible:\n"
            f"{', '.join(f['file'] for f in results['inaccessible'])}\n"
            f"See logs above for details."
        )

        logger.info("\n✓ All test files are accessible!")


if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short", "--log-cli-level=INFO"])
