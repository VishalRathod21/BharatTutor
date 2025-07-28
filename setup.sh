#!/bin/bash

# Create .streamlit directory if it doesn't exist
mkdir -p .streamlit

# Create config.toml with the necessary configurations
cat > .streamlit/config.toml << EOL
[server]
headless = true
port = 8501
address = "0.0.0.0"
enableCORS = false
enableXsrfProtection = false

[browser]
gatherUsageStats = false

[theme]
base = "light"
EOL

echo "Streamlit configuration created successfully!"
