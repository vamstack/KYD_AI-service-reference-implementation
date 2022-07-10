# KYD_AI-service-reference-implementation

## Requirements

- docker engine
- `docker-compose` version 2.6 or greater
  ```bash
  ❯ docker-compose -v
  Docker Compose version 2.6.0
  ```

## Installation

Open new terminal emulator and issue the following command

```bash
git clone git@github.com:vamstack/KYD_AI-service-reference-implementation.git
cd KYD_AI-service-reference-implementation
docker-compose up
```

## Test the setup

Open new terminal emulator and issue the following command

```bash
docker-compose exec http-server python3 generate_local_mock_request.py
```
