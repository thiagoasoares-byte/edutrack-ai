## 1. Pre-flight Checks

- [x] 1.1 Confirm the `user` table exists in the project and has an `id` primary key.
- [x] 1.2 Confirm the `user` table is the correct reference target for subject ownership.

## 2. Implementation

- [x] 2.1 Create the new table file `tables/subjects.xs`.
- [x] 2.2 Define the Xano schema with `user_id`, `name`, `description`, `teacher`, and `created_at`.
- [x] 2.3 Set `user_id` relation to `user`.
- [x] 2.4 Add appropriate indexes for `id`, `created_at`, and `user_id`.

## 3. Verification

- [x] 3.1 Confirm `tables/subjects.xs` exists and matches the schema in `design.md`.
- [x] 3.2 Confirm the `user_id` relation is correctly defined.
- [x] 3.3 Confirm the subject schema supports ownership and future access control.
