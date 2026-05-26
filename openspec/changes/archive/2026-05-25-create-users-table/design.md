## Context

A dedicated `user` table is required to support account creation, login, profile updates, and deletion. The `user` ID also acts as the primary authenticator for other APIs in the system.

## Goals / Non-Goals

**Goals:**
- Define the Xano schema for the `user` table.
- Support creation, authentication, update, and deletion of the authenticated user's account.
- Use the `user` ID as the authentication anchor for other APIs.

**Non-Goals:**
- This design does not implement API endpoints.
- This design does not cover frontend login flows.

## Decisions

### Table Schema

The `user` table will use the built-in auth model and include:

```xanoscript
table "user" {
  auth = true

  schema {
    int id {
      description = "Unique user identifier"
    }
    text name filters=trim {
      description = "User's display name"
    }
    email email filters=trim|lower {
      description = "User's email address"
    }
    password password {
      description = "Hashed password"
      sensitive = true
    }
    timestamp created_at?=now {
      description = "Account creation timestamp"
    }
    timestamp updated_at? {
      description = "Last update timestamp"
    }
  }

  index = [
    {type: "primary", field: [{name: "id"}]}
    {type: "btree|unique", field: [{name: "email", op: "asc"}]}
  ]
}
```

### Field Explanations

- `id`: Primary key used for authentication and authorization.
- `name`: User's display name.
- `email`: Unique email address used for login.
- `password`: Secure hashed password.
- `created_at`: Timestamp of account creation.
- `updated_at`: Timestamp of last user data update.

### Ownership and Access

`auth = true` enables the built-in user authentication model. The `user` ID will be the authoritative identifier for access control in downstream APIs.

## Risks / Trade-offs

- **Risk:** Built-in auth assumptions depend on the Xano workspace auth configuration.
  - **Mitigation:** Verify the Xano auth settings and ensure `user` is the expected auth table.
- **Trade-off:** The table uses `auth = true`, which is correct for login flows but means API-level access control must align with Xano auth rules.
