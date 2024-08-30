def getBytes(size: str):
    size_arr = size.split(" ")
    multiplier = 1024
    match size_arr[1]:
        case "MB":
            multiplier **= 2
        case "GB":
            multiplier **= 3
    return int(size_arr[0]) * multiplier
