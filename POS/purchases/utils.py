import random
import string

def generate_unique_order_number():
    prefix = "PO"  
    random_part = ''.join(random.choices(string.digits, k=8))  # 8-digit random part

    return f"{prefix}-{random_part}"