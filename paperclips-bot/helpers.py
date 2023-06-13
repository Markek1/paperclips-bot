def clean_num(s: str):
    s = s.strip()
    s = s.replace(",", "")
    s = s.replace(" ", "")

    return s
