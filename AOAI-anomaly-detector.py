import os
import requests
import base64
import time

# Configuration
GPT4V_KEY = os.getenv("GPT4V_KEY")
GPT4V_ENDPOINT = os.getenv("GPT4V_ENDPOINT")

def get_encoded_image(image_path):
    """Reads and encodes image to base64."""
    with open(image_path, 'rb') as img_file:
        return base64.b64encode(img_file.read()).decode('ascii')

def classify_image(file_name, gpt4v_key, gpt4v_endpoint):
    """Classifies an image by sending it to GPT-4V for analysis."""
    
    image_path = f"C:\\Users\\mboutilier\\Documents\\chimney-anomaly-detector\\images\\{file_name}"
    encoded_image = get_encoded_image(image_path)

    # System message for classification
    system_message = """ You are an advanced AI system trained to analyze descriptions of industrial (oil refinery) chimney images. 
                        Your goal is to classify the image into one of four possible classes based on its characteristics. 
                        For every image description, return a JSON object with the following structure:
                        {
                          "classification": "<classification>",
                          "justification": "<verbose justification for the classification>"
                        }

                        Here are the four classes and their criteria:
                        1. "optimized" – clear picture of chimney with fire at the top and no irregular smoke or steam.
                        2. "too much smoke" – dark or thick smoke emanating with fire at the top of the chimney.
                        3. "too much steam" – white steam emanating with fire at the top of the chimney.
                        4. "no chimney" – image is unusable, either no visible chimney or captures something irrelevant.
                        
                        When providing the justification, explain how the observed characteristics match the criteria."""
    
    # Prepare request payload
    payload = {
        "enhancements": {
            "ocr": {"enabled": True},
            "grounding": {"enabled": True}
        },
        "messages": [
            {"role": "system", "content": [{"type": "text", "text": system_message}]},
            {"role": "user", "content": [{"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{encoded_image}"}}]}
        ],
        "temperature": 0.5,
        "top_p": 0.95,
        "max_tokens": 800
    }

    headers = {
        "Content-Type": "application/json",
        "api-key": gpt4v_key
    }
    
    # Send request and handle the response
    try:
        start_time = time.time()
        response = requests.post(gpt4v_endpoint, headers=headers, json=payload)
        response.raise_for_status()  # Raise an error for bad responses
        print(f"--- {time.time() - start_time:.2f} seconds ---")
        
        # Output response content
        classification_data = response.json()['choices'][0]['message']['content']
        print(classification_data, "\n\n")
        
        # Output token usage details
        print(response.json()['usage'])
        
    except requests.RequestException as e:
        raise SystemExit(f"Request failed: {e}")

if __name__ == '__main__':
    file_name = input("Enter the name of the image file you want to classify: ")
    classify_image(file_name, GPT4V_KEY, GPT4V_ENDPOINT)
