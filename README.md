# UMPD YARA Database – Police Data Management System

## Overview
The YARA Database is a full-stack Police Data Management System built as part of my DBMS project at the University of Maryland.  
It allows officers to manage incidents, arrests, and personnel efficiently through a Streamlit-based web application connected to a SQL Server database.

## Tech Stack
- Frontend: Streamlit (Python)
- Backend: SQL Server (YARA Schema)
- ETL / Seeding: Python + Faker + pyodbc
- Language: Python 3.x

## Features
- Add new Incidents, Persons, and Arrests
- Search records across multiple tables
- Automatically generate realistic data using Faker
- Relational schema with foreign keys and cascade updates
- Real-time connection between Streamlit and SQL Server

## Database Schema
Tables:
Incident • Officer • Person • Evidence • Assign • Contain • Arrest

## Setup Instructions
### 1. Clone the repository
```bash
git clone https://github.com/mahajanyash42/YARA-Database.git
cd YARA-Database
