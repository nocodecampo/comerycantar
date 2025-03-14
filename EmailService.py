from flask_mail import Mail, Message



class EmailService:
    def __init__(self, app):
        """Inicializa Flask-Mail con la configuración de la app."""
        self.mail = Mail(app)

    def send_email(self, subject, recipients, body):
        """
        Envía un correo electrónico.

        :param subject: Asunto del correo
        :param recipients: Lista de destinatarios (ej: ["cliente@gmail.com"])
        :param body: Contenido del correo
        """
        try:
            msg = Message(subject=subject,
                          recipients=recipients,
                          body=body)
            self.mail.send(msg)
            return True
        except Exception as e:
            print(f"Error al enviar el correo: {e}")
            return False
