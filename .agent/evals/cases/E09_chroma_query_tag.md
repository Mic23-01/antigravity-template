# E09 — Chroma query by tag: find only topic=playwright

## Prompt
"Search in technical memory for all logs that have the 'playwright' tag."

## Expected
- Use of `chroma_query_documents` with filter `where_document={"$contains": "playwright"}` or appropriate metadata filter.
- Results correctly filtered to show only the requested topic.
PASS/FAIL: manual/Chroma check.
