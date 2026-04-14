def computeDeviceCrossovers(websiteVisits: list[int], appVisits: list[int]) -> int:
    if len(websiteVisits) + len(appVisits) < 2:
        return 0

    i = 0
    j = 0
    last_device = 'n'
    crossover_count = 0

    while i < len(websiteVisits) or j < len(appVisits):
        current_device = 'n'

        if j >= len(appVisits) or (i < len(websiteVisits) and websiteVisits[i] <= appVisits[j]):
            current_device = 'w'
            i += 1
        else:
            current_device = 'a'
            j += 1

        if last_device != 'n':
            if current_device != last_device:
                crossover_count += 1
        
        last_device = current_device

    return crossover_count