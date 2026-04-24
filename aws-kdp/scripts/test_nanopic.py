#!/usr/bin/env python3
import os
from dotenv import load_dotenv
from image_providers import generate_image_nanopic
from PIL import Image

def main():
    print("--- NanoPic Provider Test ---")
    load_dotenv()
    
    prompt = "A cute small cat sitting in a coffee cup, simple line art, coloring book page, bold outlines, white background"
    print(f"Prompt: {prompt}")
    
    try:
        image = generate_image_nanopic(prompt, aspect_ratio="1:1")
        
        if image:
            output_path = "test_nanopic.png"
            image.save(output_path)
            print(f"Success! Image saved to {output_path}")
            # Identify absolute path for user
            abs_path = os.path.abspath(output_path)
            print(f"Absolute path: {abs_path}")
        else:
            print("Failed to generate image (returned None).")
            
    except Exception as e:
        print(f"An error occurred during testing: {e}")

if __name__ == "__main__":
    main()
