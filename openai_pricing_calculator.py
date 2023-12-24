# openai_pricing_calculator.py

def calculate_cost(model, input_token_count, output_token_count):
    # Pricing structure per 1000 tokens
    pricing = {
        'gpt-4-1106-preview': {'input': 0.01, 'output': 0.03},
        'gpt-4-1106-vision-preview': {'input': 0.01, 'output': 0.03},
        'gpt-4': {'input': 0.03, 'output': 0.06},
        'gpt-4-32k': {'input': 0.06, 'output': 0.12},
        'gpt-3.5-turbo': {'input': 0.0010, 'output': 0.0020},
        'gpt-3.5-turbo-16k': {'input': 0.0010, 'output': 0.0020},        
        'gpt-3.5-turbo-1106': {'input': 0.0010, 'output': 0.0020},
        'gpt-3.5-turbo-instruct': {'input': 0.0015, 'output': 0.0020}
    }

    if model in pricing:
        input_cost_per_1000_tokens = pricing[model]['input']
        output_cost_per_1000_tokens = pricing[model]['output']

        input_cost = (input_token_count / 1000) * input_cost_per_1000_tokens
        output_cost = (output_token_count / 1000) * output_cost_per_1000_tokens

        total_cost = input_cost + output_cost
        return total_cost
    else:
        raise ValueError(f"Unknown model: {model}")

if __name__ == "__main__":
    import sys

    if len(sys.argv) != 3:
        print("Usage: python openai_pricing_calculator.py <model> <token_count>")
        sys.exit(1)

    model = sys.argv[1]
    token_count = int(sys.argv[2])

    try:
        cost = calculate_cost(model, token_count)
        print(f"Cost for {token_count} tokens using model {model}: ${cost:.4f}")
    except ValueError as e:
        print(e)
        sys.exit(1)