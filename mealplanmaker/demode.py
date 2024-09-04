from ultralytics import YOLO



model = YOLO('/Users/aliawartani/Desktop/best-2.pt')  # Load an official Detect model

datapath = '/Users/aliawartani/Desktop/test.jpg'

results = model.predict([datapath],save=True)


