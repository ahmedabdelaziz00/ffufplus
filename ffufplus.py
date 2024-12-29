import subprocess
import argparse
import logging

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def run_ffuf(domain_name, wordlist_path, filter_line, method, extensions, timeout):
    # List of ffuf URL patterns
    patterns = [
        "https://{}/FUZZ",
        "https://{}//FUZZ",
        "https://{}/.FUZZ",
        "https://{}/_FUZZ",
        "https://{}/-/FUZZ",
        "https://{}/_/FUZZ",
        "https://{}///FUZZ",
        "https://{}/;/FUZZ",
        "https://{}/.;/FUZZ",
        "https://{}/..;/FUZZ",
        "https://{}//.FUZZ",
        "https://{}/./FUZZ",
        "https://{}/FUZZ%09",
        "https://{}/FUZZ%20",
        "https://{}/cgi-bin/FUZZ.cgi",  #    ?FUZZ=%26id%26 => rce here
        "https://{}/%2e/FUZZ",
        "https://{}/;FUZZ",
        "https://{}/FUZZ/.",
        "https://{}//FUZZ//",
        "https://{}/./FUZZ/./",
        "https://{}/FUZZ..;/"
    ]

    for pattern in patterns:
        url = pattern.format(domain_name)
        command = [
            "ffuf", 
            "-u", url, 
            "-w", wordlist_path,
            "-t", "75",
            "-e", extensions
        ]

        if filter_line is not None:
            command.extend(["-fl", str(filter_line)])

        if method:
            command.extend(["-X", method])

        try:
            logger.info(f"Running Command: {' '.join(command)}")
            subprocess.run(command, check=True, timeout=timeout)
        except subprocess.CalledProcessError as e:
            logger.error(f"[ERROR] Command failed: {e}")
        except subprocess.TimeoutExpired:
            logger.error(f"[ERROR] Command timed out: {url}")

    # Repeat with POST method if no specific method was provided
    if method == "GET":
        logger.info("Repeating with POST method.")
        run_ffuf(domain_name, wordlist_path, filter_line, "POST", extensions, timeout)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="\n\nA utility tool to execute ffuf with multiple URL patterns.",
        epilog="\nExample usage:\n  python script.py -d example.com -w wordlist.txt -fl 10 -X POST\n  python script.py -d example.com -w wordlist.txt\n\nUse -h for this help message.",
        formatter_class=argparse.RawTextHelpFormatter
    )
    parser.add_argument("-d", "--domain", required=True, help="Target domain name")
    parser.add_argument("-w", "--wordlist", required=True, help="Path to the wordlist")
    parser.add_argument("-fl", "--filterline", type=int, help="Filter line number (optional)")
    parser.add_argument("-X", "--method", default="GET", help="HTTP request method (default: GET)")
    parser.add_argument("-e", "--extensions", default=".php,.json,.asp,.aspx,.jsp,.bak,.old", help="Comma-separated list of extensions to fuzz (default: common extensions)")
    parser.add_argument("--timeout", type=int, default=60, help="Timeout in seconds for each ffuf command (default: 60)")

    args = parser.parse_args()

    run_ffuf(args.domain, args.wordlist, args.filterline, args.method, args.extensions, args.timeout)
