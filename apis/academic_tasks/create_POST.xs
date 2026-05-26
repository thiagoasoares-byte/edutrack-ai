// Create a new academic task for the authenticated user
query create verb=POST {
  api_group = "academic_tasks"
  auth = "user"

  input {
    // Task title
    text title filters=trim

    // Optional description
    text description? filters=trim

    // Due date (ISO 8601)
    timestamp due_date

    // Task status: Pendente | Em andamento | Concluída
    text status?="Pendente"

    // Priority: Baixa | Média | Alta
    text priority?="Média"

    // Linked subject
    int subject_id
  }

  stack {
    // Verify the subject belongs to the authenticated user
    db.get subjects {
      field_name  = "id"
      field_value = $input.subject_id
    } as $subject

    precondition ($subject != null && $subject.user_id == $auth.id) {
      error_type = "accessdenied"
      error      = "Subject not found or access denied"
    }

    db.add academic_tasks {
      data = {
        user_id    : $auth.id
        subject_id : $input.subject_id
        title      : $input.title
        description: $input.description
        due_date   : $input.due_date
        status     : $input.status
        priority   : $input.priority
      }
    } as $task
  }

  response = $task
}
