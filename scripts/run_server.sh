#!/bin/sh

# Show usage information
show_help() {
  echo "Usage: sh scripts/run_server.sh [ --env <environment> ] [ --port <number> ] [ --help ]"
  echo ""
  echo "  --env   Required. Environment to use: development, staging, or production"
  echo "  --port  Optional. Port number to run the server on (default from .env or 8000)"
  echo "  --help  Show this help message"
  echo ""
  echo "Example: sh scripts/run_server.sh --env development --port 10000"
}

# Default values
ENV=""
ENV_FILE=""
RELOAD_FLAG=""
DEFAULT_PORT="8000"
APPLICATION_PORT=""
CUSTOM_PORT=""

# Parse arguments
while [ $# -gt 0 ]; do
  case "$1" in
    --env)
      if [ -n "$2" ] && [ "${2#--}" = "$2" ]; then
        ENV="$2"
        shift 2
      else
        echo "Error: Missing value for --env"
        show_help
        exit 1
      fi
      ;;
    --port)
      if [ -n "$2" ] && echo "$2" | grep -qE '^[0-9]+$'; then
        CUSTOM_PORT="$2"
        shift 2
      else
        echo "Error: Missing or invalid value for --port"
        show_help
        exit 1
      fi
      ;;
    --help|-h)
      show_help
      exit 0
      ;;
    *)
      echo "Error: Unknown argument '$1'"
      show_help
      exit 1
      ;;
  esac
done

# Handle ENV selection
case "$ENV" in
  development)
    echo "Using development environment configuration."
    ENV_FILE="env/.env.development"
    RELOAD_FLAG="--reload --reload-dir=src"
    ;;
  staging)
    echo "Using staging environment configuration."
    ENV_FILE="env/.env.staging"
    ;;
  production)
    echo "Using production environment configuration."
    ENV_FILE="env/.env.production"
    ;;
  "")
    echo "Error: Missing --env argument."
    show_help
    exit 1
    ;;
  *)
    echo "Error: Invalid environment '$ENV'"
    show_help
    exit 1
    ;;
esac

# Load the environment variables
if [ ! -f "$ENV_FILE" ]; then
  echo "Error: Environment file '$ENV_FILE' not found."
  exit 1
fi

export $(grep -v '^#' "$ENV_FILE" | xargs)

# Use HOST_IP from env or fallback
HOST=${HOST_IP:-"127.0.0.1"}

# Determine application port
if [ -n "$CUSTOM_PORT" ]; then
  APPLICATION_PORT="$CUSTOM_PORT"
elif [ -n "$APPLICATION_PORT" ]; then
  APPLICATION_PORT="$APPLICATION_PORT"
else
  echo "Warning: APPLICATION_PORT not set in $ENV_FILE. Using default port $DEFAULT_PORT."
  APPLICATION_PORT="$DEFAULT_PORT"
fi

# Activate virtual environment depending on OS
echo "Checking OS Environment"
if grep -qEi "(Microsoft|WSL)" /proc/version &>/dev/null; then
  echo "WSL detected"
  . .venv/bin/activate
else
  case "$OSTYPE" in
    linux*|darwin*)
      echo "Unix-like OS detected"
      source .venv/bin/activate
      ;;
    cygwin* | msys* | mingw*)
      echo "Windows-based OS detected"
      source .venv/Scripts/activate
      ;;
    *)
      echo "Unsupported OS."
      exit 1
      ;;
  esac
fi

# Start the server
echo "Running uvicorn server on $HOST:$APPLICATION_PORT"
uvicorn src.main:app --host "$HOST" --port "$APPLICATION_PORT" $RELOAD_FLAG
