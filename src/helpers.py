import torch

def sort_char(boxes, cls, threshold):
    line1 = []
    line2 = []
    boxes = torch.cat((boxes, cls.reshape(cls.size(dim=0),1)), 1)
    flag = 0
    for box in boxes:
        if flag == 1:
            if float(line1[0][1]/box[1]) > 1/threshold and float(line1[0][1]/box[1]) < threshold:
                line1.append(box)
            else:
                line2.append(box)
        if flag == 0:
            line1.append(box)
            flag = 1
    if len(line1) != 0 and len(line2) != 0:
        if line1[0][1] > line2[0][1] and len(line2) > 0:
            line1, line2 = line2, line1
        line2.sort(key=lambda box: -box[0])
    if len(line1) != 0:
        line1.sort(key=lambda box: -box[0])
    return line1 + line2

def track(image, model_ocr):
    fg = 1

    # results = model(image)
    # for result in results:
    #     boxes = result.boxes
    #     for box in boxes:
    #         fg = 1
    #     for i in boxes.xyxy:
    #         m, n, p, q = i
    #         crop_image = image[int(n):int(q), int(m):int(p), ::-1]
    
    plate_num = "No plate detect"
    if fg:
        result2s = model_ocr(image)
        for result2 in result2s:
            pl = sort_char(result2.boxes.xyxy, result2.boxes.cls, 1.2)

        plate_num = "".join([result2.names[char] for char in [int(ts[4]) for ts in pl]])

    return plate_num

    
