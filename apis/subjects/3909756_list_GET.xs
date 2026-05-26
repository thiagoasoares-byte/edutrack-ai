// List subjects for the authenticated user, optionally filtering by name
query list verb=GET {
  api_group = "subjects"
  auth = "user"

  input {
    // Partial subject name to search for
    text name? filters=trim
  
    // Page number for pagination
    int page?=1
  
    // Items per page
    int per_page?=20
  }

  stack {
    conditional {
      if (($input.name|strlen) > 0) {
        db.query subjects {
          where = $db.subjects.user_id == $auth.id && $db.subjects.name includes $input.name
          sort = {subjects.created_at: "desc"}
          return = {
            type  : "list"
            paging: {
              page    : $input.page
              per_page: $input.per_page
              totals  : true
            }
          }
        } as $subjects
      }
    
      else {
        db.query subjects {
          where = $db.subjects.user_id == $auth.id
          sort = {subjects.created_at: "desc"}
          return = {
            type  : "list"
            paging: {
              page    : $input.page
              per_page: $input.per_page
              totals  : true
            }
          }
        } as $subjects
      }
    }
  }

  response = $subjects
}