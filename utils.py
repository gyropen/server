import numpy as np
import cv2

def strokes_to_image(strokes):
    canvas = np.ones((28, 28), dtype=np.uint8) * 255  # White canvas

    # Scale points to fit 28x28
    xs = [pt['x'] for pt in strokes]
    ys = [pt['y'] for pt in strokes]
    min_x, max_x = min(xs), max(xs)
    min_y, max_y = min(ys), max(ys)

    scaled = []
    for pt in strokes:
        x = int((pt['x'] - min_x) / (max_x - min_x + 1e-5) * 27)
        y = int((pt['y'] - min_y) / (max_y - min_y + 1e-5) * 27)
        scaled.append((x, y))

    # Draw lines between points
    for i in range(1, len(scaled)):
        cv2.line(canvas, scaled[i-1], scaled[i], 0, 1)

    return canvas
