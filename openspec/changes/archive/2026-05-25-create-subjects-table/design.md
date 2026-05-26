## Context

The application needs a reliable database structure for academic subjects so each user can register and manage their own disciplines. This table will support ownership, access control, and future automations tied to subject data.

## Goals / Non-Goals

**Goals:**
- Define the Xano schema for a `subjects` table.
- Ensure each subject belongs to a single authenticated user via `user_id`.
- Include fields for `name`, `description`, `teacher`, and timestamps.

**Non-Goals:**
- This design does not implement API endpoints for subjects.
- This design does not cover frontend interfaces or user interactions.

## Decisions

### Table Schema

The `subjects` table will use the following schema:

```xanoscript
table subjects {
  auth = false

  schema {
    int id
    timestamp created_at?=now {
      visibility = "private"
    }
    int user_id {
      table = "user"
    }
    text name filters=trim
    text description? filters=trim
    text teacher? filters=trim
  }

  index = [
    {type: "primary", field: [{name: "id"}]}
    {type: "btree", field: [{name: "created_at", op: "desc"}]}
    {type: "btree", field: [{name: "user_id"}]}
  ]
}
```

### Field Explanations

- `id`: Primary key for the subject record.
- `created_at`: Auto-populated timestamp on creation, private visibility.
- `user_id`: Foreign key linking the subject to the authenticated `user`.
- `name`: Discipline name, required and trimmed.
- `description`: Optional text description.
- `teacher`: Optional instructor name.

### Ownership and Access

Subject ownership is enforced by the `user_id` relation. API logic should only allow subject CRUD operations for the authenticated owner.

## Risks / Trade-offs

- **Risk:** The `user` table name or primary-key type may differ from expectations.
  - **Mitigation:** Confirm `user` exists and supports `id` before finalizing the schema.
- **Trade-off:** Setting `auth = false` means access control is handled in the API layer, which is acceptable for this project.
