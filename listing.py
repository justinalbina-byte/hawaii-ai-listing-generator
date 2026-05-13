from dotenv import load_dotenv
import os
import anthropic

load_dotenv()
client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

def generate_listing():
    print("")
    address = input("Property address: ")
    bedrooms = input("Number of bedrooms: ")
    bathrooms = input("Number of bathrooms: ")
    sqft = input("Square footage: ")
    price = input("Listing price: ")
    neighborhood = input("Neighborhood or area (e.g. Poipu, Kailua, North Shore): ")
    island = input("Island (e.g. Kauai, Oahu, Maui, Big Island): ")
    ocean_view = input("Ocean view? (yes/no): ")
    pool = input("Pool? (yes/no): ")
    extra = input("One standout feature (e.g. chef's kitchen, newly renovated): ")

    try:
        sqft_num = float(sqft.replace(",", ""))
        price_num = float(price.replace(",", "").replace("$", ""))
        price_per_sqft = round(price_num / sqft_num)
    except:
        price_per_sqft = "N/A"

    print("")
    print("Generating your listing... please wait.")
    print("")

    listing_response = client.messages.create(
        model="claude-sonnet-4-5",
        max_tokens=1024,
        messages=[
            {
                "role": "user",
                "content": f"""Write a professional MLS real estate listing for a Hawaii property with these details:
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

Write 2 paragraphs, around 150 words total. Make it warm, compelling, and specific to Hawaii. End with a one-line call to action."""
            }
        ]
    )

    listing_text = listing_response.content[0].text

    analysis_response = client.messages.create(
        model="claude-sonnet-4-5",
        max_tokens=512,
        messages=[
            {
                "role": "user",
                "content": f"""You are a Hawaii real estate expert. Analyze this property and give two things:

1. LISTING SCORE: Rate this property's sellability out of 10 and explain why in 2-3 sentences.
2. PRICE ANALYSIS: Based on the details, is the asking price competitive, high, or low for this Hawaii neighborhood? Give a brief 2-3 sentence explanation.

Property details:
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

Format your response exactly like this:
LISTING SCORE: X/10
[Your explanation]

PRICE ANALYSIS:
[Your explanation]"""
            }
        ]
    )

    analysis_text = analysis_response.content[0].text

    neighborhood_response = client.messages.create(
        model="claude-sonnet-4-5",
        max_tokens=512,
        messages=[
            {
                "role": "user",
                "content": f"""You are a Hawaii local expert. Provide a neighborhood report for {neighborhood} on {island}, Hawaii.

Format your response exactly like this:

WALKABILITY SCORE: X/10
[2 sentence explanation of walkability, car dependency, and access to amenities on foot]

NEARBY ATTRACTIONS:
- [Attraction 1 and brief description]
- [Attraction 2 and brief description]
- [Attraction 3 and brief description]
- [Attraction 4 and brief description]
- [Attraction 5 and brief description]

NEIGHBORHOOD VIBE:
[2-3 sentences describing the overall feel, who it attracts, and what makes it unique]"""
            }
        ]
    )

    neighborhood_text = neighborhood_response.content[0].text

    email_text = f"""Subject: New Listing — {address}, {neighborhood} | {bedrooms}BD/{bathrooms}BA | ${price}

Hi [Client Name],

I wanted to share this exciting new listing with you.

{listing_text}

PROPERTY DETAILS:
- Address: {address}
- Neighborhood: {neighborhood}
- Island: {island}
- Bedrooms: {bedrooms}
- Bathrooms: {bathrooms}
- Square Footage: {sqft}
- Listing Price: ${price}
- Price per Sq Ft: ${price_per_sqft}
- Ocean View: {ocean_view}
- Pool: {pool}

NEIGHBORHOOD HIGHLIGHTS:
{neighborhood_text}

Please don't hesitate to reach out if you'd like to schedule a showing or have any questions.

Mahalo,
[Your Name]
[Your Phone]
[Your Email]"""

    print("=" * 50)
    print("AI-GENERATED LISTING")
    print("=" * 50)
    print("")
    print(listing_text)
    print("")
    print("=" * 50)
    print("PROPERTY ANALYSIS")
    print("=" * 50)
    print("")
    print(analysis_text)
    print("")
    print("=" * 50)
    print("NEIGHBORHOOD REPORT")
    print("=" * 50)
    print("")
    print(neighborhood_text)
    print("")
    print("=" * 50)
    print("PROPERTY SUMMARY")
    print("=" * 50)
    print(f"Address:        {address}")
    print(f"Neighborhood:   {neighborhood}")
    print(f"Island:         {island}")
    print(f"Bedrooms:       {bedrooms}")
    print(f"Bathrooms:      {bathrooms}")
    print(f"Square footage: {sqft}")
    print(f"Listing price:  ${price}")
    print(f"Price per sqft: ${price_per_sqft}")

    filename = address.replace(" ", "_") + "_listing.txt"
    with open(filename, "w") as f:
        f.write("PROPERTY LISTING\n")
        f.write("=" * 50 + "\n")
        f.write(f"Address: {address}\n")
        f.write(f"Price: ${price}\n")
        f.write(f"Bedrooms: {bedrooms} | Bathrooms: {bathrooms} | Sqft: {sqft}\n")
        f.write(f"Price per Sqft: ${price_per_sqft}\n")
        f.write("\n")
        f.write("AI-GENERATED LISTING\n")
        f.write("=" * 50 + "\n")
        f.write(listing_text)
        f.write("\n\n")
        f.write("PROPERTY ANALYSIS\n")
        f.write("=" * 50 + "\n")
        f.write(analysis_text)
        f.write("\n\n")
        f.write("NEIGHBORHOOD REPORT\n")
        f.write("=" * 50 + "\n")
        f.write(neighborhood_text)
        f.write("\n\n")
        f.write("EMAIL READY FORMAT\n")
        f.write("=" * 50 + "\n")
        f.write(email_text)

    print("")
    print(f"Listing saved to: {filename}")
    print("(Includes listing, analysis, neighborhood report, and email format)")

def view_saved_listings():
    files = [f for f in os.listdir(".") if f.endswith("_listing.txt")]
    if not files:
        print("")
        print("No saved listings yet.")
    else:
        print("")
        print("Saved listings:")
        for i, f in enumerate(files, 1):
            print(f"  {i}. {f}")

def main():
    print("================================")
    print("  Hawaii AI Listing Generator")
    print("================================")

    while True:
        print("")
        print("What would you like to do?")
        print("  1. Generate a new listing")
        print("  2. View saved listings")
        print("  3. Quit")
        print("")
        choice = input("Enter 1, 2, or 3: ")

        if choice == "1":
            generate_listing()
        elif choice == "2":
            view_saved_listings()
        elif choice == "3":
            print("")
            print("Goodbye!")
            break
        else:
            print("")
            print("Invalid choice — please enter 1, 2, or 3.")

main()