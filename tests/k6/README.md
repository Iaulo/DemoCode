# K6 Contract Testing Suite

Comprehensive contract testing suite for the Agent Sandbox API using K6.

## Overview

Contract testing validates that your API adheres to its specification by testing:
- Response status codes
- Response structure (required fields)
- Data types
- Response headers
- Authentication behavior
- Error handling

## Test Files

### 1. k6-contract-health-test.js
Tests the health endpoint contract:
- Status code is 200
- Response contains status, auth, auth_type, header_name fields
- Content-Type is JSON

Run: k6 run tests/k6/k6-contract-health-test.js

### 2. k6-contract-items-test.js
Tests CRUD operations on items:
- GET /api/items - List items
- GET /api/items?q=test - Search items
- POST /api/items - Create item

Run: k6 run tests/k6/k6-contract-items-test.js

### 3. k6-contract-auth-test.js
Tests authentication behavior:
- Valid API key handling
- Invalid API key handling
- Missing API key handling
- Health endpoint accessibility

Run: k6 run tests/k6/k6-contract-auth-test.js

### 4. k6-contract-full-suite.js (Recommended)
Complete end-to-end contract test covering:
- Health endpoint
- Root endpoint
- Full CRUD cycle (Create, Read, Update, Delete)
- Error cases

Run: k6 run tests/k6/k6-contract-full-suite.js

### 5. k6-contract-optional-auth.js
Tests optional authentication scenarios:
- Auth disabled (default)
- Auth enabled (REQUIRE_API_KEY=1)

Run with auth disabled: k6 run tests/k6/k6-contract-optional-auth.js
Run with auth enabled: REQUIRE_API_KEY=1 k6 run tests/k6/k6-contract-optional-auth.js

## Installation

### macOS
brew install k6

### Linux
sudo apt-get install k6

### Windows
choco install k6

### Docker
docker run -i -v $PWD:/scripts grafana/k6 run /scripts/tests/k6/k6-contract-full-suite.js

## Running Tests

### Basic Run
k6 run tests/k6/k6-contract-full-suite.js

### With Custom Configuration
k6 run -u 5 -d 30s tests/k6/k6-contract-full-suite.js
(-u: number of virtual users, -d: test duration)

### With Environment Variables
REQUIRE_API_KEY=1 k6 run tests/k6/k6-contract-optional-auth.js

### Output to JSON
k6 run --out json=results.json tests/k6/k6-contract-full-suite.js

## Prerequisites

1. Backend Running:
cd backend
python -m uvicorn app.main:app --reload

2. Base URL: Tests expect the API at http://localhost:8000
Modify BASE_URL constant if different

## Contract Assertions

All tests include assertions for:
✅ HTTP Status Codes
✅ Response Structure (required fields)
✅ Data Types
✅ Field Values
✅ Content-Type Headers
✅ Authentication Behavior
✅ Error Messages

## CI/CD Integration

GitHub Actions Example:
name: K6 Contract Tests
on: [push, pull_request]
jobs:
  k6:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - uses: grafana/k6-action@v0.3.0
        with:
          filename: tests/k6/k6-contract-full-suite.js
          cloud: false

## Troubleshooting

### Connection refused error
Cause: Backend not running
Solution: Start backend server:
cd backend && python -m uvicorn app.main:app --reload

### 401 Unauthorized errors
Cause: REQUIRE_API_KEY=1 is set
Solution: Either disable it or provide valid key:
export REQUIRE_API_KEY=0
k6 run tests/k6/k6-contract-full-suite.js

### Failed to resolve host
Cause: Incorrect BASE_URL
Solution: Update BASE_URL in test file to match your setup

## Resources

- K6 Documentation: https://k6.io/docs/
- Contract Testing Guide: https://k6.io/docs/testing-guides/api-contract-testing/
- K6 Best Practices: https://k6.io/docs/best-practices/