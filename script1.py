import json
import ollama


def extract_structured_data_llama2(conversation):
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
        response = ollama.generate(model="llama2", prompt=prompt)
        generated_text = response['response']
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
[customer, 'Hi, I need to return a solar panel I purchased last week.'],
[agent, 'I'd be happy to help with that. Can you provide your full name and order ID?'],
[customer, 'Sure, I'm Alex Greenwood and the order ID is 456356789.'],
[agent, 'Thank you, Alex. What's the reason for returning the solar panel?'],
[customer, 'It's not compatible with my home's electrical system.'],
[agent, 'I see. Could you please confirm your email address and phone number?'],
[customer, 'My email is alex.g@ecoemail.com and my phone is 555-987-6543.'],
[agent, 'Got it. And what's your current membership level with us?'],
[customer, 'I'm a Silver member.'],
[agent, 'Thank you. I see you purchased this item on November 10, 2024. As a Silver member, you're eligible for our 30-day return policy. How would you like to return the item?'],
[customer, 'Can I schedule a pickup from my home?'],
[agent, 'Certainly! I'll need your current address to arrange the pickup.'],
[customer, 'It's 789 Solar Street, Green Valley, GV 54321.'],
[agent, 'Perfect. I've scheduled a pickup for tomorrow between 9 AM and 12 PM. Is there anything else I can help you with?'],
[customer, 'No, that's all. Thank you for your help!'],
[agent, 'You're welcome, Alex. Have a great day!']
"""

print(extract_structured_data_llama2(conversation))