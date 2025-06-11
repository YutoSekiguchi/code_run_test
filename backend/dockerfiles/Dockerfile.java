FROM openjdk:17-slim

WORKDIR /app

# Copy and compile Java code
COPY . .
RUN javac *.java

CMD ["sh", "-c", "java $(basename *.java .java)"]