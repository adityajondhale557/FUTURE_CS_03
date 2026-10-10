# Findings Summary — FUTURE_CS_03

## Assessment Environment
- Target: OWASP crAPI running locally
- URL: http://127.0.0.1:8888
- Testing method: Firefox DevTools and controlled HTTP requests

## Findings

| ID | Finding | Preliminary Severity | Status |
|---|---|---|---|
| F-01 | Potential excessive author data exposure | Tentative Medium | Needs validation |
| F-02 | JWT stored in browser Local Storage | Informational observation | No XSS demonstrated |
| F-03 | Inconsistent pagination parameter handling | Low / unconfirmed | Impact not demonstrated |

## Authentication
- Authenticated community request: HTTP 200.
- Same request without the Authorization header: HTTP 401.
- Authentication was enforced in the tested scenario.

## Rate Limiting
- Five unauthenticated requests returned HTTP 401.
- No explicit rate-limit headers were observed in the inspected response.
- Rate limiting remains unverified.

## Key Recommendations
1. Minimize public author metadata.
2. Review token storage and strengthen XSS protections.
3. Validate pagination values and enforce reasonable limits.
4. Conduct controlled authenticated rate-limit testing.
5. Retest findings after remediation.

## Limitations
This was a limited assessment of a local training application. Findings are preliminary and require validation before final severity assignments.
