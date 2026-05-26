// Authenticate a user and return an auth token
query login verb=POST {
  api_group = "auth"

  input {
    // User email address
    email email filters=trim|lower
  
    // User password
    password password {
      sensitive = true
    }
  }

  stack {
    db.get user {
      field_name = "email"
      field_value = $input.email
    } as $user
  
    // User must exist to log in
    precondition ($user != null) {
      error_type = "inputerror"
      error = "Invalid email or password"
    }
  
    security.check_password {
      text_password = $input.password
      hash_password = $user.password
    } as $is_password_valid
  
    // Password must match the stored hash
    precondition ($is_password_valid) {
      error_type = "inputerror"
      error = "Invalid email or password"
    }
  
    security.create_auth_token {
      table = "user"
      extras = {}
      expiration = 86400
      id = $user.id
    } as $auth_token
  }

  response = {
    user      : {id: $user.id, name: $user.name, email: $user.email}
    auth_token: $auth_token
  }
}