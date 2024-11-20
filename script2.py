import json
import openai


def extract_structured_data_gpt3(conversation):
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
        response = openai.Completion.create(
            engine="text-davinci-002",
            prompt=prompt,
            max_tokens=500
        )
        generated_text = response.choices[0].text.strip()
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
[customer, 'Hi, I received the wrong size for a dress I ordered last month.'],
[agent, 'I apologize for the inconvenience. May I have your name and order number, please?'],
[customer, 'My name is Emma Thompson, and the order number is 765123456.'],
[agent, 'Thank you, Emma. Which dress did you receive the wrong size for?'],
[customer, 'It's the Floral Summer Maxi Dress.'],
[agent, 'I see. Could you provide your email address and phone number for our records?'],
[customer, 'Sure, it's emma.t@fashionmail.com and 555-123-4567.'],
[agent, 'Perfect. What's your current membership status with us?'],
[customer, 'I'm a VIP member.'],
[agent, 'Excellent. As a VIP member, you're eligible for our express exchange service. Would you like to exchange the dress for the correct size?'],
[customer, 'Yes, please. I need a medium instead of a small.'],
[agent, 'Understood. I'll arrange for a medium to be sent to you right away. Could you confirm your shipping address?'],
[customer, 'It's 123 Runway Avenue, Apt 4B, Style City, SC 98765.'],
[agent, 'Thank you. I've processed the exchange. You'll receive the new dress within 3-5 business days, and a return label for the incorrect size will be included. Is there anything else I can help you with?'],
[customer, 'No, that's all. Thank you so much!'],
[agent, 'You're welcome, Emma. Enjoy your new dress!']
"""

print(extract_structured_data_gpt3(conversation))