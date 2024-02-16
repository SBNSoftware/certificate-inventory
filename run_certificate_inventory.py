import ssl
import socket
from datetime import datetime
from urllib.parse import urlparse
import OpenSSL.crypto
import argparse

def process_certificate(cert_bin, file_type):
    x509 = OpenSSL.crypto.load_certificate(file_type, cert_bin)
    issuer = x509.get_issuer()
    subject = x509.get_subject()
    cn_name = subject.CN if hasattr(subject, "CN") else None
    ca_name = issuer.CN if hasattr(issuer, "CN") else issuer.O
    expiration_date = datetime.strptime(
        x509.get_notAfter().decode("ascii"), "%Y%m%d%H%M%SZ"
    )
    return cn_name, ca_name, expiration_date


def get_certificate(host, port):
    #context = ssl.create_default_context()
    context = ssl._create_unverified_context()
    conn = context.wrap_socket(socket.socket(socket.AF_INET), server_hostname=host)
    conn.settimeout(5.0)

    try:
        conn.connect((host, port))
        cert_bin = conn.getpeercert(True)
        return process_certificate(cert_bin, OpenSSL.crypto.FILETYPE_ASN1)
    except Exception as e:
        print(f"Error retrieving SSL certificate for {host}:{port} - {e}")
        return None, None, None
    finally:
        conn.close()


def parse_input_line(line):
    if line.startswith("https://"):
        url = urlparse(line)
        host = url.hostname
        port = url.port if url.port else 443
        return get_certificate(host, port)
    elif line.startswith("mongodb://"):
        parts = line.split("/")
        netloc = parts[2]
        host, _, port = netloc.partition(":")
        if not port:
            port = "27017"
        return get_certificate(host, int(port))
    elif line.startswith("postgres://"):
        parts = line.split("/")
        netloc = parts[2]
        host, _, port = netloc.partition(":")
        if not port:
            port = "5432"
        return get_certificate(host, int(port))
    elif line.startswith("file://"):
        file_path = line[7:]
        if file_path.lower().endswith(".pem"):
            with open(file_path, "r") as file:
                cert_data = file.read()
                return process_certificate(cert_data, OpenSSL.crypto.FILETYPE_PEM)
        else:
            return None, None, None
    else:
        host, port = line.split(",")
        return get_certificate(host, int(port))


def main(input_file, output_file):
    hosts = []
    with open(input_file, "r") as file:
        for line in file:
            line = line.split("#")[0].strip()
            if line:
                hosts.append(line)

    certificates = []
    for host in hosts:
        cn_name, ca_name, expiration_date = parse_input_line(host)
        if cn_name and ca_name and expiration_date:
            certificates.append((cn_name, ca_name, expiration_date, host))

    certificates.sort(key=lambda x: x[1])

    md_table = "CN Name | CA Name | Expiration Date | Host\n--- | --- | --- | ---\n"
    for cn_name, ca_name, expiration_date, host in certificates:
        md_table += (
            f"{cn_name} | {ca_name} | {expiration_date.strftime('%Y-%m-%d')} | {host}\n"
        )

    with open(output_file, "w") as md_file:
        md_file.write(md_table)
        print(md_table)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Generate a markdown table of SSL certificate details."
    )
    parser.add_argument(
        "-i",
        "--input",
        default="input_hosts.txt",
        help="Input file containing host details.",
    )
    parser.add_argument(
        "-o",
        "--output",
        default="certificate_inventory.md",
        help="Output markdown file for certificate details.",
    )
    args = parser.parse_args()

    main(args.input, args.output)

