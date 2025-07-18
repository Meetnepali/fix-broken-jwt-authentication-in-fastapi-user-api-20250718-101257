Task Overview
A FastAPI-based user management API has implemented JWT-based authentication with role enforcement on specific endpoints. After a recent configuration update, all protected endpoints now return HTTP 401 Unauthorized errors—valid tokens are always rejected. Your task is to diagnose and fix the JWT authentication system so that authorized users can access protected endpoints, and role-based access control is correctly enforced.

Guidance
- Review the application's authentication logic, especially how JWT tokens are issued and validated
- Inspect recent configuration values and handling of secrets and algorithms
- Ensure role checks are enforced after successful JWT authentication
- Verify that valid JWT tokens, when presented by users with correct roles, are accepted and allow access
- No new dependencies should be added; the solution must work with the existing stack

Objectives
- Diagnose why valid JWT tokens are being rejected with HTTP 401
- Implement the required fix so that JWT authentication works as intended
- Ensure endpoints only allow access to users with valid, unexpired JWTs
- Validate that role-based restrictions are properly enforced on limited endpoints

How to Verify
- Use the API to obtain a JWT token as a registered user
- Access protected endpoints with a valid token and confirm successful responses
- Ensure endpoints return 401 for invalid or expired tokens, and 403 for insufficient roles
- Confirm all authentication and role enforcement tests pass and the API operates securely
