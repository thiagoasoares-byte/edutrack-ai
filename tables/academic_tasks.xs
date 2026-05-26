// Stores academic tasks (assignments, exams, etc.) linked to a subject and user
table academic_tasks {
  auth = false

  schema {
    int id
    timestamp created_at?=now {
      visibility = "private"
    }
  
    timestamp updated_at? {
      visibility = "private"
    }
  
    // Direct owner reference for efficient queries
    int user_id {
      table = ""
    }
  
    // Subject this task belongs to
    int subject_id {
      table = ""
    }
  
    // Short task title
    text title filters=trim
  
    // Optional detailed description
    text description? filters=trim
  
    // Deadline for the task
    date due_date?
  
    // Pendente | Em andamento | Concluída
    text status?=Pendente
  
    // Baixa | Média | Alta
    text priority?="Média"
  }

  index = [
    {type: "primary", field: [{name: "id"}]}
    {type: "btree", field: [{name: "user_id"}]}
    {type: "btree", field: [{name: "subject_id"}]}
    {type: "btree", field: [{name: "due_date", op: "asc"}]}
    {type: "btree", field: [{name: "status"}]}
  ]
}