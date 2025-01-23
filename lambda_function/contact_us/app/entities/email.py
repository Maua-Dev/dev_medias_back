import os
from typing import Tuple, Any, Dict
from datetime import datetime

import boto3


class Email:
    email_address: str
    subject: str
    message: str
    user_registered_email: str
    requested_email: str

    def __init__(self, subject: str = None, message: str = None, user_name: str = None,
                 user_email: str = None) -> None:

        self.subject = subject
        self.message = message
        self.date_time = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        self.body = f"""
       <!DOCTYPE html>
        <html lang="pt-br" charset="UTF-8">
        <head>
        </head>
        <body style="margin: 0; padding: 0; display: flex; align-items: center; justify-content: center; min-height: 100vh; background-color: white; font-family: system-ui, -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, 'Open Sans', 'Helvetica Neue', sans-serif;">
        <table class="main" style="width: 50vw; max-width: 600px; background-color: white; border-radius: 10px; box-shadow: 0px 4px 10px rgba(0, 0, 0, 0.25); overflow: hidden;">
            <tr>
            <td>
                <table class="TittleBox" style="width: 100%; background-color: black; border-radius: 10px 10px 0 0;">
                <tr>
                    <td style="text-align: center; padding: 20px;">
                        <img alt="DevMedias Logo" src="https://d22wxe17x1tv7t.cloudfront.net/devmedias.png" 
                             style="max-width: 100%; height: auto; width: 200px;" />
                        <h1 style="color:white; margin-top: 10px;"><strong>Feedback Enviado!</strong></h1>
                    </td>
                </tr>
                </table>
                <table class="ContentBox" style="width: 100%; background-color: white">
                <tr>
                    <td style="text-align: center; padding: 20px;">
                    <div class="TextsBox" style="word-wrap: break-word;">
                        <h2 style="color: #272423;">Olá!<p>Recebemos sua solicitação:</p></h2>
                        <h4 style="color: black">{self.message}</h4>
                        <h4 style="color: black;">{self.date_time}</h4>
                    </div>
                    </td>
                </tr>
                </table>
                <table class="BottomBox" style="width: 100%; background-color: rgb(3, 5, 78); border-top: 1px solid white; border-radius: 0 0 10px 10px;">
                <tr>
                    <td style="text-align: center; padding: 20px;">
                    <div class="TextsBox" style="color: white; word-wrap: break-word;">
                        <h2>Atenciosamente,</h2>
                        <h2><strong>Dev. Community Mauá</strong></h2>
                    </div>
                    </td>
                </tr>
                </table>
            </td>
            </tr>
        </table>
        </body>
        </html>
        """
        self.to_address = user_email