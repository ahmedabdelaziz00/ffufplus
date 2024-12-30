import subprocess
import argparse
import logging

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def run_ffuf(domain_name, wordlist_path, filter_lines, method, extensions, timeout, threads):
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
        "https://{}/cgi-bin/FUZZ.cgi",  # ?FUZZ=%26id%26 => rce here
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
            "-t", str(threads),
            "-e", extensions
        ]

        if filter_lines:
            # Join filter lines into a single comma-separated string
            command.extend(["-fl", ",".join(map(str, filter_lines))])

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
        run_ffuf(domain_name, wordlist_path, filter_lines, "POST", extensions, timeout, threads)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="\n\nA utility tool to execute ffuf with multiple URL patterns.",
        epilog="\nExample usage:\n  python script.py -d example.com -w wordlist.txt -fl 1,3 -t 50 -X POST\n  python script.py -d example.com -w wordlist.txt\n\nUse -h for this help message.",
        formatter_class=argparse.RawTextHelpFormatter
    )
    parser.add_argument("-d", "--domain", required=True, help="Target domain name")
    parser.add_argument("-w", "--wordlist", required=True, help="Path to the wordlist")
    parser.add_argument("-fl", "--filterline", type=lambda x: list(map(int, x.split(','))), help="Comma-separated line numbers to filter (e.g., 1,3)")
    parser.add_argument("-X", "--method", default="GET", help="HTTP request method (default: GET)")
    parser.add_argument("-e", "--extensions", default=".php,.json,.asp,.aspx,.jsp,.bak,.old", help="Comma-separated list of extensions to fuzz (default: common extensions)")
    parser.add_argument("-t", "--threads", type=int, default=75, help="Number of threads (default: 75)")
    parser.add_argument("--timeout", type=int, default=60, help="Timeout in seconds for each ffuf command (default: 60)")

    args = parser.parse_args()

    run_ffuf(args.domain, args.wordlist, args.filterline, args.method, args.extensions, args.timeout, args.threads)
