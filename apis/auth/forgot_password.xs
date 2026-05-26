// Send a password-reset magic link to the user's email
query forgot_password verb=POST {
  api_group = "auth"

  input {
    email email filters=trim|lower
  }

  stack {
    db.get user {
      field_name  = "email"
      field_value = $input.email
    } as $user

    // Return success even if email not found to avoid user enumeration
    conditional {
      if ($user != null) {
        function.run "Quick Start/generate_magic_link" {
          input = { email: $input.email }
        } as $magic_link

        util.send_email {
          service_provider = "resend"
          api_key          = $env.secret_key
          from             = "no-reply@edutrack.ai"
          to               = $input.email
          subject          = "EduTrack AI — Redefinição de Senha"
          message          = "Clique no link para redefinir sua senha: " + $magic_link.token
        } as $email_result
      }
    }
  }

  response = {message: "Se este e-mail estiver cadastrado, você receberá um link em breve."}
}
