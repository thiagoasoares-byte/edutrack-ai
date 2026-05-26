## Why

The platform currently lacks a dedicated system for users to manage their academic subjects. This change introduces that capability, which is foundational for tracking academic progress and enabling future features.

## What Changes

- A new database table named `subjects` will be created.
- This table will store subject information, including a link to the user who owns it.
- This enables CRUD (Create, Read, Update, Delete) operations for subjects, associated with a specific user.

## Capabilities

### New Capabilities
- `subjects-db`: Manages the schema and storage for academic subjects.

### Modified Capabilities
- None

## Impact

- A new table will be added to the database.
- New API endpoints will be needed to manage subjects.
