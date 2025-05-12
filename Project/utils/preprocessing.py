import torchvision.transforms as transforms


def preprocess_image(image, target_size=(1440, 1440)):
    transform_pipeline = transforms.Compose([
        transforms.Resize(target_size),
        transforms.ToTensor(),
        # Uncomment and adjust if normalization is required by your model:
        # transforms.Normalize(mean=[0.485, 0.456, 0.406],
        #                      std=[0.229, 0.224, 0.225])
    ])
    return transform_pipeline(image)
