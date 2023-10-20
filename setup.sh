mkdir -p ~/.streamlit/

echo "/
[server]/n/
headless = true/n/
port = $PORT/n/
eneableCORS = false/n/
/n/
" > ~/.streamlit/config.toml