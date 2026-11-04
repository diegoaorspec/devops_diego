// Crea el usuario de la app con permisos solo sobre la base "notes".
// Se crea EN la base "notes" (antes en "admin"): la URI .../notes autentica
// contra esa base, por eso la autenticación fallaba.
// Credenciales desde el entorno; si no están, los valores originales.
db = db.getSiblingDB("notes");
db.createUser({
  user: process.env.MONGO_APP_USER || "notes_app",
  pwd: process.env.MONGO_APP_PASSWORD || "notes_pass",
  roles: [{ role: "readWrite", db: "notes" }],
});
