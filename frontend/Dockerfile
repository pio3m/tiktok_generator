FROM node:20-alpine

WORKDIR /app

# Skopiuj tylko package.json i zainstaluj zależności
COPY package*.json ./
RUN npm install

# Skopiuj cały kod aplikacji
COPY . .

# Vite dev serwer jest uruchamiany z ./node_modules/.bin
ENV PATH="./node_modules/.bin:$PATH"

EXPOSE 3000

CMD ["npm", "run", "dev"]
