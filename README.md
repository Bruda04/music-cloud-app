# Music Cloud App

A full-stack music platform (Angular frontend + AWS-backed Python backend) designed as an example music cloud application. This repository contains an Angular frontend and a Python backend built with AWS CDK and a set of AWS Lambda handlers.

## Project Overview

This repository implements a music cloud application composed of:

- Frontend: Angular application in `frontend/` for browsing albums, artists, songs, user feed and subscriptions.
- Backend: Python project in `backend/` that uses AWS CDK to define infrastructure and includes many AWS Lambda functions under `backend/app/lambdas/` that implement the application logic.

The app provides features such as artist/album/song management, listening history, ratings, subscription notifications, and a user feed.

## Features

- Artist, album and song management endpoints (CRUD via Lambdas)
- Listening history logging
- Ratings and subscription management
- User feed generation and updates
- Cognito triggers for sign-up / post-confirmation hooks
- Angular-based UI for users and admins

## Architecture

- Frontend: Angular SPA, served during development by `ng serve`. Production builds can be deployed to AWS using S3 Web hosting + Cloud Front.
- Backend: AWS CDK (Python) defines stacks and resources. Individual Lambda handlers live under `backend/app/lambdas/*`.
- Authentication: AWS Cognito (see backend lambdas in `cognito/` for pre-signup/post-confirmation hooks).

## Prerequisites

- Node.js (recommended LTS)
- npm or yarn
- Angular CLI (if you want to use `ng` commands directly)
- Python 3.8+ (matching CDK & Lambda runtime expectations)
- pip
- (Optional, for deployment) AWS CLI configured with credentials and region
- (Optional) AWS CDK installed globally if deploying: `npm install -g aws-cdk`

## Local Development

### Frontend (Angular)

1. Install dependencies and start the dev server:

```powershell
cd frontend
npm install
npm start
# or
npx ng serve --open
```

This runs the Angular development server. By default it serves on `http://localhost:4200`.

If your frontend needs to point to a running backend, update `frontend/src/app/environment/environment.ts` to point to your API gateway or backend URL.

To build a production bundle:

```powershell
cd frontend
npm run build --if-present
```

### Backend (Python + AWS CDK)

The backend contains an AWS CDK app and many Lambda handlers placed in `backend/app/lambdas/`.

## Deploying to AWS (CDK)

1. Ensure AWS credentials are configured (e.g., with `aws configure`).
2. Install CDK (if not installed):

```powershell
npm install -g aws-cdk
```

3. From the `backend/` directory, install Python dependencies required by CDK app:

```powershell
cd backend
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

4. Bootstrap your environment (once per AWS account/region):

```powershell
cd backend
cdk bootstrap
```

5. Synthesize and deploy the stack (replace stack name if needed):

```powershell
cdk synth
cdk deploy --all
```

Note: CDK deploy will create/modify AWS resources in your account and may incur charges. Review the generated CloudFormation template and resources before deploying.

## Environment & Configuration

- Frontend environment variables: `frontend/src/app/environment/environment.ts` — update API endpoints and feature flags there.
- Backend config: `backend/app/config.py` — inspect this file for environment-driven configuration used by Lambdas and the CDK stack.

When deploying, set up necessary runtime environment variables in the Lambda function definitions (via CDK) or via the infrastructure configuration.

## Authors

- Luka Bradić ([GitHub](https://github.com/Bruda04))
- Marija Parežanin ([GitHub](https://github.com/marijaparezanin))
- Anđela Ristić ([GitHub](https://github.com/RisticAndjela))
