from datetime import timedelta

class F:

    def __init__(self, column_name):
        self.column_name = column_name

    def __str__(self):
        return f"{self.column_name}"


def get_query(filters):
    base_query = "SELECT * FROM blog_post "
    for command, value in filters.items():
        if "__" in command:
            column_name, lookup = command.split("__")

            if lookup == "lte":
                base_query += f"WHERE {column_name} <= {get_value(value)}"
            elif lookup == "lt":
                base_query += f"WHERE {column_name} < {get_value(value)}"
            elif lookup == "contains":
                base_query += f"WHERE {column_name} LIKE {get_value(value, prefix='%', suffix='%')}"
            elif lookup == "startswith":
                base_query += f"WHERE {column_name} LIKE {get_value(value, suffix='%')}"
            elif lookup == "endswith":
                base_query += f"WHERE {column_name} LIKE {get_value(value, prefix='%')}"
            elif lookup == 'exact':
                base_query += f"WHERE {column_name} = {get_value(value)}"
        else:
            column_name = command
            base_query += f"WHERE {column_name} = {get_value(value)}"

    return base_query

def get_value(raw_value, prefix="", suffix=""):

    if isinstance(raw_value, F):
        return f'"blog_post"."{prefix}{raw_value}{suffix}"'
    if isinstance(raw_value, str):
        return f"'{prefix}{raw_value}{suffix}'"
    if isinstance(raw_value, int):
        return f"{prefix}{raw_value}{suffix}"


class Q:
    def __init__(self, **kwargs):
        self.filters = kwargs
        self.query = get_query(self.filters)

    def get_query(self):
        return self.query

    def split_unnecessary_part(self, another_query):
        filter_part = another_query.split("WHERE")[-1].strip(' ;')
        return filter_part

    def __or__(self, other):
        if isinstance(other, Q):
            another_query = other.get_query()
            self.query = self.query + ' OR ' + self.split_unnecessary_part(another_query)
            return self

    def __and__(self, other):
        if isinstance(other, Q):
            another_query = other.get_query()
            self.query = self.query + ' AND ' + self.split_unnecessary_part(another_query)
            return self


def custom_filter(*args, **kwargs):
    if args:
        if isinstance(args[0], Q):
            return args[0].get_query()
    query = get_query(kwargs)
    return query


# query = custom_filter(created_at__lt='2025-01-30')
# query = custom_filter(created_at__lte=F('updated_at'))
# query = custom_filter( Q(title__contains='Test') | Q(content__contains='admin'))
query = custom_filter( Q(title__contains='Test') & Q(content__contains='admin'))

# first_q = Q(title__contains='Test')
# second_q = Q(content__contains='admin')
#
# print(first_q.get_query())
# print(second_q.get_query())
#
# result = first_q | second_q
# print(result.get_query())
# query = custom_filter( result )


# query = custom_filter(title='Test Title 3')

print(query)



# lt - less than
# lte - less than or equal
