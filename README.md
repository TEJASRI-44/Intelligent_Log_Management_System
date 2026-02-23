Intelligent Log Management System


The Intelligent Log Management System is a Full Stack application designed to collect, normalize,parse, store, and manage logs from multiple formats.

Logs from different systems often come in various structures such as JSON, CSV, XML, or access logs. This system processes those different formats, converts them into a standardized internal structure, and stores them in a PostgreSQL database for efficient querying and analysis.



Key Features

* Multi-file upload support for both admin and user dashboards
* Support for JSON, CSV, XML, and access log formats
* Dedicated parser modules for each format based on content inside the log file(Content based parsing)
* Normalization layer to standardize log data
* PostgreSQL database integration using SQLAlchemy
* Cloud file storage using Appwrite
* Background log archiving using APScheduler
* Role-based access control (Admin and User)
* Login history tracking
* Audit trail for monitoring user activities
* API-based log filtering and querying


How the System Works

1. A user uploads one or more log files.
2. The files are stored securely in Appwrite cloud storage.
3. Based on the uploaded format that particular parser get dispatched using content detection.
4. The appropriate parser processes the log content by cleaning(removes spaces and duplicate lines).
5. The normalization layer converts logs into a consistent schema and parses based on category and severity.
6. During parsing not matched log lines get skipped with this parsed percentage get calculated.
7. The structured log entries after parsing gets stored in PostgreSQL.
8. Users can query and analyze logs using APIs.


Normalization Layer

Since logs come in different structures, they cannot be directly parsed.

The normalization layer ensures:

* Uniform timestamp formatting (UTC)
* Standard log levels (INFO, ERROR, WARN, DEBUG)
* Extraction of common fields such as host, environment, and message
* Clean and consistent schema for parsing.



Technology Stack

Backend
FastAPI
SQLAlchemy
PostgreSQL
APScheduler

Storage
Appwrite Cloud Storage

Frontend
React

Installation

1. Clone the repository
   git clone [https://github.com/TEJASRI-44/Intelligent_Log_Management_System.git](https://github.com/your-username/Intelligent_Log_Management_System.git)

2. Navigate into the project directory
   cd Intelligent_Log_Management_System

3. Create and activate a virtual environment
   python -m venv venv
   source venv/bin/activate  (Linux/Mac)
   venv\Scripts\activate     (Windows)

4. Install dependencies
   pip install -r requirements.txt

5. Create a .env file and configure environment variables

DATABASE_URL=your_database_url
APPWRITE_ENDPOINT=your_endpoint
APPWRITE_PROJECT_ID=your_project_id
APPWRITE_API_KEY=your_api_key

6. Run the application
   uvicorn main:app --reload

Frontend Installation (React)

1. Navigate to the frontend folder

   cd frontend

2. Install dependencies

   npm install

3. Start the development server

   npm run dev

The frontend application will run at:

[http://localhost:3000](http://localhost:3000)
