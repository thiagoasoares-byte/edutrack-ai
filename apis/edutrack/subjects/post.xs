query "subjects" verb=POST {
  api_group = "edutrack"
  description = "Creates a new subject for the authenticated user"
  auth = "user"

  input {
    text name {
      description = "Name of the subject"
    }
    text description? {
      description = "Optional description of the subject"
    }
    text teacher? {
      description = "Optional teacher name"
    }
  }

  stack {
    db.add subjects {
      description = "Create a new subject for the authenticated user"
      data = {
        name        : $input.name
        description : $input.description
        teacher     : $input.teacher
        user_id     : $auth.id
      }
    } as $new_subject
  }

  response = $new_subject
}