import re

def getModuleOptions(config: dict) -> dict:
    options = {}
    #pattern = re.Pattern("\B--(?i)[a-z]*\s|\B-(?i)[a-z]\s")
    match = [match for match in re.finditer(r"(?i)\B--[a-z]*\s|\B-[a-z]\s", config["modules"])]
    #results = pattern.match(config["modules"])
    return options