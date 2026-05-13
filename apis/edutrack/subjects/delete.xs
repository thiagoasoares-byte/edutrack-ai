query "subjects/{subjects_id}" verb=DELETE {
  api_group = "edutrack"
  description = "Deletes a specific subject if it belongs to the authenticated user"
  auth = "user"

  input {
    int subjects_id {
      description = "ID of the subject to delete"
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

    // Delete the subject
    db.delete subjects {
      description = "Delete subject record"
      where = $db.subjects.id == $input.subjects_id
    }
  }

  response = null
}