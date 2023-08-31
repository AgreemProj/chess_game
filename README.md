# Commands to run Docker container:

    docker-compose build
    docker-compose up

# Working of App:

Note: To Run the EndPoints please use postman

Example 1:

Input: {"postions": {"Queen": "E7", "Bishop": "B7", "Rook":"G5", "Knight": "C3""}}

Endpoint: /chess/knight

Request: POST

Output: {"valid_moves": ["A4", "A2", "B1","D1"]}

.

Example 2:

Input: {"postions": {"Queen": "H1", "Bishop": "B7", "Rook":"H8", "Knight": "F2"}}

Endpoint: /chess/knight

Request: POST

Output: {"valid_moves":["A1", "B1", "C1", "E1", "F1", "G1", "B7", "H8"]}
