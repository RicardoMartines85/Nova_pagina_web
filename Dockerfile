FROM node:20-alpine AS builder

WORKDIR /app
COPY package*.json ./
RUN npm install --ignore-scripts --legacy-peer-deps

COPY . .
RUN npm run build

FROM node:20-alpine

WORKDIR /app
COPY --from=builder /app/dist ./dist
COPY --from=builder /app/package.json ./package.json
COPY --from=builder /app/vite.config.ts ./vite.config.ts
COPY --from=builder /app/public ./public
COPY --from=builder /app/src ./src
COPY --from=builder /app/node_modules ./node_modules

EXPOSE 3000
ENV PORT=3000
ENV NODE_ENV=production

CMD ["npm", "run", "preview", "--", "--port", "3000", "--host", "0.0.0.0"]
