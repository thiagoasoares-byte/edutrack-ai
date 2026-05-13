query "subjects/{subjects_id}" verb=GET {
  api_group = "edutrack"
  description = "Returns a specific subject if it belongs to the authenticated user"
  auth = "user"

  input {
    int subjects_id {
      description = "ID of the subject to retrieve"
    }
  }

  stack {
    db.query subjects {
      where = ($db.subjects.id == $input.subjects_id) && ($db.subjects.user_id == $auth.id)
      return = {
        type: "single"
      }
    } as $subject

    conditional {
      if ($subject == null) {
        throw {
          name = "NotFoundError"
          value = "Subject not found or access denied"
        }
      }
    }
  }

  response = $subject
}