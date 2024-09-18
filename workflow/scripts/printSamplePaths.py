from sampleFileScripts import parseSampleFile

if __name__ == "__main__":
    paths = parseSampleFile()
    for path in paths:
        print(path)
