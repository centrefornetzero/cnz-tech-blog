# Pushing Docker Image to Google Artifact Registry
This is a tutorial guide on a bare minimum github action workflow to deploy docker images to Google Artifact Registry.

---

## Couple of things to note:
1. You need to create a service account credentials with permissions needed to push images to Google Artifact Registry
2. `SERVICE_ACCOUNT_KEY` refers to the JSON Key of your service account which should be stored as a Github repository secret (see [docs](https://cloud.google.com/iam/docs/creating-managing-service-account-keys))



## What this Github Action does:

1. `Google Auth`: Authenticate with Google Cloud using the service account credentials
2. `Build images`: Builds the docker image as prescribed in `Dockerfile` and naming it after the repo name + github commit SHA
3. `Push images`: Pushes docker image to Google Artifact Registry
4. `Tag Latest Images`: Tags the docker image we've just pushed with `latest` so we can select the latest image with just the `latest` tag without needing the commit SHA


## YAML file
```yaml
name: Push Docker Image to Google Artifact Registry

on: [push]

env:
  ARTIFACT_REGISTRY: ${{ secrets.GCP_ARTIFACT_REGISTRY }}
  REGION: ${{ secrets.REGION }}
  SERVICE_ACCOUNT_KEY: ${{ secrets.SERVICE_ACCOUNT_KEY }}


jobs:

  # Download model artefact from GCS as Faraday Service Client and upload to Github
  push-and-tag:
      runs-on: ubuntu-latest
      steps:
      - name: Checkout
        uses: actions/checkout@v2

      - name: Google Auth
        uses: 'google-github-actions/auth@v0'
        with:
          credentials_json: '${{ env.SERVICE_ACCOUNT_KEY }}'

      - name: Build images
        run: |
          gcloud auth configure-docker "$(echo "$ARTIFACT_REGISTRY" | awk -F/ '{print $1}')"
          docker buildx install
          docker build -t "$ARTIFACT_REGISTRY"/docker/"${GITHUB_REPOSITORY#*/}":"$GITHUB_SHA"

      - name: Push images
        run: |
          docker push "$ARTIFACT_REGISTRY"/docker/"${GITHUB_REPOSITORY#*/}":"$GITHUB_SHA"

      - name: Tag latest images
        run: |
            gcloud artifacts docker tags add "$ARTIFACT_REGISTRY"/docker/"${GITHUB_REPOSITORY#*/}":"$GITHUB_SHA" \
              "$ARTIFACT_REGISTRY"/docker/"${GITHUB_REPOSITORY#*/}":latest

```
