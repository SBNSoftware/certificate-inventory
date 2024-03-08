The purpose of this document is to provide a guide for updating the inventory list of certificates, including their corresponding expiration dates, for various hosts used by the DAQ

Note: For security reasons, it's important to protect both the input file to be analyzed and the results using Single Sign-On (SSO) and to avoid storing this information on publicly accessible servers.

DAQ/DQM is using various databases and web services protected by the Secure Socket Layer (SSL) protocol, which uses SSL certificates. SSL certificates are issued for a fixed duration and can abruptly expire, causing service outages. To address this issue, the `Certificate Inventory Tool` was created. This tool is a Python3 program that takes two arguments: the input file name with a list of URIs to be analyzed for expiring certificates and the name of the output file. The output file will contain a table in Markdown format listing the original URIs along with their certificate names and expiration dates.

Furthermore, for this tool to be beneficial, it's important to periodically review and update the input file, and rerun the `Certificate Inventory Tool` so that the certificate list stays current. A general recommendation is to do this once every year or when a new SSL-protected service not mentioned in the input list is identified. Additionally, it's advisable to perform these actions preceding and following the expiration date of any certificate being monitored.

The example of the input file containing the list of URIs queried for their certificate expiration is given below. Please note that the tool supports protocols specified in examples and may require a code change to accommodate other protocols.

Example:
````txt
https://yahoo.com
https://github.com
#https://localhost
#https://localhost:443/
#mongodb://localhost:2701/
#postgres://localhost:5432/
#file:///path/to/file-ca.pem
#file:///path/to/file-client-cert.pem
````

The output produced by the `Certificate Inventory Tool` is given below and is a table with four columns: CN Name | CA Name | Expiration Date | Host.

Example:
````txt
CN Name | CA Name | Expiration Date | Host
--- | --- | --- | ---
yahoo.com | DigiCert SHA2 High Assurance Server CA | 2024-03-20 | https://yahoo.com
github.com | DigiCert TLS Hybrid ECC SHA384 2020 CA1 | 2024-03-14 | https://github.com
````

*CN Name* (Common Name): This column represents the Common Name associated with the SSL certificate. The Common Name typically identifies the host or domain for which the certificate is issued.

*CA Name* (Certificate Authority Name): In this column, the Certificate Authority (CA) Name is listed. The CA is the entity that issues the SSL certificate. It is responsible for verifying the identity of the certificate holder and endorsing the certificate.

*Expiration Date*: This column displays the expiration date of the SSL certificate. SSL certificates have a validity period, and this date signifies when the certificate will expire. Regular monitoring is essential to prevent service disruptions.

*Host*: The Host column contains the names or URLs of the various hosts or domains for which the SSL certificates are issued. It identifies the specific entities covered by the certificates listed in the inventory.


The updated certificate inventory can be produced using the following steps:

1. SSH into the host/server from which all URIs that require inventory are accessible.
2. Clone this git repository into an empty directory.
3. Setup and verify python3 from UPS using the command `setup python v3_9_13`.
4. Change directory into the `certificate-inventory` directory and `source create_venv.sh` script, which creates a new virtual Python3 environment and activates it.
5. Update the `input_hosts.txt` file to contain a complete list of URIs to be analyzed for their certificate expiration.
6. Run the `run_certificate_inventory.py`` program using the command `python3 run_certificate_inventory.py -i input_hosts.txt -o certificate_inventory.md`.
7. Finally, upload both the `input_hosts.txt` and `certificate_inventory.md` files to the server protected by SSO authentication. This step is important.
