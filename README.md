# FUTURE_CS_03 — API Security Risk Analysis

## Project Overview

This project documents an API security assessment conducted as part of the Future Interns Cyber Security Internship (Task 3).

The assessment uses OWASP crAPI, an intentionally vulnerable API training application, running locally in a controlled lab environment.

## Objectives

- Assess API authentication and authorization behavior.
- Review JWT token storage and handling.
- Examine API input validation and pagination.
- Identify potential excessive data exposure.
- Recommend security improvements.

## Tools Used

- OWASP crAPI
- Firefox Developer Tools
- Kali Linux
- Docker Compose
- Python ReportLab

## Key Observations

| ID | Observation | Preliminary Assessment |
|---|---|---|
| F-01 | Community API returned author metadata, including email and vehicle ID | Potential data exposure; needs validation |
| F-02 | JWT access token stored in Local Storage | Informational; no XSS demonstrated |
| F-03 | Pagination parameters were handled inconsistently | Low / unconfirmed; impact not demonstrated |

Authentication was enforced in the tested community API scenario: the authenticated request returned HTTP 200, while the same request without its Authorization header returned HTTP 401.

Rate limiting was not conclusively assessed.

## Deliverables

- [PDF Assessment Report](report/FUTURE_CS_03_API_Security_Risk_Analysis.pdf)
- [Report Source](report/report_content.md)
- [Findings Summary](analysis/findings_summary.md)
- [Testing Notes](evidence/api_test_notes.md)

## Recommendations

1. Minimize author information returned by community endpoints.
2. Review token storage and strengthen XSS protections.
3. Validate pagination parameters and enforce reasonable limits.
4. Conduct controlled authenticated rate-limit testing.
5. Retest findings before assigning final severity ratings.

## Scope and Disclaimer

All testing was performed against a local OWASP crAPI training environment. Findings are preliminary and should be validated before being treated as confirmed vulnerabilities. No production systems were targeted.

## Internship

**Program:** Future Interns — Cyber Security  
**Task:** FUTURE_CS_03 — API Security Risk Analysis
