echo '{"cwd": "'$PWD'", "tool_name": "Write",
  "tool_input": {"file_path": "'$PWD'/src/invoicer/fees.py"}}' |
  python3 .claude/hooks/format_python.py; echo "exit $?"
