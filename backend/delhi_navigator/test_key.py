from google import genai
import os

# Aapki API Key (Jo aapne share ki thi)
MY_API_KEY = "AIzaSyCc1NAeudwmB2M4AynT0vR605dEKbr-suU" 

try:
    print("Testing connection with new SDK...")
    
    # Naya Client banayein
    client = genai.Client(api_key=MY_API_KEY)
    
    # Testing ke liye 'gemini-1.5-flash' best hai kyunki yeh stable hai
    response = client.models.generate_content(
        model="gemini-1.5-flash",
        contents="Say Hello"
    )
    
    print("\n✅ SUCCESS! API Key bilkul sahi hai aur kaam kar rahi hai.")
    print(f"Response: {response.text}")

except Exception as e:
    print("\n❌ ERROR: Abhi bhi dikkat hai!")
    print(e)