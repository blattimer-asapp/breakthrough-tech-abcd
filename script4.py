import json
import openai


def extract_structured_data_gpt4(conversation):
    prompt = f"""
    Given the following conversation, extract the structured data as a JSON object:
    {conversation}
    The JSON should have the following structure:
    {{
        "scenario": {{
            "personal": {{
                "customer_name": "",
                "email": "",
                "member_level": "",
                "phone": "",
                "username": ""
            }},
            "order": {{
                "street_address": "",
                "full_address": "",
                "city": "",
                "num_products": 0,
                "order_id": "",
                "packaging": "",
                "payment_method": "",
                "products": [],
                "amount": 0,
                "purchase_date": "",
                "state": "",
                "zip_code": ""
            }},
            "return": {{
                "reason": "",
                "eligible": false,
                "return_method": ""
            }}
        }}
    }}
    Fill in the values based on the information provided in the conversation. If a piece of information is not available, leave it as an empty string or 0 for numeric fields.
    Ensure that the output is a valid JSON object.
    """

    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system",
                 "content": "You are a helpful assistant that extracts structured data from conversations."},
                {"role": "user", "content": prompt}
            ]
        )
        generated_text = response.choices[0].message.content.strip()
        json_start = generated_text.find('{')
        json_end = generated_text.rfind('}') + 1

        if json_start == -1 or json_end == 0:
            return f"Error: No JSON object found in the response. Full response:\n{generated_text}"
        json_str = generated_text[json_start:json_end]
        structured_data = json.loads(json_str)
        return json.dumps(structured_data, indent=4)
    except json.JSONDecodeError as e:
        return f"Error: Unable to parse the generated JSON. Error details: {str(e)}\nGenerated text:\n{generated_text}"
    except Exception as e:
        return f"Error: An unexpected error occurred. Error details: {str(e)}"


conversation = """
[agent, 'How may I assist you today?'],
[customer, 'Hello, I need to return a book I ordered last week.'],
[agent, 'I'd be happy to help you with that. Could you please provide your full name and order number?'],
[customer, 'Certainly. My name is Olivia Nguyen, and the order number is 834135790.'],
[agent, 'Thank you, Olivia. Which book are you looking to return?'],
[customer, 'It's "The Quantum Enigma" by Bruce Rosenblum.'],
[agent, 'I see. May I ask the reason for the return?'],
[customer, 'I accidentally ordered two copies, and I only need one.'],
[agent, 'I understand. Could you please confirm your email address and phone number?'],
[customer, 'Sure, it's olivia.n@bookmail.com and 555-246-8135.'],
[agent, 'Thank you. And what's your current BookWorm membership level?'],
[customer, 'I'm a Platinum Reader.'],
[agent, 'Excellent. As a Platinum Reader, you're eligible for our express return service. Would you like us to send a courier to pick up the book?'],
[customer, 'Yes, that would be great.'],
[agent, 'Perfect. I'll arrange that for you. Could you confirm your current address?'],
[customer, '789 Library Lane, Apt 12D, Bookville, BV 67890.'],
[agent, 'Thank you, Olivia. I've scheduled a pickup for tomorrow between 10 AM and 2 PM. Once we receive the book, we'll process your refund within 2-3 business days. Is there anything else I can help you with?'],
[customer, 'No, that's all. Thank you for your help!'],
[agent, 'You're welcome, Olivia. Enjoy your reading, and have a great day!']
"""

print(extract_structured_data_gpt4(conversation))