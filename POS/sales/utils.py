import random
import string

def generate_unique_sale_number():
    prefix = "SA"  
    random_part = ''.join(random.choices(string.digits, k=8))  # 8-digit random part

    return f"{prefix}-{random_part}"