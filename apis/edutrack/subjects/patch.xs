query "subjects/{subjects_id}" verb=PATCH {
  api_group = "edutrack"
  description = "Updates a specific subject if it belongs to the authenticated user"
  auth = "user"

  input {
    int subjects_id {
      description = "ID of the subject to update"
    }
    text name? {
      description = "Updated name of the subject"
    }
    text description? {
      description = "Updated description of the subject"
    }
    text teacher? {
      description = "Updated teacher name"
    }
  }

  stack {
    // First check if subject exists and belongs to user
    db.query subjects {
      where = ($db.subjects.id == $input.subjects_id) && ($db.subjects.user_id == $auth.id)
      return = {
        type: "single"
      }
    } as $existing_subject

    conditional {
      if ($existing_subject == null) {
        throw {
          name = "NotFoundError"
          value = "Subject not found or access denied"
        }
      }
    }

    // Update the subject
    db.update subjects {
      description = "Update subject data"
      where = $db.subjects.id == $input.subjects_id
      data = {
        name        : $input.name
        description : $input.description
        teacher     : $input.teacher
      }
    } as $updated_subject
  }

  response = $updated_subject
}