#!/bin/bash

SERVER_PORT=${1-5000}
export SERVER_PORT=${SERVER_PORT}
export DATABASE_HOST=localhost
export DATABASE_PORT=5432
export DATABASE_USER=dhos-telemetry-api
export DATABASE_PASSWORD=dhos-telemetry-api
export DATABASE_NAME=dhos-telemetry-api
export AUTH0_DOMAIN=https://login-sandbox.sensynehealth.com/
export AUTH0_AUDIENCE=https://dev.sensynehealth.com/
export AUTH0_METADATA=https://gdm.sensynehealth.com/metadata
export AUTH0_JWKS_URL=https://login-sandbox.sensynehealth.com/.well-known/jwks.json
export ENVIRONMENT=DEVELOPMENT
export ALLOW_DROP_DATA=true
export PROXY_URL=http://localhost
export HS_KEY=secret
export FLASK_APP=dhos_telemetry_api/autoapp.py
export IGNORE_JWT_VALIDATION=True
export REDIS_INSTALLED=False
export LOG_LEVEL=${LOG_LEVEL:-DEBUG}
export LOG_FORMAT=${LOG_FORMAT:-COLOUR}

if [ -z "$*" ]
then
  flask db upgrade
  python3 -m dhos_telemetry_api
else
  python3 -m flask $*
fi
