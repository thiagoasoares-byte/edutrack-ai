// List academic tasks for the authenticated user with optional filters
query list verb=GET {
  api_group = "academic_tasks"
  auth = "user"

  input {
    // Filter by subject
    int subject_id?

    // Filter by status: Pendente | Em andamento | Concluída
    text status? filters=trim

    // Pagination
    int page?=1
    int per_page?=50
  }

  stack {
    conditional {
      if (($input.status|strlen) > 0 && $input.subject_id > 0) {
        db.query academic_tasks {
          where = $db.academic_tasks.user_id == $auth.id && $db.academic_tasks.subject_id == $input.subject_id && $db.academic_tasks.status == $input.status
          sort  = {academic_tasks.due_date: "asc"}
          return = {
            type  : "list"
            paging: {page: $input.page, per_page: $input.per_page, totals: true}
          }
        } as $tasks
      }

      elseif (($input.status|strlen) > 0) {
        db.query academic_tasks {
          where = $db.academic_tasks.user_id == $auth.id && $db.academic_tasks.status == $input.status
          sort  = {academic_tasks.due_date: "asc"}
          return = {
            type  : "list"
            paging: {page: $input.page, per_page: $input.per_page, totals: true}
          }
        } as $tasks
      }

      elseif ($input.subject_id > 0) {
        db.query academic_tasks {
          where = $db.academic_tasks.user_id == $auth.id && $db.academic_tasks.subject_id == $input.subject_id
          sort  = {academic_tasks.due_date: "asc"}
          return = {
            type  : "list"
            paging: {page: $input.page, per_page: $input.per_page, totals: true}
          }
        } as $tasks
      }

      else {
        db.query academic_tasks {
          where = $db.academic_tasks.user_id == $auth.id
          sort  = {academic_tasks.due_date: "asc"}
          return = {
            type  : "list"
            paging: {page: $input.page, per_page: $input.per_page, totals: true}
          }
        } as $tasks
      }
    }
  }

  response = $tasks
}
