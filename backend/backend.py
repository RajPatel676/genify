# from flask import Flask, request, jsonify, send_file
# from flask_cors import CORS
# import shutil
# import os
# import base64
# import io
# from gradio_client import Client
# import tempfile
# from PIL import Image

# app = Flask(__name__)
# CORS(app)  # Enable CORS for all routes

# # Your original filename function
# def short_filename(prompt):
#     # Extract keywords like "cute cat" only
#     keywords = ["cat", "dog", "robot", "man", "woman", "bird", "flower", "landscape", "sunset", "tree", "baby", "animal", "space", "car", "house"]
#     descriptors = ["cute", "beautiful", "realistic", "magic", "super", "tiny", "dark", "light"]
#     words = prompt.lower().split()
#     picked = [word for word in words if word in keywords or word in descriptors]
#     return "".join(picked[:3]) if picked else "generated"

# @app.route('/api/generate-image', methods=['POST'])
# def generate_image():
#     try:
#         data = request.json
        
#         # Extract parameters
#         prompt = data.get('prompt', '')
#         negative_prompt = data.get('negative_prompt', '')
#         seed = data.get('seed', 0)
#         width = data.get('width', 1024)
#         height = data.get('height', 1024)
#         guidance_scale = data.get('guidance_scale', 6)
#         randomize_seed = data.get('randomize_seed', True)
        
#         if not prompt:
#             return jsonify({'success': False, 'error': 'Prompt is required'}), 400
        
#         print(f"Generating image with prompt: {prompt}")
        
#         # Initialize Gradio client
#         client = Client("prithivMLmods/FLUX-REALISM")
        
#         # Call the API
#         result = client.predict(
#             prompt=prompt,
#             negative_prompt=negative_prompt,
#             seed=seed,
#             width=width,
#             height=height,
#             guidance_scale=guidance_scale,
#             randomize_seed=randomize_seed,
#             api_name="/run"
#         )
        
#         # Get the image path from result
#         image_path = result[0][0]["image"]
#         print(f"Generated image path: {image_path}")
        
#         # Read and convert image to base64 for frontend display
#         with open(image_path, 'rb') as img_file:
#             img_data = img_file.read()
#             img_base64 = base64.b64encode(img_data).decode('utf-8')
#             img_base64_url = f"data:image/jpeg;base64,{img_base64}"
        
#         # Generate filename
#         filename = short_filename(prompt) + ".jpg"
        
#         # # Optional: Save to your custom directory
#         # custom_save_path = os.path.join("C:/Users/patel/Desktop/RAJ LJ/", filename)
#         # os.makedirs(os.path.dirname(custom_save_path), exist_ok=True)
#         # shutil.copy(image_path, custom_save_path)
#         # print(f"Image saved to: {custom_save_path}")
        
#         return jsonify({
#             'success': True,
#             'image_url': img_base64_url,  # Base64 data URL for display
#             'image_base64': img_base64_url,  # For download
#             'filename': filename,
#             # 'saved_path': custom_save_path
#         })
        
#     except Exception as e:
#         print(f"Error generating image: {str(e)}")
#         return jsonify({
#             'success': False, 
#             'error': str(e)
#         }), 500

# @app.route('/api/health', methods=['GET'])
# def health_check():
#     return jsonify({'status': 'Server is running!', 'message': 'Backend is ready for image generation'})

# @app.route('/', methods=['GET'])
# def home():
#     return '''
#     <h1>AI Image Generator Backend</h1>
#     <p>Server is running!</p>
#     <p>Endpoints:</p>
#     <ul>
#         <li>POST /api/generate-image - Generate images</li>
#         <li>GET /api/health - Health check</li>
#     </ul>
#     '''

# if __name__ == '__main__':
#     print("Starting Flask server...")
#     print("Make sure to install requirements: pip install flask flask-cors gradio-client pillow")
#     print("Server will run on http://localhost:5000")
#     app.run(debug=True, host='0.0.0.0', port=5000)


from flask import Flask, request, jsonify
from flask_cors import CORS
import base64
import os
from gradio_client import Client
import traceback

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

def short_filename(prompt):
    keywords = ["cat", "dog", "robot", "man", "woman", "bird", "flower", "landscape", "sunset", "tree", "baby", "animal", "space", "car", "house"]
    descriptors = ["cute", "beautiful", "realistic", "magic", "super", "tiny", "dark", "light"]
    words = prompt.lower().split()
    picked = [word for word in words if word in keywords or word in descriptors]
    return "".join(picked[:3]) if picked else "generated"

@app.route('/api/generate-image', methods=['POST'])
def generate_image():
    try:
        data = request.json

        prompt = data.get('prompt', '')
        negative_prompt = data.get('negative_prompt', '')
        seed = data.get('seed', 0)
        width = data.get('width', 1024)
        height = data.get('height', 1024)
        guidance_scale = data.get('guidance_scale', 6)
        randomize_seed = data.get('randomize_seed', True)

        if not prompt:
            return jsonify({'success': False, 'error': 'Prompt is required'}), 400

        print(f"Generating image with prompt: {prompt}")

        client = Client("prithivMLmods/FLUX-REALISM")

        result = client.predict(
            prompt=prompt,
            negative_prompt=negative_prompt,
            seed=seed,
            width=width,
            height=height,
            guidance_scale=guidance_scale,
            randomize_seed=randomize_seed,
            api_name="/run"
        )

        image_path = result[0][0]["image"]
        print(f"Generated image path: {image_path}")

        with open(image_path, 'rb') as img_file:
            img_data = img_file.read()
            img_base64 = base64.b64encode(img_data).decode('utf-8')
            img_base64_url = f"data:image/jpeg;base64,{img_base64}"

        filename = short_filename(prompt) + ".jpg"

        return jsonify({
            'success': True,
            'image_url': img_base64_url,
            'image_base64': img_base64_url,
            'filename': filename
        })
    except Exception as e:
            traceback.print_exc()
            if "GPU quota" in str(e):
                    return jsonify({'success': False,'error': '🚫 Gradio GPU quota exceeded. Please wait and try again in 24 hours.'}), 429
            return jsonify({'success': False, 'error': str(e)}), 500                    


@app.route('/api/health', methods=['GET'])
def health_check():
    return jsonify({'status': 'Server is running!', 'message': 'Backend is ready for image generation'})

@app.route('/', methods=['GET'])
def home():
    return '''
    <h1>AI Image Generator Backend</h1>
    <p>Server is running!</p>
    <ul>
        <li>POST /api/generate-image - Generate images</li>
        <li>GET /api/health - Health check</li>
    </ul>
    '''

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
