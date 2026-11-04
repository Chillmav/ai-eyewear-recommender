import torch
from torchvision import models, transforms
from PIL import Image
import cv2

from model.create_dataset_brows import detect_landmarks, load_dlib_detector
#ex model path model_path = 'best_model.pth'

def predict_shape(image_path, model_path='C:\\Users\\Kubus\\Desktop\\INZYNIERKA\\backend\\model\\models\\best_model.pth'):
    # ----- 1. Model -----
    model = models.efficientnet_b4(pretrained=False)
    num_classes = 5
    model.classifier = torch.nn.Sequential(
        torch.nn.Dropout(p=0.3, inplace=True),
        torch.nn.Linear(model.classifier[1].in_features, num_classes)
    )
    
    model.load_state_dict(torch.load(model_path, map_location=torch.device('cpu')))
    model.eval()

    device = "cuda" if torch.cuda.is_available() else "cpu"
    model.to(device)

    transform = transforms.Compose([
        transforms.Resize((224, 224)),
        transforms.ToTensor(),
        transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
    ])

    # ----- 2. Wczytaj obraz do modelu -----
    image = Image.open(image_path).convert('RGB')
    input_image = transform(image).unsqueeze(0).to(device)

    with torch.no_grad():
        output = model(input_image)
        _, predicted_class = torch.max(output, 1)

    class_names = ["heart", "oblong", "oval", "round", "square"]
    predicted_class_name = class_names[predicted_class.item()]

    # ----- 3. Dodaj landmarki -----
    detector, predictor = load_dlib_detector()
    landmarks = detect_landmarks(image_path, detector, predictor)

    if landmarks is not None:
        img_cv2 = cv2.imread(image_path)

        # tylko punkty twarzy, bez brwi (czyli 0–16, 27–67)
        face_shape_points = list(range(0, 17)) + list(range(27, 68))
        
        for i in face_shape_points:
            x, y = landmarks.part(i).x, landmarks.part(i).y
            cv2.circle(img_cv2, (x, y), 2, (0, 255, 0), -1)

        output_path = "C:\\Users\\Kubus\\Desktop\\INZYNIERKA\\src\\public\\face_shape.jpg"
        cv2.imwrite(output_path, img_cv2)
    else:
        output_path = None

    return predicted_class_name

