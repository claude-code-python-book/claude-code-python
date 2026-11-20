TOOL_SCHEMAS: list[dict[str, Any]] = [
    {
        "name": "list_python_files",
        "description": "List all .py files under a directory of the project.",
        "input_schema": {
            "type": "object",
            "properties": {
                "directory": {"type": "string",
                              "description": "Relative path, e.g. 'src'"},
            },
            "required": [],
        },
    },
    {
        "name": "read_file",
        "description": "Read one file. Lines are prefixed with numbers.",
        "input_schema": {
            "type": "object",
            "properties": {"path": {"type": "string"}},
            "required": ["path"],
        },
    },
]

SYSTEM_PROMPT = (
    "You are a code-auditing agent. Use the tools to inspect the project. "
    "Only report what you actually read in a file. When you are done, "
    "answer with a short Markdown report and stop calling tools."
)
