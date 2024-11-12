def is_success(result):
    for line in result.split("\n"):
        if line.strip() == "Success":
            return True
    return False