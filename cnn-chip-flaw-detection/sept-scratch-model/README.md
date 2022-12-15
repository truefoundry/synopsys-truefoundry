How to run this:

1. Install requirements  
    
    ```
    pip install -r requirements.txt
    ```

2. Login  
    
    ```
    sfy login
    ```

3. Deploy  

    ```
    python deploy.py --model_version_fqn <your-model-version-fqn> --workspace_fqn <your-workspace_fqn>
    ```

4. Test with the script

    ```
    python test.py --endpoint_url <your-endpoint-url> --image ./a.png
    ```

Endpoint url might look like: https://truefoundry.tfy-ctl-euwe1-production.production.truefoundry.com/demo-synopsys-sept-scratch-model/
