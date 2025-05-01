from flask import Flask, render_template, request, redirect, url_for, flash
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY') or 'tu_clave_secreta_aqui'

# Configuration for email
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'javier.surtravel@gmail.com'
app.config['MAIL_PASSWORD'] = os.getenv('GMAIL_APP_PASSWORD')  # Use app-specific password

# Rutas principales
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/destinos')
def destinos():
    return render_template('destinos.html')

@app.route('/atractivos')
def experiencias():
    return render_template('atractivos.html')

@app.route('/contacto')
def contacto():
    return render_template('contacto.html')

@app.route('/nosotros')
def nosotros():
    return render_template('nosotros.html')

# Manejo de formulario de contacto
@app.route('/enviar-formulario', methods=['POST'])
def enviar_formulario():
    if request.method == 'POST':
        try:
            # Get form data
            nombre = request.form.get('nombre')
            email = request.form.get('email')
            telefono = request.form.get('telefono', 'No proporcionado')
            asunto = request.form.get('asunto', 'Consulta desde el sitio web')
            mensaje = request.form.get('mensaje')
            
            # Validate required fields
            if not all([nombre, email, mensaje]):
                flash('Por favor complete todos los campos obligatorios', 'error')
                return redirect(url_for('contacto'))
            
            # Create email message
            msg = MIMEMultipart()
            msg['Subject'] = f"Nuevo mensaje: {asunto}"
            msg['From'] = email
            msg['To'] = 'javier.surtravel@gmail.com'
            
            # Email body
            body = f"""
            <h2>Nuevo mensaje desde el formulario de contacto</h2>
            <p><strong>Nombre:</strong> {nombre}</p>
            <p><strong>Email:</strong> {email}</p>
            <p><strong>Teléfono:</strong> {telefono}</p>
            <p><strong>Asunto:</strong> {asunto}</p>
            <p><strong>Mensaje:</strong></p>
            <p>{mensaje}</p>
            """
            
            msg.attach(MIMEText(body, 'html'))
            
            # Send email
            with smtplib.SMTP(app.config['MAIL_SERVER'], app.config['MAIL_PORT']) as server:
                server.starttls()
                server.login(app.config['MAIL_USERNAME'], app.config['MAIL_PASSWORD'])
                server.send_message(msg)
            
            flash('¡Mensaje enviado con éxito! Nos pondremos en contacto pronto.', 'success')
            return redirect(url_for('gracias'))
            
        except Exception as e:
            app.logger.error(f"Error sending email: {str(e)}")
            flash('Ocurrió un error al enviar el mensaje. Por favor intente nuevamente más tarde.', 'error')
            return redirect(url_for('contacto'))

@app.route('/gracias')
def gracias():
    return render_template('gracias.html')

# Configuración para manejar errores
@app.errorhandler(404)
def pagina_no_encontrada(e):
    return render_template('404.html'), 404

@app.errorhandler(500)
def error_servidor(e):
    return render_template('500.html'), 500

if __name__ == '__main__':
    app.run(debug=True)