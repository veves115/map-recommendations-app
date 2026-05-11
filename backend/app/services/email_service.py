import resend
import os
import logging

logger = logging.getLogger(__name__)


class EmailService:

    @staticmethod
    def send_password_reset(to_email: str, username: str, token: str):
        resend.api_key = os.getenv("RESEND_API_KEY")
        frontend_url = os.getenv("FRONTEND_URL", "http://localhost:5173")
        reset_url = f"{frontend_url}/reset-password?token={token}"

        try:
            result = resend.Emails.send({
                "from": "onboarding@resend.dev",
                "to": to_email,
                "subject": "Recuperar contraseña — MapApp",
                "html": f"""
                    <h2>Hola, {username}</h2>
                    <p>Recibimos una solicitud para recuperar tu contraseña.</p>
                    <p>
                        <a href="{reset_url}">Restablecer contraseña</a>
                    </p>
                    <p>Este enlace expira en 1 hora.</p>
                """,
            })
            logger.info("Email enviado: %s", result)
        except Exception as e:
            logger.error("Error enviando email: %s", e)
