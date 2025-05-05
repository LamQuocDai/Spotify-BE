# Spotify Back End

This is the back-end implementation for a Spotify-like music streaming service. Built primarily in Python, this project provides APIs and services to manage user accounts, playlists, and music streaming functionalities.

## Features

- **User Management**: Handle user registration, authentication, and profile management.
- **Music Streaming**: APIs to serve audio tracks on demand.
- **Playlist Management**: Create, update, and delete playlists for users.
- **Search Functionalities**: Search for songs, artists, and albums.
- **Recommendation Engine**: Personalized song recommendations (if implemented).
- **Scalable Architecture**: Built to handle a large number of requests.

## Tech Stack

- **Language**: Python
- **Frameworks**: Django
- **Database**: PostgreSQL (Supabase)
- **Others**:  Docker, Redis, Celery, Amazon S3, WebSocket

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/LamQuocDai/Spotify-BE.git
   cd Spotify-BE
   ```

2. Set up a virtual environment:
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # For Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Configure environment variables:
   Create a `.env` file in the root directory and add necessary configuration (e.g., database credentials, API keys).

5. Run the application:
   ```bash
   python app.py  # Replace with the appropriate command to start the app
   ```

## Usage

- API Documentation: [Swagger/OpenAPI URL if applicable]
- Example requests:
  - **Get all playlists**:
    ```bash
    curl -X GET http://localhost:5000/api/playlists
    ```
  - **Search for a song**:
    ```bash
    curl -X GET http://localhost:5000/api/search?song_name=example
    ```

## Contributing

Contributions are welcome! Please follow these steps to contribute:

1. Fork the repository.
2. Create a new branch (`git checkout -b feature-name`).
3. Commit your changes (`git commit -m "Add feature"`).
4. Push to the branch (`git push origin feature-name`).
5. Open a pull request.

## License

This project is licensed under the [MIT License](LICENSE).

## Contact

- **Author**: Lam Quoc Dai
- **GitHub**: [LamQuocDai](https://github.com/LamQuocDai)
