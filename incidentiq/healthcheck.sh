#!/bin/bash

BASE_URL="${1:-http://localhost:8000}"

echo "Checking IncidentIQ health at $BASE_URL..."

check() {
  local label=$1
  local url=$2
  local status
  status=$(curl -s -o /dev/null -w "%{http_code}" "$url")
  if [ "$status" = "200" ]; then
    echo "  ✓ $label ($status)"
  else
    echo "  ✗ $label ($status)"
    exit 1
  fi
}

check "Health endpoint"   "$BASE_URL/health"
check "Incidents list"    "$BASE_URL/incidents"
check "Monitor payment"   "$BASE_URL/monitor/payment-api"

echo "All checks passed."
