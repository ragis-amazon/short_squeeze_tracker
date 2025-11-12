# Data Processor Prototype
# Simple data processing example

def process_data(data):
    """
    Process a list of numbers and return statistics
    """
    if not data:
        return None
    
    processed = {
        'count': len(data),
        'sum': sum(data),
        'average': sum(data) / len(data),
        'min': min(data),
        'max': max(data)
    }
    
    return processed

# Example usage
sample_data = [10, 20, 30, 40, 50]
result = process_data(sample_data)

print("Data Statistics:")
print(f"Count: {result['count']}")
print(f"Sum: {result['sum']}")
print(f"Average: {result['average']}")
print(f"Min: {result['min']}")
print(f"Max: {result['max']}")

