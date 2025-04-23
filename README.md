# gestion

cómo usar desde Next.js
Cuando el usuario inicia sesión desde tu frontend:

Envía un POST a /login con username=email y password

Recibe el access_token

Guarda el token en localStorage o cookies

Agrega este header en las llamadas futuras:

http
Copy
Edit
Authorization: Bearer <access_token>