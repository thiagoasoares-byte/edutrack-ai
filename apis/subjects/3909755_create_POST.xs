// Create a new subject for the authenticated user
query create verb=POST {
  api_group = "subjects"
  auth = "user"

  input {
    // Subject name
    text name filters=trim

    // Optional subject description
    text description? filters=trim

    // Teacher or professor name
    text teacher? filters=trim

    // Academic semester/period (e.g. "2026/1")
    text semester? filters=trim
  }

  stack {
    db.query subjects {
      where  = $db.subjects.user_id == $auth.id && $db.subjects.name == $input.name && $db.subjects.teacher == $input.teacher
      return = {type: "exists"}
    } as $duplicate_exists

    // Subject name and teacher must be unique for the authenticated user
    precondition ($duplicate_exists == false) {
      error_type = "inputerror"
      error      = "Você já possui uma disciplina com este nome e professor"
    }

    db.add subjects {
      data = {
        user_id    : $auth.id
        name       : $input.name
        description: $input.description
        teacher    : $input.teacher
        semester   : $input.semester
      }
    } as $subject
  }

  response = $subject
}
