# Notes App

Aplicación de notas con tres componentes, lista para correr con Docker Compose, Kubernetes (`kubectl`) o Helm.

Los comandos se muestran en dos variantes: **Bash** (Linux, macOS, Git Bash, WSL) y **PowerShell** (Windows). Cuando son idénticos en ambos, se muestran una sola vez.

**Desde dónde se ejecuta cada cosa.** Todas las rutas son relativas a la **raíz del repo** (la carpeta que contiene `api/`, `k8s/`, `helm/`, etc.), salvo donde se indique otra:

| Etapa | Directorio de ejecución |
|---|---|
| Docker Compose | `diagnostics/` |
| kubectl (`k8s/`) | raíz del repo |
| Helm | raíz del repo |
| Tests | `api/` |

## Estructura

```
api/            API Flask (rutas, modelos, tests con pytest)
frontend/       App Angular y Dockerfile con nginx
k8s/            Manifiestos para kubectl (numerados en orden de aplicación)
helm/notes-app/ Chart de Helm equivalente
diagnostics/    Docker Compose (compose-fix.yml funcional, compose-broken.yml con errores a propósito)
.github/        CI: tests, build y push de imágenes a Docker Hub
```

## Opción 1: Docker Compose (local)

📂 **Se ejecuta desde `diagnostics/`**

**Bash**

```bash
# desde la raíz del repo
cd diagnostics
cp .env.example .env        # opcional: ajusta MONGO_APP_PASSWORD
docker compose -f compose-fix.yml up --build -d
```

**PowerShell**

```powershell
# desde la raíz del repo
cd diagnostics
Copy-Item .env.example .env   # opcional: ajusta MONGO_APP_PASSWORD
docker compose -f compose-fix.yml up --build -d
```

Abrir <http://localhost:8080>.

Con `-d` corre en segundo plano. Sin `-d` queda en primer plano mostrando los logs de todos los servicios (Ctrl+C detiene los contenedores).

Comandos útiles (iguales en Bash y PowerShell):

```
docker compose -f compose-fix.yml ps                 # estado y salud de los servicios
docker compose -f compose-fix.yml logs -f api        # logs en vivo de un servicio
docker compose -f compose-fix.yml logs --tail 50     # últimas 50 líneas de todos
docker compose -f compose-fix.yml down               # detiene y borra contenedores (conserva datos)
docker compose -f compose-fix.yml down -v            # también borra los volúmenes (se pierden los datos)
```

Orden de arranque (`depends_on` con healthchecks): `mongo` (healthy) → `api` (healthy) → `web`. Con `up -d --wait` el comando espera a que los healthchecks pasen.

## Opción 2: Kubernetes con kubectl


📂 **Se ejecuta desde la raíz del repo** (si venías de la sección anterior, vuelve con `cd ..`)

Requisitos: un cluster y `kubectl` configurado. **En nuestro caso se usó minikube** como cluster local; los comandos de esta sección y de la siguiente funcionan igual en cualquier otro cluster.


**Bash**

```bash
# 1. Namespace
kubectl apply -f k8s/00-namespace.yaml

# 2. Secrets (cambia las contraseñas)
kubectl create secret generic mongo-root -n notes-app \
  --from-literal=MONGO_INITDB_ROOT_USERNAME=root \
  --from-literal=MONGO_INITDB_ROOT_PASSWORD=rootpass

kubectl create secret generic mongo-app -n notes-app \
  --from-literal=MONGO_APP_USER=notes_app \
  --from-literal=MONGO_APP_PASSWORD=notes_pass

# 3. Mongo, API y web (en este orden)
kubectl apply -f k8s/01-mongo.yaml
kubectl apply -f k8s/02-api.yaml
kubectl apply -f k8s/03-web.yaml

# 4. Verificar
kubectl get pods -n notes-app -w
```

**PowerShell**

```powershell
# 1. Namespace
kubectl apply -f k8s/00-namespace.yaml

# 2. Secrets (cambia las contraseñas)
kubectl create secret generic mongo-root -n notes-app `
  --from-literal=MONGO_INITDB_ROOT_USERNAME=root `
  --from-literal=MONGO_INITDB_ROOT_PASSWORD=rootpass

kubectl create secret generic mongo-app -n notes-app `
  --from-literal=MONGO_APP_USER=notes_app `
  --from-literal=MONGO_APP_PASSWORD=notes_pass

# 3. Mongo, API y web (en este orden)
kubectl apply -f k8s/01-mongo.yaml
kubectl apply -f k8s/02-api.yaml
kubectl apply -f k8s/03-web.yaml

# 4. Verificar
kubectl get pods -n notes-app -w
```

La única diferencia entre ambas es el carácter de continuación de línea (`\` en Bash, `` ` `` en PowerShell).

Abrir la app con port-forward (igual en ambas shells). El comando queda corriendo y bloquea la terminal, así que déjalo en una terminal aparte:

```
kubectl port-forward svc/web 8080:80 -n notes-app
```

Luego abrir <http://localhost:8080>. Se detiene con Ctrl+C.

Notas:
- Los nombres de los Secrets (`mongo-root`, `mongo-app`) y sus claves deben quedar exactamente así: los manifiestos los leen con esos nombres.
- Con caracteres especiales en la contraseña usa comillas simples (funciona igual en Bash y PowerShell): `--from-literal=MONGO_APP_PASSWORD='P@ss$word'`. Las comillas dobles harían que `$` se interprete como variable.
- Mongo solo aplica las credenciales al inicializar el volumen. Para cambiarlas después hay que borrar el PVC `mongo-data` (**se pierden los datos**).

Para eliminar todo (igual en ambas):

```
kubectl delete namespace notes-app
```

## Opción 3: Helm

El chart **crea los Secrets** (`notes-mongo-root` y `notes-mongo-app`, con el nombre del release como prefijo). Las contraseñas no están en `values.yaml`: se pasan al instalar con `--set` y son obligatorias.

📂 **Se ejecuta desde la raíz del repo**: el chart se referencia como `./helm/notes-app`.

**Bash**

```bash
helm install notes ./helm/notes-app -n notes-app --create-namespace \
  --set mongo.rootPassword=rootpass \
  --set mongo.appPassword=notes_pass
```

**PowerShell**

```powershell
helm install notes ./helm/notes-app -n notes-app --create-namespace `
  --set mongo.rootPassword=rootpass `
  --set mongo.appPassword=notes_pass
```

Abrir la app con port-forward (igual en ambas). El comando queda corriendo, déjalo en una terminal aparte:

```
kubectl port-forward svc/notes-web 8080:80 -n notes-app
```

Luego abrir <http://localhost:8080>. Se detiene con Ctrl+C. Si usas otro nombre de release, el servicio es `<release>-web`.

Desinstalar (igual en ambas):

```
helm uninstall notes -n notes-app
```

Valores configurables en [helm/notes-app/values.yaml](helm/notes-app/values.yaml): imágenes y tags, réplicas, puertos, tipo de servicio del frontend (web) y tamaño del almacenamiento de mongo.


## CI

El workflow [.github/workflows/ci.yml](.github/workflows/ci.yml) corre en cada push a `main`, en tags `v*` y en pull requests:

1. **test**: ejecuta `pytest` sobre la API (Python 3.13).
2. **build**: construye las imágenes `notes-api` y `notes-web`. En pull requests solo valida el build; en `main` y tags las publica en Docker Hub (`latest`, `sha-<commit>` y la versión semver).

Configuración requerida en el repositorio (Settings > Secrets and variables > Actions):
- Variable `DOCKERHUB_USERNAME`
- Secret `DOCKERHUB_TOKEN` (access token de Docker Hub)
