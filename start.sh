#!/bin/bash

# ✅ Start the FastAPI server
uvicorn main:app --host 0.0.0.0 --port 10000 --reload