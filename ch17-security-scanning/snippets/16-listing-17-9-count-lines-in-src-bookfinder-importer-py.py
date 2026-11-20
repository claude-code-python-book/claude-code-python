def count_lines(path: Path) -> int:
    """Count lines with wc, passing the file name as one argument, no shell."""
    result = subprocess.run(  # noqa: S603 - fixed program, argument list, no shell
        ["wc", "-l", "--", str(path)],  # noqa: S607 - wc is found on PATH
        capture_output=True,
        text=True,
        check=True,
        timeout=10,
    )
    return int(result.stdout.split()[0])
