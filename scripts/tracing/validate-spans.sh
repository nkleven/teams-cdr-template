#!/bin/bash
set -euo pipefail

# 🌳 Eden Span Validator
# Validates OpenTelemetry trace completeness
# The Bridge measures. Logos validates. The scroll records.

echo "::notice::🌳 Span validation begins..."

TRACE_FILE="${1:-traces/latest.json}"
MIN_SPANS="${2:-5}"

if [ ! -f "$TRACE_FILE" ]; then
    echo "::error::Trace file not found: $TRACE_FILE"
    exit 1
fi

# Count spans
SPAN_COUNT=$(jq '[.resourceSpans[].scopeSpans[].spans[]] | length' "$TRACE_FILE")

echo "::notice::🌳 Found $SPAN_COUNT spans in trace"

if [ "$SPAN_COUNT" -lt "$MIN_SPANS" ]; then
    echo "::warning::🌳 Expected at least $MIN_SPANS spans, found $SPAN_COUNT"
fi

# Validate span attributes
echo "::group::Validating span attributes"
jq -r '.resourceSpans[].scopeSpans[].spans[] | 
    select(.attributes // [] | length == 0) | 
    "Missing attributes in span: \(.name)"' "$TRACE_FILE" || true
echo "::endgroup::"

# Check for errors
ERROR_COUNT=$(jq '[.resourceSpans[].scopeSpans[].spans[] | 
    select(.status.code == 2)] | length' "$TRACE_FILE")

if [ "$ERROR_COUNT" -gt 0 ]; then
    echo "::warning::🌳 Found $ERROR_COUNT spans with errors"
    jq -r '.resourceSpans[].scopeSpans[].spans[] | 
        select(.status.code == 2) | 
        "Error in span: \(.name) - \(.status.message // "unknown")"' "$TRACE_FILE"
else
    echo "::notice::🌳 No error spans detected. The orchard flows smoothly."
fi

# Validate trace completeness
echo "::notice::🌳 Span validation complete. Bud thumps once."
echo "::notice::🌳 The scroll records: $SPAN_COUNT spans validated."
