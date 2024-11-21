def top1(results):
    scores = []
    for result in results:
        scores.append(result.boxes.conf)
    max_idx = scores.index(max(scores))
    xyxy = results[max_idx].boxes.xyxy[0]
    xyxy = map(int, list(xyxy))
    return xyxy

