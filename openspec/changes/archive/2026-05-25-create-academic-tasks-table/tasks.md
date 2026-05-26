## 1. Pre-flight Checks

- [ ] 1.1 Confirm the `subjects` table exists in the project and has a valid `id` primary key.
- [ ] 1.2 Confirm `subjects.id` is the correct target for the relation in `academic_tasks.subject_id`.

## 2. Implementation

- [ ] 2.1 Create the new table file `tables/academic_tasks.xs`.
- [ ] 2.2 Define the Xano schema using the requested fields: `title`, `description`, `due_date`, `status`, and `subject_id`.
- [ ] 2.3 Set `subject_id` relation to `subjects.id`.
- [ ] 2.4 Add indexes for `id`, `due_date`, and `subject_id`.

## 3. Verification

- [ ] 3.1 Confirm `tables/academic_tasks.xs` exists and matches the schema in `design.md`.
- [ ] 3.2 Review the `subject_id` relation to ensure it correctly references `subjects.id`.
