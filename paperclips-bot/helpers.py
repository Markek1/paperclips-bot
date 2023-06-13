def clean_num(s: str):
    s = s.strip()
    s = s.replace(",", "")
    s = s.replace(" ", "")

    return s


def is_valid_btn(btn):
    return btn.is_enabled() and btn.is_displayed()
