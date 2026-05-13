# Hawaii AI Listing Generator

An AI-powered real estate listing generator for Hawaii properties. 
Built with Python, Flask, and the Anthropic Claude API.

## Features
- Clean web interface — no terminal needed
- Generates professional MLS-style listing descriptions
- Calculates price per square foot automatically
- AI listing score and sellability rating out of 10
- Price competitiveness analysis for the Hawaii market
- Neighborhood report with walkability score
- Nearby attractions and neighborhood vibe summary

## Built with
- Python
- Flask
- Anthropic Claude API
- python-dotenv

## How to run
1. Clone the repository
2. Install dependencies:
   pip3 install anthropic flask python-dotenv
3. Create a .env file and add your Anthropic API key:
   ANTHROPIC_API_KEY=your-key-here
4. Run:
   python3 app.py
5. Open http://127.0.0.1:5000 in your browser