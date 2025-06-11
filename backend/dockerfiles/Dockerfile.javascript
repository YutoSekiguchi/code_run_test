FROM node:18-slim

WORKDIR /app

# Copy and run user code
COPY . .

CMD ["node", "main.js"]