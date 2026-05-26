## ADDED Requirements

### Requirement: Store application users
The system SHALL have a table named `user` to store account data.

#### Scenario: User account is created
- **WHEN** a new user signs up with a name, email, and password
- **THEN** the `user` table SHALL contain a new record with those values and `created_at` populated.

### Requirement: Support user authentication
The `user` table SHALL support login via email and password.

#### Scenario: User logs in
- **WHEN** a user provides valid credentials
- **THEN** the system SHALL authenticate the user and associate requests with their `user` id.

### Requirement: User data must be updatable and deletable by owner
Each user SHALL be able to update or delete their own record.

#### Scenario: User updates profile
- **WHEN** the authenticated user updates profile fields
- **THEN** the `user` record SHALL reflect the changes in the database.

#### Scenario: User deletes account
- **WHEN** the authenticated user deletes their account
- **THEN** the system SHALL remove the corresponding `user` record.
