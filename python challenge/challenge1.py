import string

original_string = """g fmnc wms bgblr rpylqjyrc gr zw fylb. rfyrq ufyr amknsrcpq ypc dmp. bmgle gr gl zw fylb gq glcddgagclr ylb rfyr'q ufw rfgq rcvr gq qm jmle. sqgle qrpgle.kyicrpylq() gq pcamkkclbcb. lmu ynnjw ml rfc spj."""

map1 = "abcdefghijklmnopqrstuvwxyz"
map2 = "cdefghijklmnopqrstuvwxyzab"

mapped_table = string.maketrans(map1, map2)

print original_string.translate(mapped_table)

result = "map"

print result.translate(mapped_table)