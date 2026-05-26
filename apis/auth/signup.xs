// Register a new user and return an auth token
query signup verb=POST {
  api_group = "auth"

  input {
    // Full name of the user
    text name filters=trim
  
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
    } as $existing_user
  
    // Prevent duplicate signup with the same email
    precondition ($existing_user == null) {
      error_type = "inputerror"
      error = "Email already registered"
    }
  
    db.add user {
      data = {
        name    : $input.name
        email   : $input.email
        password: $input.password
      }
    } as $new_user
  
    security.create_auth_token {
      table = "user"
      extras = {}
      expiration = 86400
      id = $new_user.id
    } as $auth_token
  }

  response = {
    user      : {id: $new_user.id, name: $new_user.name, email: $new_user.email}
    auth_token: $auth_token
  }
}