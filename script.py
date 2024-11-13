import json
import ollama

def extract_structured_data(conversation):
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
                "products": "",
                "amount": 0,
                "purchase_date": "",
                "state": "",
                "zip_code": ""
            }}
        }}
    }}

    Fill in the values based on the information provided in the conversation. If a piece of information is not available, leave it as an empty string or 0 for numeric fields.
    Ensure that the output is a valid JSON object.
    """

    try:
        response = ollama.generate(model="llama2", prompt=prompt)

        generated_text = response['response']

        # Find the JSON section
        json_start = generated_text.find('{')
        json_end = generated_text.rfind('}') + 1
        
        if json_start == -1 or json_end == 0:
            return f"Error: No JSON object found in the response. Full response:\n{generated_text}"

        json_str = generated_text[json_start:json_end]

        # Parse the JSON string
        structured_data = json.loads(json_str)
        return json.dumps(structured_data, indent=4)
    except json.JSONDecodeError as e:
        return f"Error: Unable to parse the generated JSON. Error details: {str(e)}\nGenerated text:\n{generated_text}"
    except Exception as e:
        return f"Error: An unexpected error occurred. Error details: {str(e)}"

#conversation input
conversation = """
[agent, 'Hi!'],
[agent, 'How can I help you?'],
[customer, 'Hi! I need to return an item, can you help me with that?'],
[agent, 'sure, may I have your name please?'],
[customer, 'Crystal Minh'],
[agent, 'thanks, may I ask the reason for the return?'],
[action, 'Account has been pulled up for Crystal Minh.'],
[customer, 'I got the wrong size.'],
[agent, 'ok, may I have your username, email address and order ID please?'],
[customer, 'Username: cminh730'],
[customer, 'cminh730@email.com'],
[customer, 'Order ID: 3348917502'],
[action, 'Purchase validation in progress ...'],
[agent, 'thanks so much! What is your membership level Crystal?'],
[customer, 'I'm a bronze'],
[agent, 'ok, was the purchase made in the last 90 days?'],
[customer, 'No, I bought it in November.']
"""

print(extract_structured_data(conversation))