## Context

The application needs a structured way for students to register and manage academic obligations such as lessons, exams, and assignments. These tasks must be linked to an existing `subjects` record so each obligation belongs to a specific discipline.

## Goals / Non-Goals

**Goals:**
- Define the Xano schema for the new `academic_tasks` table.
- Store the requested fields: `title`, `description`, `due_date`, `status`, and `subject_id`.
- Ensure `subject_id` references the existing `subjects` table.

**Non-Goals:**
- This design does not implement API endpoints for task CRUD.
- This design does not cover UI or frontend behavior.

## Decisions

### Table Schema

The `academic_tasks` table will be defined as follows:

```xanoscript
table academic_tasks {
  auth = false

  schema {
    int id
    timestamp created_at?=now {
      visibility = "private"
    }
    text title
    text description
    date due_date
    text status
    int subject_id {
      relation = "subjects.id"
    }
  }

  index = [
    {type: "primary", field: [{name: "id"}]}
    {type: "btree", field: [{name: "due_date", op: "asc"}]}
    {type: "btree", field: [{name: "subject_id"}]}
  ]
}
```

### Field Explanations

- `id`: Primary key for each academic task.
- `created_at`: Timestamp set automatically on creation and kept private.
- `title`: Task title, e.g. "Read chapter 4".
- `description`: Detailed task description.
- `due_date`: Due date for the obligation.
- `status`: Current task status, e.g. "pending", "completed", "in progress".
- `subject_id`: Link to the owning subject in `subjects.id`.

### Ownership and Access

Ownership will be inferred through `subject_id` and the subject's `user_id`. API-level logic should ensure that users can only access tasks belonging to subjects they own.

## Risks / Trade-offs

- **Risk:** The `subjects` table may have a different primary key or relationship pattern than expected.
  - **Mitigation:** Verify `subjects.id` exists and is the correct relational target before implementation.
- **Trade-off:** Not adding `user_id` directly to `academic_tasks` keeps the schema aligned with the requested fields, but requires API logic to enforce ownership through the related `subject`.
