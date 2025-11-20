import pytest

from test_utils import (
    require_ids,
    TEST_FILES,
    _resolve_test_uri,
    run_idstools_script,
)


class TestIDSListScript:

    @pytest.fixture(params=TEST_FILES)
    def test_file_path(self, request):
        file_path = request.param
        # Resolve URI (downloads if needed) and return absolute path
        return _resolve_test_uri(file_path)

    def run_idslist(self, args, timeout=120):
        return run_idstools_script("idslist", args, timeout=timeout)

    def test_idslist_default_mode(self, test_file_path):
        result = self.run_idslist(["--uri", test_file_path])

        # Always raise error, don't skip
        if result.returncode != 0:
            raise AssertionError(
                f"Command failed with return code {result.returncode}\nSTDOUT: {result.stdout}\nSTDERR: {result.stderr}"
            )

        assert "List of IDSes" in result.stdout
        assert "IDS" in result.stdout
        assert "SLICES" in result.stdout
        assert "TIME" in result.stdout

    @require_ids("summary")
    def test_idslist_filter_single_ids(self, test_file_path):
        result = self.run_idslist(["--uri", test_file_path, "--ids", "summary"])

        assert result.returncode == 0
        assert "summary" in result.stdout

    @require_ids("summary")
    def test_idslist_fullarray_option(self, test_file_path):
        result = self.run_idslist(["--uri", test_file_path, "-f"])

        assert result.returncode == 0
        assert "TIME" in result.stdout

    @require_ids("summary")
    def test_idslist_yaml_mode(self, test_file_path):
        result = self.run_idslist(["--uri", test_file_path, "-y"])

        assert result.returncode == 0
        assert "time_step_number:" in result.stdout or "time:" in result.stdout

    @require_ids("summary")
    def test_idslist_yaml_with_filter(self, test_file_path):
        result = self.run_idslist(["--uri", test_file_path, "-y", "--ids", "summary"])

        assert result.returncode == 0
        assert "summary" in result.stdout
        assert "time_step_number:" in result.stdout or "time:" in result.stdout

    @require_ids("summary")
    def test_idslist_comment_mode(self, test_file_path):
        result = self.run_idslist(["--uri", test_file_path, "-c"])

        assert result.returncode == 0
        assert "COMMENT" in result.stdout

    @require_ids("summary")
    def test_idslist_dd_version_mode(self, test_file_path):
        result = self.run_idslist(["--uri", test_file_path, "--dd-version"])

        assert result.returncode == 0
        assert "DD VERSION" in result.stdout

    def test_idslist_error_invalid_file(self):
        result = self.run_idslist(["--uri", "nonexistent_file.nc"])

        assert result.returncode != 0
        assert result.returncode == 1


if __name__ == "__main__":
    pytest.main(
        [
            __file__,
            "-v",
            "--tb=short",
            "-x",
        ]
    )
