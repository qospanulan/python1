

def custom_filter(*args, **kwargs):
    print(f"args: {args}")
    print(f"kwargs: {kwargs}")



# custom_filter(created_at='2025-12-01', title_contains='test')
custom_filter(True & True)
