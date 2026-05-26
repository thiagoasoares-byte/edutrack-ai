// Stores academic subjects (disciplines) linked to an authenticated user
table subjects {
  auth = false

  schema {
    int id
    timestamp created_at?=now {
      visibility = "private"
    }
  
    timestamp updated_at? {
      visibility = "private"
    }
  
    // Owner of this subject
    int user_id {
      table = ""
    }
  
    // Discipline name
    text name filters=trim
  
    // Optional description
    text description? filters=trim
  
    // Professor / instructor name
    text teacher? filters=trim
  
    // Academic period, e.g. 2026/1
    text semester? filters=trim
  
    // Soft-archive without deleting
    bool archived?
  }

  index = [
    {type: "primary", field: [{name: "id"}]}
    {type: "btree", field: [{name: "user_id"}]}
    {type: "btree", field: [{name: "created_at", op: "desc"}]}
    {type: "btree", field: [{name: "name", op: "asc"}]}
  ]
}