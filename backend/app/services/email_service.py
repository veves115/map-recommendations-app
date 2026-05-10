import resend
import os


class EmailService:

    @staticmethod
    def send_password_reset(to_email: str, username: str, token: str):
        resend.api_key = os.getenv("RESEND_API_KEY")
        frontend_url = os.getenv("FRONTEND_URL", "http://localhost:5173")
        reset_url = f"{frontend_url}/reset-password?token={token}"

        resend.Emails.send({
            "from": "onboarding@resend.dev",
            "to": to_email,
            "subject": "Recuperar contraseña — MapApp",
            "html": f"""
                <h2>Hola, {username}</h2>
                <p>Recibimos una solicitud para recuperar tu contraseña.</p>
                <p>
                    <a href="{reset_url}" style="
                        background:#000;color:#fff;padding:12px 24px;
                        border-radius:8px;text-decoration:none;font-weight:bold;
                    ">
                        Restablecer contraseña
                    </a>
                </p>
                <p>Este enlace expira en 1 hora. Si no solicitaste esto, ignora este email.</p>
            """,
        })
