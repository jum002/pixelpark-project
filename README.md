# PixelPark Project: Backend

Scalable serverless backend infrastructure built on AWS with cloud-native CI/CD workflows.

### Services

- API Gateway – Exposes REST API endpoints
- AWS Lambda – Serverless compute
- Amazon RDS (PostgreSQL) – Relational database
- Amazon Cognito – User authentication & authorization
- AWS SAM / CloudFormation – Infrastructure as Code

### API Endpoints

| Method  | Path |  Body  |  Description  |  Auth  |
| - | - | - | - | - |
| GET  | /products  |  |  get all products  |  no  |
| GET  | /products/{id}  |  |  get product by id  |  no  |
| POST  | /auth/register  | email, password |  user sign up  |  no  |
| POST  | /auth/confirm-registration  | email, code |  user email confirmation  |  no  |
| POST  | /auth/resend-confirmation  | email |  resend confirmation code to user email  |  no  |
| POST  | /auth/forgot-password  | email |  send password reset code to user email  |  no  |
| POST  | /auth/confirm-reset-password  | email, code, new_password |  user confirm reset password  |  no  |
| POST  | /auth/login  | email, password |  user login  |  no  |
| POST  | /auth/logout  | access_token |  user logout  |  no  |
| GET  | /profile  |  |  get user data  |  yes  |

### Setup

- Python Version: `3.11`.
- Create and activate virtual environment.
- Install dependencies from `requirements.txt`. 
- Run tests with `pytest`.