# Lithops-Storage

This guide provides two methods for running and interacting with the application.

---

## Method 1: Manual AWS Inbound Rule Setup

This method involves running the application directly and connecting to it from your local machine, which may require configuring a network rule in your AWS security group.

1.  **Execute App.py**

    On your PyRun VM, start the application server. Note that for this method to work, the application must be configured to use the HTTP transport.

    ```bash
    # Ensure this line is in the code: mcp.run(transport="http", host="0.0.0.0", port=8080)
    python3 /work/app.py
    ```

2.  **Open Inspector from your personal PC**

    From your personal PC, launch the Model-Context-Protocol Inspector.

    ```bash
    npx @modelcontextprotocol/inspector
    ```

3.  **Connect to the PyRun VM**

    In the Inspector UI, configure the connection with the following details:
    *   **Transport Type:** `streamable http`
    *   **URL:** `http://<IP_OF_VM>:8080/mcp`

    > **Note:** You may need to add an Inbound Rule to your VM's AWS Security Group to allow HTTP traffic on port `8080` from your IP address.

4.  **Example Usage**

    a. Execute `lithops_storage` without parameters.

    b. Run a `download_file` operation.

    ```python
    lithops_download_file(
          bucket="mcp-testing",
          key="customers.csv",
          file_name="/work/app.py",
    )
    ```

---

## Method 2: Using Ollama

This method uses `mcphost` to integrate with a locally running Ollama model, communicating via standard I/O instead of HTTP.

> **Prerequisites:** You have to install ollama and the model you wan't to use.

First, you must modify a line in the application code.

**Substitute this line in the code:**
`mcp.run(transport="http", host="0.0.0.0", port=8080)`

**For this one:**
`mcp.run(transport="stdio")`

### Steps

1.  **Install MCPHOST**

    ```bash
    go install github.com/mark3labs/mcphost@latest
    ```

2.  **Export Go to your PATH**

    ```bash
    export PATH=$PATH:$(go env GOPATH)/bin
    ```

3.  **Execute MCPHOST**

    Run `mcphost` and point it to the application and your desired Ollama model.

    ```bash
    mcphost --config /work/mcphost.json --model {your_model}
    ```
    > More info about MCPHOST can be found here: [https://github.com/mark3labs/mcphost](https://github.com/mark3labs/mcphost?tab=readme-ov-file)

4.  **Prompt Example**

    > Can you please download the file with the key {KEY} from the bucket {BUCKET} where save as file_name /work/{filename}, keep in my mind maybe you have to execute first lithops_storage without config since we are in pyrun.