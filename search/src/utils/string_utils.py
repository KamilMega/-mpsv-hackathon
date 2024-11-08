# Funkce pro odstranění znaku před prvním "[" a za posledním "]"
def trim_string_array(input_str):
    start_index = input_str.find("[")
    end_index = input_str.rfind("]")

    if start_index != -1 and end_index != -1 and end_index > start_index:
        return input_str[start_index:end_index+1]
    else:
        return []
