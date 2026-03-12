# This file enables FastAPI to run on Vercel serverless functions
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import os
from dotenv import load_dotenv

# Import your main app
from main import app

# The app is already configured in main.py and exports as 'app'
# Vercel will use this file to run the FastAPI application as a serverless function

# Export the app for Vercel
__all__ = ['app']
