# Twitter Airflow ETL Project

A data pipeline project that extracts tweets from Twitter/X (specifically from @elonmusk), transforms the data, and loads it into AWS S3 using Apache Airflow for orchestration.

## 📋 Project Overview

This project demonstrates a complete ETL (Extract, Transform, Load) pipeline using:
- **Twitter API v2** (via Tweepy) - for fetching tweets
- **Apache Airflow** - for scheduling and orchestrating the pipeline
- **AWS S3** - for storing the extracted tweet data
- **AWS EC2** - for hosting the Airflow instance

The pipeline fetches tweets along with engagement metrics (likes, retweets) and stores them as JSON files in S3 with a timestamp-based directory structure.

## 🛠️ Prerequisites

Before you start, make sure you have:
- An **AWS EC2 instance** (running Ubuntu or similar Linux distribution)
- A **Twitter/X Developer Account** with API access (API keys, Bearer Token)
- **AWS S3 bucket** created for data storage
- **AWS credentials** configured on your EC2 instance

## 📥 Installation Guide

Follow these steps to set up the project on your AWS EC2 instance:

### Step 1: Update System Packages

```bash
sudo apt-get update
```

This updates the package lists on your EC2 instance to ensure you have access to the latest versions.

### Step 2: Create Project Directory

```bash
# Create a directory for your project
mkdir airflow-project && cd airflow-project
```

This creates a new directory where all your Airflow project files will be stored.

### Step 3: Set Up Python Virtual Environment

```bash
# Create a virtual environment
python3 -m venv venv

# Activate the virtual environment
source venv/bin/activate
```

A virtual environment isolates your project dependencies from the system Python, preventing conflicts with other projects.

**Note:** Every time you open a new terminal/SSH session to work on this project, you'll need to activate the environment using:
```bash
source venv/bin/activate
```

### Step 4: Install Required Python Packages

```bash
pip install apache-airflow
pip install tweepy
pip install datetime
pip install boto3
```

**Package Details:**
- **apache-airflow** - Workflow orchestration platform
- **tweepy** - Python library for accessing the Twitter API
- **datetime** - For handling date and time operations
- **boto3** - AWS SDK for Python (used for S3 interactions)

## ⚙️ Configuration Steps

### Step 1: Copy Project Files to Airflow DAGs Folder

Once Airflow is installed, copy your ETL and DAG Python files:

```bash
# Find your Airflow home directory (usually ~/airflow)
cd ~/airflow

# Copy your files to the dags folder
cp /path/to/twitter_dag.py dags/
cp /path/to/twitter_etl.py dags/
```

### Step 2: Update airflow.cfg

Edit the Airflow configuration file to specify the DAGs folder path:

```bash
nano ~/airflow/airflow.cfg
```

Find and update the `dags_folder` setting to point to your project's DAGs folder:

```
dags_folder = /path/to/airflow-project/dags
```

Save and exit (Ctrl+X, then Y, then Enter in nano).

### Step 3: Configure Twitter API Credentials

Create the following credentials for the app from Twitter
    bearerToken
    SecretKey
    ConsumerKey

## 🚀 Running the Project

### Start Airflow Services

In separate terminal session, run:

```bash
airflow standalone
```

The Airflow UI will be accessible at `http://<your_ec2_instance_public_ip>:8080`

username and password to login to airflow ui will be available inside airflow directory

### Monitor and Trigger DAGs

1. Open your browser and navigate to the Airflow UI
2. Log in with your admin credentials
3. Find your Twitter DAG in the list
4. Click the play button to trigger a manual run, or wait for the scheduled execution

## 📁 Project File Structure

```
airflow-project/
├── venv/                          # Python virtual environment
├── dags/
│   ├── twitter_dag.py            # Airflow DAG definition
│   └── twitter_etl.py            # ETL logic
└── README.md                     # This file
```

## 📊 How It Works

1. **Extract** - The Airflow DAG triggers the ETL script at scheduled intervals
2. **Transform** - The script queries Twitter API for @elonmusk's latest tweets with metrics
3. **Load** - Transformed data is formatted as JSON and uploaded to AWS S3
4. **Storage** - Data is organized in S3 with the structure: `twitter_ingestion/{username}/tweets_{timestamp}.json`

## 🐛 Troubleshooting

### Issue: "Module not found" errors
**Solution:** Make sure your virtual environment is activated:
```bash
source venv/bin/activate
```

### Issue: Twitter API authentication fails
**Solution:** Verify your Bearer Token is correct and has the necessary permissions in the Twitter Developer Dashboard

### Issue: S3 upload fails
**Solution:** Check that:
- AWS credentials are properly configured
- S3 bucket exists and is accessible
- IAM user has `s3:PutObject` permissions

### Issue: Airflow DAG not appearing
**Solution:** Ensure the dags folder path in `airflow.cfg` is correct and DAG files are in that location



