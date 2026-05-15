from flask import Flask, render_template, request, session
from dotenv import load_dotenv
import os
import anthropic

load_dotenv()
client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

app = Flask(__name__)
app.secret_key = "alohaagent-secret-2024"

@app.route("/")
def home():
    count = session.get("count", 0)
    remaining = max(0, 3 - count)
    return render_template("index.html", remaining=remaining, count=count)

@app.route("/generate", methods=["POST"])
def generate():
    if "count" not in session:
        session["count"] = 0

    if session["count"] >= 3:
        return render_template("limit.html")

    session["count"] += 1
    address = request.form["address"]
    bedrooms = request.form["bedrooms"]
    bathrooms = request.form["bathrooms"]
    sqft = request.form["sqft"]
    price = request.form["price"]
    neighborhood = request.form["neighborhood"]
    island = request.form["island"]
    ocean_view = request.form["ocean_view"]
    pool = request.form["pool"]
    extra = request.form["extra"]

    try:
        sqft_num = float(sqft.replace(",", ""))
        price_num = float(price.replace(",", "").replace("$", ""))
        price_per_sqft = round(price_num / sqft_num)
    except:
        price_per_sqft = "N/A"

    listing_response = client.messages.create(
        model="claude-sonnet-4-5",
        max_tokens=1024,
        messages=[{"role": "user", "content": f"""Write a professional MLS real estate listing for a Hawaii property with these details:
Address: {address}
Neighborhood: {neighborhood}
Island: {island}
Bedrooms: {bedrooms}
Bathrooms: {bathrooms}
Square footage: {sqft}
Price: {price}
Price per sqft: ${price_per_sqft}
Ocean view: {ocean_view}
Pool: {pool}
Standout feature: {extra}

Write 2 paragraphs, around 150 words total. Make it warm, compelling, and specific to Hawaii. End with a one-line call to action."""}]
    )

    analysis_response = client.messages.create(
        model="claude-sonnet-4-5",
        max_tokens=512,
        messages=[{"role": "user", "content": f"""You are a Hawaii real estate expert. Analyze this property:

Address: {address}, {neighborhood}, {island}
Bedrooms: {bedrooms}, Bathrooms: {bathrooms}
Square footage: {sqft}, Price: {price}
Price per sqft: ${price_per_sqft}
Ocean view: {ocean_view}, Pool: {pool}
Standout feature: {extra}

Format exactly like this:
LISTING SCORE: X/10
[2-3 sentence explanation]

PRICE ANALYSIS:
[2-3 sentence explanation]"""}]
    )

    neighborhood_response = client.messages.create(
        model="claude-sonnet-4-5",
        max_tokens=512,
        messages=[{"role": "user", "content": f"""You are a Hawaii local expert. Provide a neighborhood report for {neighborhood} on {island}, Hawaii.

Format exactly like this:
WALKABILITY SCORE: X/10
[2 sentence explanation]

NEARBY ATTRACTIONS:
- [Attraction 1 and brief description]
- [Attraction 2 and brief description]
- [Attraction 3 and brief description]
- [Attraction 4 and brief description]
- [Attraction 5 and brief description]

NEIGHBORHOOD VIBE:
[2-3 sentences]"""}]
    )

    return render_template("results.html",
        address=address,
        bedrooms=bedrooms,
        bathrooms=bathrooms,
        sqft=sqft,
        price=price,
        neighborhood=neighborhood,
        island=island,
        ocean_view=ocean_view,
        pool=pool,
        price_per_sqft=price_per_sqft,
        listing=listing_response.content[0].text,
        analysis=analysis_response.content[0].text,
        neighborhood_report=neighborhood_response.content[0].text
    )

@app.route("/waitlist", methods=["POST"])
def waitlist():
    email = request.form["email"]
    with open("waitlist.txt", "a") as f:
        f.write(email + "\n")
    return render_template("waitlist_success.html", email=email)

if __name__ == "__main__":
    app.run(debug=True)