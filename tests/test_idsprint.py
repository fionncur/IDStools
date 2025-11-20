import pytest
import tempfile
from pathlib import Path
import shutil

from test_utils import (
    require_ids,
    TEST_FILES,
    _resolve_test_uri,
    check_result_skip_if_empty_or_error,
    run_idstools_script,
)


class TestIDSPrintScript:

    @pytest.fixture(params=TEST_FILES)
    def test_file_path(self, request):
        file_path = request.param
        # Resolve URI (downloads if needed) and return absolute path
        return _resolve_test_uri(file_path)

    @pytest.fixture
    def temp_output_dir(self):
        temp_dir = tempfile.mkdtemp()
        yield temp_dir
        shutil.rmtree(temp_dir, ignore_errors=True)

    def run_idsprint(self, args, timeout=60):
        return run_idstools_script("idsprint", args, timeout=timeout)

    def test_idsprint_list_available_ids(self, test_file_path):
        result = self.run_idsprint(["--uri", test_file_path])

        assert result.returncode == 1
        assert "summary" in result.stdout

    @require_ids("summary")
    def test_idsprint_show_summary_structure(self, test_file_path):
        result = self.run_idsprint(["--uri", f"{test_file_path}#summary"])

        assert result.returncode == 0
        assert "summary" in result.stdout
        assert "time:" in result.stdout or "time" in result.stdout
        assert "global_quantities/ip" in result.stdout

    @require_ids("summary")
    def test_idsprint_inspect_time_field(self, test_file_path):
        result = self.run_idsprint(["--uri", f"{test_file_path}#summary/time", "-i"])

        assert result.returncode == 0
        assert "IDS value: time" in result.stdout
        assert "DD version" in result.stdout
        assert "has_value = True" in result.stdout
        assert "data_type = 'FLT_1D'" in result.stdout

    @require_ids("summary")
    def test_idsprint_plot_time_field(self, test_file_path, temp_output_dir):
        result = self.run_idsprint(
            ["--uri", f"{test_file_path}#summary/time", "-p", "--save", "--directory", temp_output_dir]
        )

        assert result.returncode == 0
        assert "Coordinates are empty, creating default" in result.stdout
        assert "Figure saved to" in result.stdout or "Figure saved to" in result.stderr

        plot_files = list(Path(temp_output_dir).glob("*.png"))
        assert len(plot_files) == 1

        plot_file = plot_files[0]
        assert plot_file.exists()
        assert plot_file.stat().st_size > 1000

    @require_ids("summary")
    def test_idsprint_compact_output(self, test_file_path):
        result = self.run_idsprint(["--uri", f"{test_file_path}#summary", "-c"])

        assert result.returncode == 0
        assert "summary" in result.stdout
        assert "array" not in result.stdout

    @require_ids("summary")
    def test_idsprint_show_empty_fields(self, test_file_path):
        result = self.run_idsprint(["--uri", f"{test_file_path}#summary", "-e"])

        check_result_skip_if_empty_or_error(result)
        assert result.returncode == 0
        assert "summary" in result.stdout
        assert "value_error_upper" in result.stdout

    @require_ids("summary")
    def test_idsprint_full_array_output(self, test_file_path):
        result = self.run_idsprint(["--uri", f"{test_file_path}#summary/time", "-f"])

        assert result.returncode == 0
        assert "array([" in result.stdout or "numpy.ndarray([" in result.stdout

    @require_ids("summary")
    def test_idsprint_error_invalid_path(self, test_file_path):
        result = self.run_idsprint(["--uri", f"{test_file_path}#summary/nonexistent_field"])

        assert result.returncode == 0
        assert "path does not exist" in result.stdout

    def test_idsprint_error_invalid_file(self):
        result = self.run_idsprint(["--uri", "nonexistent_file.nc"])

        assert result.returncode != 0
        assert "provide valid URI" in result.stdout

    @require_ids("equilibrium")
    def test_idsprint_equilibrium_structure(self, test_file_path):
        result = self.run_idsprint(["--uri", f"{test_file_path}#equilibrium"], timeout=120)

        check_result_skip_if_empty_or_error(result)
        assert result.returncode == 0
        assert "equilibrium" in result.stdout

    @require_ids("plasma_profiles")
    def test_idsprint_core_profiles_temperature(self, test_file_path):
        result = self.run_idsprint(["--uri", f"{test_file_path}#plasma_profiles/profiles_1d(:)/electrons/temperature"])

        check_result_skip_if_empty_or_error(result)
        assert result.returncode == 0
        assert "float64" in result.stdout and "array([[" in result.stdout

    @require_ids("edge_profiles")
    def test_idsprint_edge_profiles_grid_names(self, test_file_path):
        result = self.run_idsprint(
            ["--uri", f"{test_file_path}#edge_profiles/grid_ggd[0]/grid_subset[:]/identifier/name"]
        )

        check_result_skip_if_empty_or_error(result)

        assert result.returncode == 0
        assert "dtype='<U" in result.stdout and "array([" in result.stdout

    @require_ids("plasma_profiles")
    def test_idsprint_core_profiles_ion_labels(self, test_file_path):
        result = self.run_idsprint(["--uri", f"{test_file_path}#plasma_profiles/profiles_1d[0]/ion[:]/label"])

        check_result_skip_if_empty_or_error(result)

        assert result.returncode == 0
        assert "dtype='<U" in result.stdout and "array([" in result.stdout

    @require_ids("plasma_profiles")
    def test_idsprint_core_profiles_temperature_single_time(self, test_file_path):
        result = self.run_idsprint(["--uri", f"{test_file_path}#plasma_profiles/profiles_1d[0]/electrons/temperature"])

        check_result_skip_if_empty_or_error(result)
        assert result.returncode == 0
        assert "numpy.ndarray|(" in result.stdout and ")|float64" in result.stdout

    @require_ids("plasma_profiles")
    def test_idsprint_core_profiles_temperature_range_with_index(self, test_file_path):
        result = self.run_idsprint(
            ["--uri", f"{test_file_path}#plasma_profiles/profiles_1d(0:2)/electrons/temperature[0]"]
        )

        check_result_skip_if_empty_or_error(result)
        assert result.returncode == 0
        assert "numpy.ndarray|(" in result.stdout and ")|float64" in result.stdout

    @require_ids("plasma_profiles")
    def test_idsprint_core_profiles_temperature_step_slice(self, test_file_path):
        result = self.run_idsprint(
            ["--uri", f"{test_file_path}#plasma_profiles/profiles_1d(::2)/electrons/temperature"]
        )

        check_result_skip_if_empty_or_error(result)
        assert result.returncode == 0
        assert "numpy.ndarray|(" in result.stdout and "," in result.stdout and ")|float64" in result.stdout

    @require_ids("plasma_profiles")
    def test_idsprint_core_profiles_temperature_first_two(self, test_file_path):
        result = self.run_idsprint(["--uri", f"{test_file_path}#plasma_profiles/profiles_1d(:2)/electrons/temperature"])

        check_result_skip_if_empty_or_error(result)
        assert result.returncode == 0
        assert "numpy.ndarray|(" in result.stdout and "," in result.stdout and ")|float64" in result.stdout

    @require_ids("plasma_profiles")
    def test_idsprint_core_profiles_temperature_all_times(self, test_file_path):
        result = self.run_idsprint(["--uri", f"{test_file_path}#plasma_profiles/profiles_1d(::)/electrons/temperature"])

        check_result_skip_if_empty_or_error(result)
        assert result.returncode == 0
        assert "numpy.ndarray|(" in result.stdout and "," in result.stdout and ")|float64" in result.stdout

    @require_ids("edge_profiles")
    def test_idsprint_edge_profiles_grid_range(self, test_file_path):
        result = self.run_idsprint(
            ["--uri", f"{test_file_path}#edge_profiles/grid_ggd[0]/grid_subset[0:52]/identifier/name"]
        )

        check_result_skip_if_empty_or_error(result)

        assert result.returncode == 0
        assert "array([" in result.stdout


class TestIDSPrintExportFunctionality:

    @pytest.fixture(params=TEST_FILES)
    def test_file_path(self, request):
        file_path = request.param
        # Resolve URI (downloads if needed) and return absolute path
        return _resolve_test_uri(file_path)

    @pytest.fixture
    def temp_output_dir(self):
        temp_dir = tempfile.mkdtemp()
        yield temp_dir
        shutil.rmtree(temp_dir, ignore_errors=True)

    def run_idsprint(self, args):
        return run_idstools_script("idsprint", args, timeout=120)

    @require_ids("summary")
    @pytest.mark.parametrize("export_type", ["json", "mat"])
    def test_idsprint_export_formats(self, test_file_path, temp_output_dir, export_type):
        result = self.run_idsprint(
            [
                "--uri",
                f"{test_file_path}#summary/time",
                "--export",
                "--export-type",
                export_type,
                "--directory",
                temp_output_dir,
            ]
        )

        assert result.returncode == 0
        assert f"{export_type.upper()} file" in result.stdout
        assert "successfully!" in result.stdout

        expected_extension = export_type
        export_files = list(Path(temp_output_dir).glob(f"*.{expected_extension}"))
        assert len(export_files) == 1

        export_file = export_files[0]
        assert export_file.exists()
        assert export_file.stat().st_size > 10

        if export_type == "json":
            import json

            with open(export_file, "r") as f:
                data = json.load(f)
            assert "summary" in data
            assert isinstance(data, dict)


if __name__ == "__main__":
    pytest.main(
        [
            __file__,
            "-v",
            "--tb=short",
            "-x",
        ]
    )
