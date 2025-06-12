FROM php:8.2-cli-alpine

WORKDIR /app

# Copy and run user code
COPY . .
RUN chmod +x /app/*

CMD ["php", "main.php"]