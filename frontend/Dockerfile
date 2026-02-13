FROM node:20-alpine
WORKDIR /app
COPY frontend/package.json ./
RUN npm install
COPY frontend /app/frontend
WORKDIR /app/frontend
ENV VITE_API_URL=http://backend:8000
CMD ["npm", "run", "dev"]
