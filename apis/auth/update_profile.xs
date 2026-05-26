// Update the authenticated user's profile
query update_profile verb=PATCH {
  api_group = "auth"
  auth = "user"

  input {
    // Updated full name
    text name? filters=trim
  
    // Updated email address
    email email? filters=trim|lower
  
    // Updated password
    password password? {
      sensitive = true
    }
  }

  stack {
    db.get user {
      field_name = "id"
      field_value = $auth.id
    } as $current_user
  
    conditional {
      if (($input.email|strlen) > 0 && $input.email != $current_user.email) {
        db.get user {
          field_name = "email"
          field_value = $input.email
        } as $existing_user
      
        // Prevent email duplication
        precondition ($existing_user == null) {
          error_type = "inputerror"
          error = "Email already in use"
        }
      }
    }
  
    var $payload {
      value = {}
    }
  
    conditional {
      if (($input.name|strlen) > 0) {
        var.update $payload.name {
          value = $input.name
        }
      }
    }
  
    conditional {
      if (($input.email|strlen) > 0) {
        var.update $payload.email {
          value = $input.email
        }
      }
    }
  
    conditional {
      if (($input.password|strlen) > 0) {
        var.update $payload.password {
          value = $input.password
        }
      }
    }
  
    db.patch user {
      field_name = "id"
      field_value = $auth.id
      data = $payload
    } as $updated_user
  }

  response = {user: $updated_user}
}