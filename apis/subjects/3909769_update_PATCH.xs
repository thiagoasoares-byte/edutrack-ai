// Update a subject belonging to the authenticated user
query update verb=PATCH {
  api_group = "subjects"
  auth = "user"

  input {
    int  id

    text name?        filters=trim
    text description? filters=trim
    text teacher?     filters=trim
    text semester?    filters=trim
    bool archived?
  }

  stack {
    db.get subjects {
      field_name  = "id"
      field_value = $input.id
    } as $subject

    precondition ($subject != null && $subject.user_id == $auth.id) {
      error_type = "accessdenied"
      error      = "Subject not found or access denied"
    }

    var $payload {
      value = {}
    }

    conditional {
      if (($input.name|strlen) > 0) {
        var.update $payload.name {value = $input.name}
      }
    }

    conditional {
      if (($input.description|strlen) > 0) {
        var.update $payload.description {value = $input.description}
      }
    }

    conditional {
      if (($input.teacher|strlen) > 0) {
        var.update $payload.teacher {value = $input.teacher}
      }
    }

    conditional {
      if (($input.semester|strlen) > 0) {
        var.update $payload.semester {value = $input.semester}
      }
    }

    conditional {
      if ($input.archived != null) {
        var.update $payload.archived {value = $input.archived}
      }
    }

    db.patch subjects {
      field_name  = "id"
      field_value = $input.id
      data        = $payload
    } as $updated_subject
  }

  response = $updated_subject
}
