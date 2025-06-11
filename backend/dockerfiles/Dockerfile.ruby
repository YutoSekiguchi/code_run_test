FROM ruby:3.2-slim

WORKDIR /app

# Copy and run Ruby code
COPY . .

CMD ["ruby", "main.rb"]