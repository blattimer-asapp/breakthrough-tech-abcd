import json
import anthropic


def extract_structured_data_claude(conversation):
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
        client = anthropic.Client()
        response = client.completion(
            model="claude-2",
            prompt=prompt,
            max_tokens_to_sample=1000
        )
        generated_text = response.completion
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
[agent, 'How can I assist you today?'],
[customer, 'Hello, I need to return a kitchen appliance I bought two weeks ago.'],
[agent, 'I'd be happy to help you with that. Could you please provide your name and order number?'],
[customer, 'Certainly. I'm Michael Chen, and my order number is 649987654.'],
[agent, 'Thank you, Michael. Which appliance are you looking to return?'],
[customer, 'It's the Smart Pressure Cooker Pro.'],
[agent, 'I see. May I ask the reason for the return?'],
[customer, 'The lid doesn't seal properly, causing steam to escape.'],
[agent, 'I apologize for the inconvenience. Could you please confirm your email address and phone number?'],
[customer, 'Sure, it's michael.c@foodiemail.com and 555-789-0123.'],
[agent, 'Thank you. And what's your current membership level with us?'],
[customer, 'I'm a Culinary Club member.'],
[agent, 'Excellent. As a Culinary Club member, you're eligible for our premium return service. Would you like us to send a courier to pick up the item?'],
[customer, 'Yes, that would be great.'],
[agent, 'Perfect. I'll arrange that for you. Could you confirm your current address?'],
[customer, 'It's 456 Gourmet Lane, Suite 7C, Flavor Town, FT 54321.'],
[agent, 'Thank you, Michael. I've scheduled a pickup for tomorrow between 2 PM and 5 PM. Once we receive the item, we'll process your refund within 3-5 business days. Is there anything else I can help you with?'],
[customer, 'No, that's all. Thank you for your help!'],
[agent, 'You're welcome, Michael. Enjoy the rest of your day!']
"""

print(extract_structured_data_claude(conversation))