import json
import difflib
import re
import ollama

# Step 1: Structured Data Extraction
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
        response = ollama.generate(model="llama3.1:latest", prompt=prompt)
        generated_text = response['response']

        json_start = generated_text.find('{')
        json_end = generated_text.rfind('}') + 1
        if json_start == -1 or json_end == 0:
            return None, f"Error: No JSON object found in response. Full response:\n{generated_text}"

        json_str = generated_text[json_start:json_end]
        structured_data = json.loads(json_str)
        return structured_data, None
    except Exception as e:
        return None, str(e)

def calculate_structure_score(data, flow_type):
    structure_score = 0
    max_structure_score = 25

    if 'personal' in data and 'customer_name' in data['personal']:
        structure_score += 5
    if 'order' in data and 'street_address' in data['order']:
        structure_score += 5
    if 'product' in data and 'names' in data['product']:
        structure_score += 5
    if 'flow' in data and data['flow'] == flow_type:
        structure_score += 5
    if 'subflow' in data:
        structure_score += 5

    return (structure_score / max_structure_score) * 100

def calculate_entity_score(data, flow_type):
    entity_score = 0
    max_entity_score = 20

    if data['personal']['customer_name'] == 'alessandro phoenix':
        entity_score += 5
    if 'email' in data['personal'] and '@' in data['personal']['email']:
        entity_score += 5
    if 'products' in data['order'] and 'michael_kors' in data['order']['products']:
        entity_score += 5
    if 'flow' in data and data['flow'] == 'product_defect':
        entity_score += 5

    return (entity_score / max_entity_score) * 100

def compare_generated_vs_ground_truth(generated, correct):
    similarity = difflib.SequenceMatcher(None, generated, correct).ratio()
    return similarity * 100

def format_disruption_level(generated, correct, section):
    comparison_score = compare_generated_vs_ground_truth(generated, correct)
    slight_disruption = comparison_score >= 80
    medium_disruption = 50 <= comparison_score < 80
    major_disruption = comparison_score < 50

    if slight_disruption:
        disruption_level = "Slight Disruption"
    elif medium_disruption:
        disruption_level = "Medium Disruption"
    else:
        disruption_level = "Major Disruption"

    return comparison_score, disruption_level

def evaluate_data_with_format(data, generated_data):
    flow_type = data.get('flow', '')
    structure_score = calculate_structure_score(data, flow_type)
    entity_score = calculate_entity_score(data, flow_type)
    total_score = (structure_score + entity_score) / 2

    format_comparison_scores = {}
    if structure_score == 100:
        for key in generated_data:
            if key in data and isinstance(data[key], dict):
                for subkey in generated_data[key]:
                    if subkey in data[key]:
                        correct_answer = str(data[key][subkey])
                        generated_answer = str(generated_data[key][subkey])
                        section = f"{key}.{subkey}"
                        score, level = format_disruption_level(generated_answer, correct_answer, section)
                        format_comparison_scores[section] = {
                            "comparison_score": score,
                            "disruption_level": level
                        }

    return {
        'structure_score': structure_score,
        'entity_score': entity_score,
        'total_score': total_score,
        'format_comparison_scores': format_comparison_scores if structure_score == 100 else None
    }

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

structured_data, error = extract_structured_data(conversation)
if error:
    print(f"Error extracting structured data: {error}")
else:
    correct_data = {
        "personal": {
            "customer_name": "Crystal Minh",
            "email": "cminh730@email.com",
            "member_level": "bronze",
            "phone": "",
            "username": "cminh730"
        },
        "order": {
            "street_address": "",
            "full_address": "",
            "city": "",
            "num_products": 0,
            "order_id": "3348917502",
            "packaging": "",
            "payment_method": "",
            "products": "",
            "amount": 0,
            "purchase_date": "2023-11-15",
            "state": "",
            "zip_code": ""
        },
        "flow": "return_request",
        "subflow": ""
    }

    evaluation = evaluate_data_with_format(correct_data, structured_data)
    print("\nEvaluation Results:")
    print(json.dumps(evaluation, indent=4))
