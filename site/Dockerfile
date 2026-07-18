# Etapa 1: build
# Contexto de build = raíz del repo (Zay-M3/Learning)
# Esto permite que sync-content.mjs acceda a las carpetas de sesiones
# (arquitectura-software/, agentes-ia/, etc.) que viven fuera de site/.
FROM node:22-alpine AS builder

# nbconvert requiere Python 3 + pip (para convertir .ipynb → HTML estático)
RUN apk add --no-cache python3 py3-pip
RUN pip3 install --no-cache-dir --break-system-packages nbconvert jupyter-client ipykernel

WORKDIR /app

# Copiar dependencias primero (mejor cache de Docker)
COPY site/package.json site/package-lock.json* ./
RUN npm ci || npm install

# Copiar todo el código del sitio
COPY site/ ./

# Copiar las carpetas de sesiones del repo raíz (necesarias para sync-content)
# Estas NO se incluyen en el contexto de Astro (que solo mira src/content/)
COPY arquitectura-software/ /repo-sessions/arquitectura-software/
COPY agentes-ia/ /repo-sessions/agentes-ia/
COPY algoritmia/ /repo-sessions/algoritmia/
COPY ingenieria-de-requisitos/ /repo-sessions/ingenieria-de-requisitos/
COPY ingenieria-de-software/ /repo-sessions/ingenieria-de-software/

# Variable de entorno: sync-content.mjs usa esto como REPO_ROOT alternativo
ENV LEARNING_REPO_ROOT=/repo-sessions
RUN node scripts/sync-content.mjs && \
    python3 scripts/notebooks.py && \
    npm run build && \
    # Eliminar el HTML de notebooks del dist (lo servimos desde public/)
    rm -rf dist/algoritmia/notebooks

# Etapa 2: nginx
FROM nginx:1.27-alpine
RUN rm -f /etc/nginx/conf.d/default.conf
COPY site/nginx.conf /etc/nginx/conf.d/default.conf
COPY --from=builder /app/dist /usr/share/nginx/html
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]