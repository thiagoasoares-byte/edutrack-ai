## ADDED Requirements

### Requirement: Store academic task records
The system SHALL have a table named `academic_tasks` to store tasks linked to academic subjects.

#### Scenario: Create a new academic task
- **WHEN** a student creates a new academic task with a title, due_date, status, and subject_id
- **THEN** the `academic_tasks` table SHALL contain a new row with the provided values and `created_at` set automatically.

### Requirement: Academic tasks must reference a subject
Each `academic_tasks` record SHALL reference an existing `subjects` record through `subject_id`.

#### Scenario: Create a task with a valid subject
- **WHEN** a task is created with a `subject_id` that exists in `subjects`
- **THEN** the task SHALL be accepted.

#### Scenario: Create a task with an invalid subject
- **WHEN** a task is created with a `subject_id` that does not exist in `subjects`
- **THEN** the system SHALL reject the task.

### Requirement: Task fields are required and typed
The `academic_tasks` table SHALL include `title` (text), `description` (text), `due_date` (date), `status` (text), and `subject_id` (int).

#### Scenario: Task record contains all requested fields
- **WHEN** a task record is read from the database
- **THEN** it SHALL include `title`, `description`, `due_date`, `status`, and `subject_id` fields.
