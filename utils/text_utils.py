import os


def left(s, amount):
    return s[:amount]


def right(s, amount):
    return s[-amount:]


def mid(s, point, amount):
    return s[point:point+amount]


def mid_amos(s, point, amount):
    if point == 0:
        point = 1
    return s[point-1:point-1+amount]


def add_space(in_bit, pos):
    in_bit = left(in_bit, pos - 1) + " " + right(in_bit, len(in_bit) - pos + 1)
    return in_bit


def make_full_cd32_name(in_name):
    # check the txt file
    file_name = "settings/CD32ISO_Longname_Fixes.txt"
    content = ""

    if os.path.isfile(file_name):
        with open(file_name) as f:
            content = f.readlines()
            content = [x.strip() for x in content]
        f.close()

    for this_line in content:
        if this_line.find("|") > -1:
            find_part = left(this_line, this_line.find("|"))
            replace_part = right(this_line, len(this_line) - this_line.find("|") - 1)

            if in_name == find_part:
                in_name = replace_part

    return in_name
