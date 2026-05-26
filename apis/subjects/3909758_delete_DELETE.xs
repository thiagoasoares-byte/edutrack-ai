// Delete a subject owned by the authenticated user
query delete verb=DELETE {
  api_group = "subjects"
  auth = "user"

  input {
    // Subject ID
    int id
  }

  stack {
    db.get subjects {
      field_name = "id"
      field_value = $input.id
    } as $subject
  
    // Subject must exist and belong to the authenticated user
    precondition ($subject != null && $subject.user_id == $auth.id) {
      error_type = "accessdenied"
      error = "Subject not found or access denied"
    }
  
    db.del subjects {
      field_name = "id"
      field_value = $input.id
    }
  }

  response = {success: true}
}