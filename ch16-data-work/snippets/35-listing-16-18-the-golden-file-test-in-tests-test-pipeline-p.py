def test_sample_report_matches_golden_file(tmp_path: Path) -> None:
    result = run(SAMPLE, tmp_path, "2026-10")
    assert (tmp_path / "report.md").read_text() == GOLDEN.read_text()
    assert (
        result.rows_read == result.valid + result.rejected + result.duplicates_dropped
    )
