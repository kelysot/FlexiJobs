<br />
<p align="center">
    <a href="https://github.com/kelysot/FlexiJobs">
            <img src="https://i.ibb.co/JHgBRG6/2023-07-04-17-11-18.png" alt="Logo" width="200" heigt="200">
    </a>
 </p>
 
# 
 
FlexiJobs is a backend project designed to help users to find temporary job opportunities. 

It provides a REST API for job searching, user authentication, and various other essential functionalities. 

This project is built with Python, FastAPI, and PostgreSQL.

## Features

- User AuthN & AuthZ with JWT (JSON Web Tokens)
- REST API architecture for handling HTTP requests
- Sending email functionality using AWS SES (Simple Email Service)
- Image upload feature with AWS S3 integration
- Database connectivity to PostgreSQL using SQLAlchemy ORM

## Prerequisites

Before running the project, ensure you have the following prerequisites installed and set up:

- Python 3
- PostgreSQL
- AWS account with SES and S3 services enabled

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/kelysot/FlexiJobs.git

2. Create a python virtual environment
   ```bash
   python3 -m venv ./venv

3. Open the virtual environment
   ```bash
   source ./venv/bin/activate
   
4. Install the required dependencies:
   ```bash
   pip install -r ./requirements.txt

## Usage

1. In a terminal, run the application:
   ```bash
   uvicorn main:app --reload

2. The application should now be running at [http://127.0.0.1:8000/docs#/](http://127.0.0.1:8000/docs#/).

3. Explore the API endpoints.

## API Endpoints

For all types of users:

- `/register` - User registration and JWT generation
- `/login` - User login and JWT generation
- `/companies/` - Get All Companies
- `/jobs` - List of jobs
- `/jobs/{company_id}/get-jobs-by-company-id/` - Get All jobs that belong to the company

For approvers:
- `/jobs` - Create a new job
- `/jobs_users/{job_id}/get-candidates-by-job-id/` - Get all candidates that applied to the job
- `/jobs_users/{candidate_id}/approve` - Approve a candidate for the job
- `/jobs_users/{candidate_id}/reject` - Reject a candidate for the job

For admins:
- `/companies/` - Create a new company
- `/users/{user_id}/make-approver-with-company` - Make approver and connect him to the company he works for
- `/users/{user_id}/remove-approver` - Remove approver
- `/users/{user_id}/remove-admin` - Remove admin

For candidates:
- `/jobs_users` - Candidate applies for a job

   
