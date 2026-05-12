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
    ocean_view = input("Ocean view? (yes/no): ")
    pool = input("Pool? (yes/no): ")
    extra = input("One standout feature (e.g. chef's kitchen, newly renovated): ")

    print("")
    print("Generating your listing... please wait.")
    print("")

    message = client.messages.create(
        model="claude-sonnet-4-5",
        max_tokens=1024,
        messages=[
            {
                "role": "user",
                "content": f"""Write a professional MLS real estate listing for a Hawaii property with these details:
Address: {address}
Neighborhood: {neighborhood}
Bedrooms: {bedrooms}
Bathrooms: {bathrooms}
Square footage: {sqft}
Price: {price}
Ocean view: {ocean_view}
Pool: {pool}
Standout feature: {extra}

Write 2 paragraphs, around 150 words total. Make it warm, compelling, and specific to Hawaii. End with a one-line call to action."""
            }
        ]
    )

    listing_text = message.content[0].text

    print("Your AI-generated listing:")
    print("")
    print(listing_text)

    filename = address.replace(" ", "_") + "_listing.txt"
    with open(filename, "w") as f:
        f.write("PROPERTY LISTING\n")
        f.write("================\n")
        f.write(f"Address: {address}\n")
        f.write(f"Price: {price}\n")
        f.write(f"Bedrooms: {bedrooms} | Bathrooms: {bathrooms} | Sqft: {sqft}\n")
        f.write("\n")
        f.write(listing_text)

    print("")
    print(f"Listing saved to: {filename}")

def view_saved_listings():
    import os
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