import os
import torch
import Image_Training.Utils as Utils
import Messages.OccupancyReport as reports

async def StartSemiAutoTraining():
    device = torch.device('cuda') if torch.cuda.is_available() else torch.device('cpu')
    image_paths = Utils.GetImagePath()
    num_classes = 6
    model = Utils.get_model_instance_segmentation(num_classes)
    model.to(device)

    checkpoint_dir = "./Models/"
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
            for image_path in image_paths:
                input_image = Utils.preprocess_image(image_path).to(device)
                input_image = [input_image]

                with torch.no_grad():
                    predictions = model(input_image)
                    all_predictions.append(predictions)

                    for box, label, score in zip(predictions[0]['boxes'], predictions[0]['labels'], predictions[0]['scores']):
                       if score > 0.7:
                          category_name = Utils.get(label.item(), f"Label {label.item()}")
                       print(f"  {category_name}: {score:.2f} (Box: {box.cpu().numpy()})")

                    detected_labels = {"lights": 0.00, "lawn": 0.00, "bins": 0.00, "human": 0.00, "car": 0.00}

                    if predictions[0]['labels'] == "lights":
                        detected_labels["lights"] = predictions[0]['scores']
                    if predictions[0]['labels'] == "lawn":
                        detected_labels["lawn"] = predictions[0]['scores']
                    if predictions[0]['labels'] == "bins":
                        detected_labels["bins"] = predictions[0]['scores']
                    if predictions[0]['labels'] == "human":
                        detected_labels["human"] = predictions[0]['scores']
                    if predictions[0]['labels'] == "car":
                        detected_labels["car"] = predictions[0]['scores']

                print("Detected labels:", detected_labels)
                print(f"Predictions for {checkpoint_file} (Score > 0.7):")
        except Exception as e:
            print(f"Error processing the image for checkpoint {checkpoint_file}: {e}")

        ## New Method for Annotations
        Utils.visualize_combined_predictions(image_path, all_predictions)


