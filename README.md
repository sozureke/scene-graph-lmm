# Scene Graph Generation Project

## Overview

This project focuses on the development of a program capable of generating detailed scene graphs from data analyzed by multimodal models. The program integrates advanced machine learning techniques to process and synthesize diverse data types, enhancing the semantic perception and analytical capabilities of robotic systems. The key features include effective integration of multimodal models for diverse sensory data processing, reliable generation of accurate semantic graphs, and improved robot perception and interaction with surroundings.

## Getting Started

### Prerequisites

To run this project, you will need to set up the following:

1. **API Key for Gemini API**: Ensure you have a valid API key for the Gemini API. This key should be set in your environment variables.
2. **VPN Requirement**: Due to restrictions in Luxembourg, you must use a VPN to access the Gemini API.

### Installation

1. **Clone the Repository**

   ```sh
   git clone https://github.com/sozureke/scene-graph-lmm.git
   cd scene-graph-generation
   ```

2. **Set Up Environment Variables**
   Create a `.env` file using .env_example template in the project root directory and add your Gemini API key:

   ```sh
   GEMINI_API_KEY=your_api_key_here
   ```

3. **Install Required Packages**
   Use the `requirements.txt` file to install the necessary Python packages:
   ```sh
   pip install -r requirements.txt
   ```

### Running the Project

1. **Start the VPN**
   Ensure your VPN is active and connected to a region outside Luxembourg.

2. **Run the Program**
   Execute the main script to start the scene graph generation process:
   ```sh
   python main.py
   ```

## Disclaimer

- **VPN Requirement**: Access to the Gemini API is currently restricted in Luxembourg. You must use a VPN to connect to the API. Ensure your VPN is configured correctly before running the program.

By following these steps, you should be able to set up and run the scene graph generation program effectively. This project represents a significant advancement in the field of AI and robotics, providing a robust tool for enhancing robot perception and interaction with their environment.
