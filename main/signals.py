# -*- coding: utf-8 -*-
from django.core.mail import EmailMessage
from django_rest_passwordreset.signals import reset_password_token_created
from django.core.mail import EmailMultiAlternatives
from django.dispatch import receiver
from django.template.loader import render_to_string

@receiver(reset_password_token_created)
def password_reset_token_created(sender, instance, reset_password_token, **kwargs):
    user = reset_password_token.user
    token = reset_password_token.key


    reset_url = f"http://192.168.1.123/reset-password/?token={token}"

    html_message = f"""
        <html>
            <body style="color: #715D4C; font-family: Arial, sans-serif;">
                <h2>R&eacute;initialisation de votre mot de passe - <strong>Patrimoine en jeu</strong></h2>
                <p>Bonjour {user.first_name}, </p>
                <p>Nous avons reçu une demande pour r&eacute;initialiser votre mot de passe.</p>

                <p style="margin: 20px 0;">
                    <a href="{reset_url}" style="background-color: #715D4C; color: #FAFAFA; padding: 10px 20px; text-decoration: none; border-radius: 5px; font-weight: bold;">
                        R&eacute;initialiser mon mot de passe
                    </a>
                 </p>

                <p>Si vous n'avez pas demand&eacute; cette r&eacute;initialisation, vous pouvez ignorer ce message.</p>                
                <p>Cordialement,<br>L'&eacute;quipe <strong>Patrimoine en jeu</strong></p>

                    <div style="margin-top: 30px;">
                        <img src="https://i.imgur.com/uK7CvDZ.png" alt="Logo Patrimoine en jeu" width="150" style="margin-bottom: 20px;">
                    </div>
            </body>
        </html>
    """

    email = EmailMessage(
        subject = "Réinitialisation de votre mot de passe - Patrimoine en jeu",
        body = html_message,
        from_email = 'Patrimoine en jeu <patrimoine.en.jeu@gmail.com>',
        to=[user.email]
    )
    email.content_subtype = 'html'
    email.send()