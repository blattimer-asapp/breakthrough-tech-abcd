# Data Scoring Tool

This tool evaluates JSON data based on two key metrics: `structure_score` and `entity_score`. The tool is designed to assess data associated with two types of flows: `product_defect` and `storewide_query`. These scores are then used to calculate a `total_score`, which reflects the overall quality and completeness of the data.

## How It Works

### 1. Structure Score

The `structure_score` assesses whether all required fields (both rows and columns) are present in the data.

#### Flow Type: product_defect

- **Required Rows:** customer_name, email, member_level, phone, username, street_address, full_address, city, state, zip_code, num_products, order_id, packaging, payment_method, products, purchase_date, names, amounts
- **Max Structure Score:** 25 (20 rows + 5 columns)

#### Flow Type: storewide_query

- **Required Rows:** customer_name, email, member_level, phone, username, street_address, full_address, city, state, zip_code, names, amounts
- **Max Structure Score:** 19 (14 rows + 5 columns)

**Note:** The presence of specific columns (personal, order, product, flow, subflow) also contributes to the `structure_score`.

### 2. Entity Score

The `entity_score` evaluates the correctness and completeness of the data within each entity. This includes verifying data formats, matching addresses, and ensuring fields contain appropriate values.

#### Flow Type: product_defect

- **Max Entity Score:** 20
- **Scoring Criteria:**
  - **personal fields:** presence and correctness of customer_name, email, member_level, phone, username
  - **order fields:** matching street_address with full_address, zip_code with full_address, city with full_address, correctness of order_id, and presence of other order-related fields (num_products, packaging, payment_method, products, purchase_date, state)
  - **product fields:** presence of names and amounts
  - **flow and subflow fields:** correctness based on predefined options

#### Flow Type: storewide_query

- **Max Entity Score:** 14
- **Scoring Criteria:**
  - **personal fields:** similar to product_defect
  - **order fields:** similar to product_defect
  - **product fields:** should be empty (presence of names and amounts is penalized)
  - **flow and subflow fields:** correctness based on predefined options

### 3. Total Score

The `total_score` is the average of the `structure_score` and `entity_score`, giving a comprehensive evaluation of the data.

