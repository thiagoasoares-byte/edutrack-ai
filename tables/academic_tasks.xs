table academic_tasks {
  auth = false

  schema {
    int id
    timestamp created_at?=now {
      visibility = "private"
    }
  
    timestamp deleted_at? {
      visibility = "private"
    }
  
    text title
    text description?
    date due_date
    text status?=pending
    int subject_id
    int user_id
  }

  index = [
    {type: "primary", field: [{name: "id"}]}
    {type: "btree", field: [{name: "user_id"}]}
    {type: "btree", field: [{name: "subject_id"}]}
  ]
}