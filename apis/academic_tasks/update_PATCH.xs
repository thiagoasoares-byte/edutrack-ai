// Update an academic task (title, description, due_date, status, priority, subject_id)
query update verb=PATCH {
  api_group = "academic_tasks"
  auth = "user"

  input {
    int  id

    text      title?      filters=trim
    text      description? filters=trim
    timestamp due_date?
    text      status?     filters=trim
    text      priority?   filters=trim
    int       subject_id?
  }

  stack {
    db.get academic_tasks {
      field_name  = "id"
      field_value = $input.id
    } as $task

    precondition ($task != null && $task.user_id == $auth.id) {
      error_type = "accessdenied"
      error      = "Task not found or access denied"
    }

    var $payload {
      value = {}
    }

    conditional {
      if (($input.title|strlen) > 0) {
        var.update $payload.title {value = $input.title}
      }
    }

    conditional {
      if (($input.description|strlen) > 0) {
        var.update $payload.description {value = $input.description}
      }
    }

    conditional {
      if ($input.due_date != null) {
        var.update $payload.due_date {value = $input.due_date}
      }
    }

    conditional {
      if (($input.status|strlen) > 0) {
        var.update $payload.status {value = $input.status}
      }
    }

    conditional {
      if (($input.priority|strlen) > 0) {
        var.update $payload.priority {value = $input.priority}
      }
    }

    conditional {
      if ($input.subject_id > 0) {
        // Verify new subject also belongs to the user
        db.get subjects {
          field_name  = "id"
          field_value = $input.subject_id
        } as $new_subject

        precondition ($new_subject != null && $new_subject.user_id == $auth.id) {
          error_type = "accessdenied"
          error      = "Subject not found or access denied"
        }

        var.update $payload.subject_id {value = $input.subject_id}
      }
    }

    db.patch academic_tasks {
      field_name  = "id"
      field_value = $input.id
      data        = $payload
    } as $updated_task
  }

  response = $updated_task
}
