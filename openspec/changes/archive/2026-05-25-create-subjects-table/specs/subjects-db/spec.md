## ADDED Requirements

### Requirement: Store subjects per user
The system SHALL have a table named `subjects` to store academic subject data for each user.

#### Scenario: Create subject with ownership
- **WHEN** a user creates a new subject
- **THEN** the `subjects` table SHALL store the subject with the correct `user_id` association.

### Requirement: Subject ownership must be enforced
Each subject record SHALL reference the owning `user` through `user_id`.

#### Scenario: Query subjects by user
- **WHEN** the system queries subjects for a specific authenticated user
- **THEN** it SHALL return only subjects associated with that user.

### Requirement: Subject schema must include required fields
The `subjects` table SHALL have `name`, `description`, and `teacher` fields.

#### Scenario: Subject record contains all fields
- **WHEN** a subject record is read from the database
- **THEN** it SHALL include `name`, `description`, and `teacher` values.
