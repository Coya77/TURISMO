// Aquí puedes agregar interactividad con JavaScript, por ejemplo, un mensaje al enviar el formulario

document.querySelector('form').addEventListener('submit', function(e) {
    e.preventDefault();  // Prevenir el envío del formulario (para prueba)

    const nombre = document.getElementById('nombre').value;
    const email = document.getElementById('email').value;
    const mensaje = document.getElementById('mensaje').value;

    if (nombre && email && mensaje) {
        alert(`Gracias por tu mensaje, ${nombre}! Nos pondremos en contacto contigo a través de ${email}.`);
    } else {
        alert('Por favor, completa todos los campos.');
    }
});


