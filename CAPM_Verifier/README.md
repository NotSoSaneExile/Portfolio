# CAPM Verifier
This tool allows users to create a portfolio from either stocks or funds found on the WIG20 index, and perform calculations to determine whether the portfolio is well-valued and efficient according to the Capital Asset Pricing Model (CAPM).

# Dependencies
The CAPM Verifier uses the following Python dependencies:

* gsheetsdb
* numpy
* pandas
* protobuf
* pyecharts
* streamlit
* streamlit_echarts
* The Python version used for this app is 3.9.5.

# Usage
You can try the tool by clicking on this link. https://capm-notsosaneexile.streamlit.app/\
If the app was put to sleep you can try to run it locally.\
Current version uses a .streamlit directory with the config and secrets files. Both being .toml format\
If you'd like to run the code on your machine you'd need to create a .streamlit directory.\
The logic between accessing data sheets should be put in secrets.toml like that:\
`[gcp_service_account]`\
`type = "service_account"`\
`project_id = "your-project-id"`\
`private_key_id = "your-private-key-id"`\
`private_key = "-----BEGIN PRIVATE KEY-----\nYour private key goes here\n-----END PRIVATE KEY-----"`\
`client_email = "your-service-account-email@your-project-id.iam.gserviceaccount.com"`\
`client_id = "your-client-id"`\
`auth_uri = "https://accounts.google.com/o/oauth2/auth"`\
`token_uri = "https://oauth2.googleapis.com/token"`\
`auth_provider_x509_cert_url = "https://www.googleapis.com/oauth2/v1/certs"`\
`client_x509_cert_url = "https://www.googleapis.com/robot/v1/metadata/x509/your-service-account-email%40your-project-id.iam.gserviceaccount.com"`\
config.toml is only for the visual configurations and can be omitted, but if you'd like to setup your own style please check the Streamlit documentation on setting up config files.
