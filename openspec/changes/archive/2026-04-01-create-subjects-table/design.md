## Context

Based on the `proposal.md`, the platform needs a way to store and manage academic subjects for each user. This involves creating a new table in the existing Xano database.

## Goals / Non-Goals

**Goals:**
- Define the schema for the `subjects` table in a Xano-compatible format.
- The table must include a field to link to the `user` table, establishing ownership.

**Non-Goals:**
- This design does not cover the API endpoints to interact with the table.
- This design does not cover any UI for managing subjects.

## Decisions

### Table Schema

The `subjects` table will be defined with the following schema.

```xanoscript
table subjects {
  auth = false

  schema {
    int id
    timestamp created_at?=now {
      visibility = "private"
    }
    text name
    int user_id {
      relation = "user.id"
    }
    text description
    text teacher
  }

  index = [
    {type: "primary", field: [{name: "id"}]}
    {type: "btree", field: [{name: "created_at", op: "desc"}]}
    {type: "btree", field: [{name: "user_id"}]}
  ]
}
```

### Field Explanations

- **id**: Primary key (integer).
- **created_at**: Timestamp, automatically set on creation.
- **name**: The name of the subject (e.g., "Calculus I"). This field will be required.
- **user_id**: An integer that links to the `user` table's `id` field to establish ownership.
- **description**: An optional text field for a longer description of the subject.
- **teacher**: An optional text field for the teacher or instructor's name.

### Indexing

An index will be created on the `user_id` field to ensure efficient querying of subjects belonging to a specific user.

## Risks / Trade-offs

- **Risk**: The user table might not be named `user` or its primary key might not be `id`.
  - **Mitigation**: The implementation tasks will include a verification step to confirm the correct user table name and its primary key before creating the `subjects` table.
- **Trade-off**: `auth = false` is set on the table, which means the API layer is fully responsible for enforcing access control. This is a standard and acceptable pattern.
