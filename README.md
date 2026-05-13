# Hawaii AI Listing Generator

An AI-powered real estate listing generator for Hawaii properties. 
Built with Python, Flask, and the Anthropic Claude API.

## Live Demo
👉 https://listaloha.onrender.com

## Features
- Clean web interface — no terminal needed
- Generates professional MLS-style listing descriptions
- Calculates price per square foot automatically
- AI listing score and sellability rating out of 10
- Price competitiveness analysis for the Hawaii market
- Neighborhood report with walkability score
- Nearby attractions and neighborhood vibe summary
- Email-ready format saved to file

## Built with
- Python
- Flask
- Anthropic Claude API
- python-dotenv

## How to run locally
1. Clone the repository
2. Install dependencies:
   pip3 install anthropic flask python-dotenv gunicorn
3. Create a .env file and add your Anthropic API key:
   ANTHROPIC_API_KEY=your-key-here
4. Run:
   python3 app.py
5. Open https://listaloha.onrender.com in your browser

## About
Built as part of a journey into AI-powered app development, with a focus on real estate tools for the Hawaii market.