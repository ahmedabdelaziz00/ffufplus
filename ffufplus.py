import subprocess
import argparse

def run_ffuf(domain_name, wordlist_path, filter_line, method):
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
        "https://{}//.FUZZ",
        "https://{}/./FUZZ",
    ]

    for pattern in patterns:
        url = pattern.format(domain_name)
        command = [
            "ffuf", 
            "-u", url, 
            "-w", wordlist_path
        ]

        if filter_line is not None:
            command.extend(["-fl", str(filter_line)])

        if method:
            command.extend(["-X", method])

        try:
            print("\n===============================")
            print(f"Running Command:")
            print(f"{' '.join(command)}")
            print("===============================\n")
            subprocess.run(command, check=True)
        except subprocess.CalledProcessError as e:
            print(f"\n[ERROR] Failed to execute command:\n{e}\n")

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

    args = parser.parse_args()

    run_ffuf(args.domain, args.wordlist, args.filterline, args.method)
