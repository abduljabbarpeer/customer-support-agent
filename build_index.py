"""Builds the help-document search index. Run: .venv/bin/python build_index.py"""

from support_agent.help_docs import build_index

parts, files = build_index()
print(f"Saved {parts} parts from {files} files.")
