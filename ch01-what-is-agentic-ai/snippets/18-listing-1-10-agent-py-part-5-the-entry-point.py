if __name__ == "__main__":
    report = run_agent(
        "Find every TODO or FIXME comment in this project. Group them by "
        "file, include the line number, and add a one-line summary of "
        "what each one asks for."
    )
    print(report)
