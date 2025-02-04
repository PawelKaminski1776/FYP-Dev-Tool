import os
import torch
import Utils as utils

device = torch.device('cuda') if torch.cuda.is_available() else torch.device('cpu')


def StartSemiAutoTraining():
    image_path =  utils.GetImagePath()
    num_classes = 6
    model = utils.get_model_instance_segmentation(num_classes)
    model.to(device)

    checkpoint_dir = "../Models"
    checkpoint_files = sorted([f for f in os.listdir(checkpoint_dir) if f.startswith("fasterrcnn_model_epoch")])

    if not checkpoint_files:
        print("No checkpoints found in the directory.")

    all_predictions = []

    for checkpoint_file in checkpoint_files:
        checkpoint_path = os.path.join(checkpoint_dir, checkpoint_file)
        print(f"Loading checkpoint: {checkpoint_file}")

        checkpoint = torch.load(checkpoint_path, map_location=device)
        model.load_state_dict(checkpoint)
        model.eval()

        try:
            input_image = utils.preprocess_image(image_path).to(device)
            input_image = [input_image]

            with torch.no_grad():
                predictions = model(input_image)
                all_predictions.append(predictions)

            print(f"Predictions for {checkpoint_file} (Score > 0.3):")
            for box, label, score in zip(predictions[0]['boxes'], predictions[0]['labels'], predictions[0]['scores']):
                if score > 0.7:  # Only print predictions with score > 0.3
                    category_name = utils.get(label.item(), f"Label {label.item()}")
                    print(f"  {category_name}: {score:.2f} (Box: {box.cpu().numpy()})")
        except Exception as e:
            print(f"Error processing the image for checkpoint {checkpoint_file}: {e}")

    ## New Method for Annotations
    utils.visualize_combined_predictions(image_path, all_predictions)
