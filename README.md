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
| GET  | /auth/register  | email, password |  user sign up  |  no  |
| GET  | /auth/confirm  | email, code |  user email confirmation  |  no  |
| GET  | /auth/login  | email, password |  user login  |  no  |
| GET  | /auth/logout  | access_token |  user logout  |  no  |
| GET  | /profile  |  |  get user data  |  yes  |