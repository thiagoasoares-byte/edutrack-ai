## ADDED Requirements

### Requirement: The system must store subject data
The system SHALL have a table named `subjects` to store academic subject information.

#### Scenario: A new subject is created
- **WHEN** a new subject record is created with a name and user_id
- **THEN** the `subjects` table SHALL contain a new row with the provided `name` and `user_id`, and `created_at` is automatically populated.

### Requirement: Subjects must be owned by a user
Each subject record SHALL be associated with a single user.

#### Scenario: A subject is created without a user
- **WHEN** an attempt is made to create a subject record without a `user_id`
- **THEN** the system SHALL reject the record.

#### Scenario: Querying subjects for a user
- **WHEN** the system is queried for subjects with a specific `user_id`
- **THEN** it SHALL return all subjects associated with that `user_id`.

### Requirement: Subject name is mandatory
The `name` field for a subject SHALL NOT be null or empty.

#### Scenario: Create a subject with no name
- **WHEN** an attempt is made to create a subject with a null or empty `name`
- **THEN** the system SHALL reject the record.
