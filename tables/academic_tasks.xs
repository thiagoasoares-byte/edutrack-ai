table academic_tasks {
  schema {
    int id
    timestamp created_at?=now
    text title
    text description?
    date due_date
    text status?="pending"
    int subject_id {
      relation = "subjects.id"
    }
    int user_id {
      relation = "user.id"
    }
  }

  index = [
    { type: "primary", field: [{ name: "id" }] }
    { type: "btree", field: [{ name: "user_id" }] }
    { type: "btree", field: [{ name: "subject_id" }] }
  ]
}