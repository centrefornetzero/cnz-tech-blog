# Deploying a Docker a Google Cloud Run service
This is a tutorial guide on a bare minimum github action workflow to deploy a Google Cloud Run service

---

### Couple of things to note:
1. You need to create a service account credentials with necessary permissions (see [docs](https://cloud.google.com/run/docs/deploying#permissions_required_to_deploy))
2. `SERVICE_ACCOUNT_KEY` refers to the JSON Key of your service account which should be stored as a Github repository secret (see [docs](https://cloud.google.com/iam/docs/creating-managing-service-account-keys))


### What this Github Action does:

1. `Google Auth`: Authenticate with Google Cloud using the service account credentials
2. `Deploy Image to Google Cloud Run`:Uses `google-github-actions/deploy-cloudrun@v0` github action to deploy container images to Google Cloud Run. For full list of configurable parameters see [docs](https://github.com/google-github-actions/deploy-cloudrun).
3. `Get Cloud Run Service URL`: Prints out the URL of the google cloud run service we've deployed in the previous step.


### YAML file

```yaml

name: Deploy Image to Google Cloud Run

on: [push]

env:
  ARTIFACT_REGISTRY: ${{ secrets.GCP_ARTIFACT_REGISTRY }}
  REGION: ${{ secrets.REGION }}
  SERVICE_ACCOUNT_KEY: ${{ secrets.SERVICE_ACCOUNT_KEY }}


jobs:

  deploy-cloud-run:
    runs-on: ubuntu-latest
    steps:

      - name: Checkout
        uses: actions/checkout@v2

      - name: Google Auth
        uses: 'google-github-actions/auth@v0'
        with:
          credentials_json: '${{ env.SERVICE_ACCOUNT_KEY }}'

      - name: Deploy Image to Google Cloud Run
        id: deploy
        uses: 'google-github-actions/deploy-cloudrun@v0'
        with:
          service: cloud_run_service_name
          region: ${{ env.REGION }}
          image: image_url

      - name: Get Cloud Run Service URL
        run: |
          echo ${{ steps.deploy.outputs.url }}
```
