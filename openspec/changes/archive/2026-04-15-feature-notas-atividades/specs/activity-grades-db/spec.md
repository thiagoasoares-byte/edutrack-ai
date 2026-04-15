# activity-grades Specification

## Purpose

This specification defines the database structure for storing student grades on academic activities. It ensures that each grade is linked to a specific activity, a student, and the teacher who assigned it.

## ADDED Requirements

### Requirement: Store Activity Grades
The system SHALL provide a mechanism to store grades for students on specific academic tasks.

#### Scenario: A teacher assigns a grade to a student
- **WHEN** a teacher submits a grade for a student on an academic task
- **THEN** the system SHALL save a record containing the academic task's ID, the student's ID, the teacher's ID, and the assigned grade.
