FROM gcc:latest

WORKDIR /app

# Copy and compile C code
COPY . .
RUN gcc -o main *.c -lm

CMD ["./main"]