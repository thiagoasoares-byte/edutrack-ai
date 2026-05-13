query "subjects" verb=GET {
  api_group = "edutrack"
  description = "Returns a list of subjects belonging to the authenticated user"
  auth = "user"

  input {
  }

  stack {
    db.query subjects {
      where = $db.subjects.user_id == $auth.id
    } as $user_subjects
  }

  response = $user_subjects
}