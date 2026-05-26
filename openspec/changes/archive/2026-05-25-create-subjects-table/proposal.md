# Create Subjects Database Proposal

## Why

Students need a dedicated structure for registering and managing academic subjects. A `subjects` table with ownership metadata enables access control and supports future automations around user-specific discipline data.

## What Changes

- Add `tables/subjects.xs` with the subject schema.
- Define `user_id` as a relation to the existing `user` table.
- Include fields `name`, `description`, `teacher`, and `created_at`.
- Add indexes for efficient queries by `created_at` and `user_id`.

## Impact

- Enables secure subject ownership per authenticated user.
- Provides a foundation for subject CRUD APIs and subsequent automations.
- Keeps authorization enforcement in the API layer while preserving clean schema design.
