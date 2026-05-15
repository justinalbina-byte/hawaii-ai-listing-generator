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

@app.route("/open-house")
def open_house():
    return render_template("open_house.html")

@app.route("/open-house/generate", methods=["POST"])
def open_house_generate():
    address = request.form["address"]
    neighborhood = request.form["neighborhood"]
    island = request.form["island"]
    bedrooms = request.form["bedrooms"]
    bathrooms = request.form["bathrooms"]
    price = request.form["price"]
    date = request.form["date"]
    time_start = request.form["time_start"]
    time_end = request.form["time_end"]
    extra = request.form["extra"]

    response = client.messages.create(
        model="claude-sonnet-4-5",
        max_tokens=1500,
        messages=[{"role": "user", "content": f"""You are a Hawaii real estate marketing expert. Generate three open house announcements for this property:

Address: {address}
Neighborhood: {neighborhood}
Island: {island}
Bedrooms: {bedrooms}
Bathrooms: {bathrooms}
Price: {price}
Open House Date: {date}
Time: {time_start} to {time_end}
Highlight: {extra}

Format your response EXACTLY like this:

INSTAGRAM POST:
[2-3 sentences max, warm and exciting, include the date and time, end with relevant Hawaii hashtags]

FACEBOOK POST:
[3-4 sentences, friendly and detailed, include all property details and open house info, professional tone]

EMAIL SUBJECT:
[Compelling email subject line]

EMAIL BODY:
[Professional 3-4 sentence email announcing the open house, suitable to send to a client list]"""}]
    )

    content = response.content[0].text

    sections = {}
    for section in ["INSTAGRAM POST", "FACEBOOK POST", "EMAIL SUBJECT", "EMAIL BODY"]:
        if section + ":" in content:
            start = content.index(section + ":") + len(section + ":")
            next_sections = [s + ":" for s in ["INSTAGRAM POST", "FACEBOOK POST", "EMAIL SUBJECT", "EMAIL BODY"] if s + ":" in content and content.index(s + ":") > start]
            if next_sections:
                end = content.index(next_sections[0])
                sections[section] = content[start:end].strip()
            else:
                sections[section] = content[start:].strip()

    return render_template("open_house_results.html",
        address=address,
        neighborhood=neighborhood,
        island=island,
        date=date,
        time_start=time_start,
        time_end=time_end,
        price=price,
        instagram=sections.get("INSTAGRAM POST", ""),
        facebook=sections.get("FACEBOOK POST", ""),
        email_subject=sections.get("EMAIL SUBJECT", ""),
        email_body=sections.get("EMAIL BODY", "")
    )
if __name__ == "__main__":
    app.run(debug=True)