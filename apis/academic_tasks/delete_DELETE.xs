// Delete an academic task owned by the authenticated user
query delete verb=DELETE {
  api_group = "academic_tasks"
  auth = "user"

  input {
    int id
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

    db.del academic_tasks {
      field_name  = "id"
      field_value = $input.id
    }
  }

  response = {success: true}
}
