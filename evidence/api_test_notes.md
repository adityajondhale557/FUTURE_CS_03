W# API Security Assessment Notes

## Target API

Local target: http://127.0.0.1:8888
Lab: OWASP crAPI
Authorization: Authorized local testing environment

Observed:
- POST /verify returned HTTP 200 and a valid JWT message.
- The JWT access token is stored in browser Local Storage.
- The /verify request sends a token in its request body.
- The community API request uses an Authorization: Bearer header.
- The chat_session_id cookie has HttpOnly and Secure enabled.


## Authentication

- The authenticated community request returned HTTP 200.
- After disabling the Authorization header in the test request, the endpoint returned HTTP 401 Unauthorized.
- Conclusion: authentication is enforced for this endpoint in the tested scenario.

## Authorization

- The authenticated community API request returned HTTP 200.
- When the Authorization header was disabled, the same endpoint returned HTTP 401 Unauthorized.
- Assessment: Authentication is enforced for this endpoint in the tested scenario.

## Token / Key Handling

- The JWT access token was observed in browser Local Storage under the application's origin.
- Risk: If an attacker exploits XSS in the same origin, JavaScript may be able to read the token and potentially impersonate the user.
- Recommendation: Prefer secure, short-lived token handling; implement XSS protections and a strong Content Security Policy (CSP). Evaluate an HttpOnly cookie-based design where appropriate.
- Assessment: Potential risk identified; no XSS vulnerability was demonstrated during this assessment.

## Rate Limiting

- Five unauthenticated requests to the local community endpoint returned HTTP 401.
- Response headers did not include visible RateLimit-Limit, RateLimit-Remaining, or Retry-After headers.
- Conclusion: Rate limiting remains unverified; authenticated testing is needed before reporting a potential weakness.

## Input Validation

- `limit=abc` returned HTTP 200 and the response still contained three posts.
- `limit=1000` returned HTTP 200; the response reported `total: 3`.
- `limit=0` returned HTTP 200; the response reported `total: 3`.
- `offset=-1` returned a validation error: skip value must be non-negative.
- `offset=9999` returned an empty posts array with `total: 0`.
- Assessment: Input validation is inconsistent for the `limit` parameter. Further testing is needed to determine whether invalid values are normalized or ignored.

## Data Exposure

- GET /community/api/v2/community/posts/recent?limit=30&offset=0 returned HTTP 200.
- Response contained community post title/content and author fields including nickname, email, vehicleid, profile_pic_url, and authorid.
- Potential issue: author email and vehicle ID may be exposed unnecessarily in public community responses.
- Status: Needs validation; confirm whether these fields are intended to be public before assigning severity.

## Findings

### Finding 1: Potential Excessive Data Exposure
- Endpoint: GET /community/api/v2/community/posts/recent
- Evidence: The response included author email and vehicle ID alongside community post data.
- Risk: Personal or vehicle-related information may be disclosed beyond what is necessary for the feature.
- Severity: Tentative Medium; confirm intended visibility and authorization requirements before final rating.
- Recommendation: Return only necessary public author fields and enforce appropriate data-access rules.

### Finding 2: JWT Stored in Local Storage
- Evidence: The browser's Local Storage contained the JWT access token.
- Risk: An XSS vulnerability in the same origin could allow JavaScript to access the token.
- Severity: Informational observation; no XSS was demonstrated.
- Recommendation: Apply strong XSS defenses, use a restrictive Content Security Policy, and review token storage and expiration.

### Finding 3: Pagination Input Handling
- Evidence: limit=abc, limit=0, and limit=1000 returned HTTP 200; offset=-1 produced a non-negative skip validation error.
- Risk: Invalid or excessive pagination inputs may be handled inconsistently.
- Severity: Low / unconfirmed; impact has not been demonstrated.
- Recommendation: Validate pagination values, require positive integer limits, and enforce a reasonable maximum.

## Recommendations

1. Data minimization: Return only author information required by the community feature. Confirm whether email and vehicle ID should be visible to other users.
2. Authentication and tokens: Keep authentication enforcement consistent, protect JWTs from client-side script access, and review token expiration and revocation.
3. Input validation: Require integer pagination parameters, enforce a positive limit and a reasonable maximum, and return consistent validation errors.
4. Rate limiting: Test authenticated requests with a controlled request rate and document the actual results before concluding whether rate limiting is missing.
5. Security monitoring: Log authentication failures and suspicious API usage without recording access tokens or other secrets.
6. Retesting: Repeat the relevant checks after remediation and retain sanitized request/response evidence.

## Lab Status

- OWASP crAPI was restarted successfully after the virtual machine session ended.
- All 10 listed containers are running.
- The listed services report healthy status.
- Testing target: http://127.0.0.1:8888
- Testing is restricted to the local, intentionally vulnerable lab.

