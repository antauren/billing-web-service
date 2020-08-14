## Requirements
Python >= 3.7


## Installation and launch
1. Clone the repository:

    ```bash
    git clone https://github.com/antauren/billing-web-service.git
    cd billing-web-service
    ```
    
2. Install requirements:
    ```
    pip install -r requirements.txt
    ```
    
3. Create environment file from example:
    ```bash
    cp .env.example .env
    ```
    
4. Personalize settings by modifying ```.env``` with your preferable text editor.
     
5. Run server:
    ```
    python server.py
    ```
    
6. Launch client:
    ```
    python client.py
    ```
