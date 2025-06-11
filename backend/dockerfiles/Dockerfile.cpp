FROM gcc:latest

WORKDIR /app

# Copy and compile C++ code
COPY . .
RUN g++ -o main *.cpp -lm

CMD ["./main"]