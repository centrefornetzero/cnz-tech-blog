# Deploying a Docker a Google Cloud Run service
This is a tutorial guide on a bare minimum github action workflow to deploy a Google Cloud Run service

---

### Couple of things to note:
1. You need to create a service account credentials with necessary permissions (see [docs](https://cloud.google.com/api-gateway/docs/configure-dev-env))
2. `SERVICE_ACCOUNT_KEY` refers to the JSON Key of your service account which should be stored as a Github repository secret (see [docs](https://cloud.google.com/iam/docs/creating-managing-service-account-keys))
3. `SERVICE_ACCOUNT_NAME` refers to the email address of the service account

### What this Github Action does:

1. `Google Auth`: Authenticate with Google Cloud using the service account credentials
2. `Create API Config`: Creates API config with `gcloud` command line, using the Swagger 2.0 specs named `api_config.yaml`
3. `Deploy API Gateway`: Deploys the API Config to the API Gateway. This step also outputs 2 variables: `MANAGED_SERVICE_URL` and `GATEWAY_URL`
   - `MANAGED_SERVICE_URL` is a google managed service that we need to enable to enable API Gateway
   - `GATEWAY_URL` is the URL that end users will use too access the API Gateway

### YAML File
```yaml

name: Push Docker Image to Google Artifact Registry

on: [push]

env:
  ARTIFACT_REGISTRY: ${{ secrets.GCP_ARTIFACT_REGISTRY }}
  REGION: ${{ secrets.REGION }}
  SERVICE_ACCOUNT_NAME: ${{ secrets.SERVICE_ACCOUNT_NAME }}
  SERVICE_ACCOUNT_KEY: ${{ secrets.SERVICE_ACCOUNT_KEY }}
  PROJECT_ID: project_id
  API_ID: api_id
  API_GATEWAY_ID: api_gateway_id
  API_CONFIG_NAME: config_name


jobs:

  deploy-api-gateway:
    runs-on: ubuntu-latest
    steps: 

      - name: Checkout
        uses: actions/checkout@v2

      - name: Google Auth
        uses: 'google-github-actions/auth@v0'
        with:
          credentials_json: '${{ env.SERVICE_ACCOUNT_KEY }}'

      - name: Create API Config
        run: |
          gcloud api-gateway api-configs create ${{ env.API_CONFIG_NAME }} \ 
          --api=${{ env.API_ID }} \
          --openapi-spec=api_config.yaml \
          --project=${{ env.PROJECT_ID }} \
          --backend-auth-service-account=${{ env.SERVICE_ACCOUNT_NAME }}

      - name: Deploy API Gateway
        id: deploy-api-gateway
        run: |
          gcloud api-gateway gateways create ${{ env.API_GATEWAY_ID }} \
          --api=${{ env.API_ID }} \
          --api-config=${{ env.API_CONFIG_NAME }} \
          --location=${{ env.REGION }}
          
          echo "::set-output name=MANAGED_SERVICE_URL::$(gcloud api-gateway apis describe ${{ env.API_ID }} | sed -n 's/.*managedService: //p')"
          echo "::set-output name=GATEWAY_URL::$(gcloud api-gateway gateways describe ${{ env.API_GATEWAY_ID }} --location=${{ inputs.region }} | sed -n 's/.*defaultHostname: /https:\/\//p')"

      - name: Enable API Gateway
        run: |
          gcloud services enable ${{ steps.deploy-api-gateway.outputs.MANAGED_SERVICE_URL }}

      - name: Get API Gateway URL
        run: |
          echo ${{ steps.deploy-api-gateway.outputs.GATEWAY_URL }}
```