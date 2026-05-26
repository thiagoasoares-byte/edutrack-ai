// Auth table — stores user accounts and credentials
table user {
  auth = true

  schema {
    // Unique user identifier
    int id
  
    // Account creation timestamp
    timestamp created_at?=now {
      visibility = "private"
    }
  
    // Last update timestamp
    timestamp updated_at? {
      visibility = "private"
    }
  
    // User's display name
    text name filters=trim
  
    // User's unique email address
    email email filters=trim|lower
  
    // Hashed password
    password password {
      sensitive = true
    }
  }

  index = [
    {type: "primary", field: [{name: "id"}]}
    {type: "btree|unique", field: [{name: "email", op: "asc"}]}
  ]
}