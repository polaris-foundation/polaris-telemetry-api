# dhos-telemetry-api Integration Tests
This folder contains service-level integration tests for the dhos-telemetry-api.

## Running the tests
```
# run tests
$ make test-local

# inspect test logs
$ docker logs dhos-telemetry-api-integration-tests

# cleanup
$ docker-compose down
```

## Test development
For test development purposes you can keep the service running and keep re-running only the tests:
```
# in one terminal screen, or add `-d` flag if you don't want the process running in foreground
$ docker-compose up --force-recreate

# in the other terminal screen you can now run the tests
$ DHOS_TELEMETRY_BASE_URL=http://localhost:5000 \
  HS_ISSUER=http://localhost/ \
  HS_KEY=secret \
  PROXY_URL=http://localhost \
  behave --no-capture

# Don't forget to clean up when done!
$ docker-compose down
```
