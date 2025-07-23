import argparse
import subprocess
import pathlib
import time
import re
import os
import shutil  # For tool checks

class BaseModule:
    """Base class for all reconnaissance modules."""
    name = "base"
    output_file = "output.txt"

    def __init__(self, target, output_dir, config=None):
        self.target = target
        self.output_dir = pathlib.Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self.config = config or {}  # For future YAML config

    def check_tool(self, tool):
        """Check if tool is available."""
        if shutil.which(tool) is None:
            print(f"[ERROR] {tool} not found. Please install it and add to PATH.")
            return False
        return True

    def run_cmd(self, cmd, outfile_path):
        """Run external command with error handling."""
        try:
            start = time.time()
            result = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=self.config.get('timeout', 300))
            if result.returncode != 0:
                print(f"[ERROR] in {self.name}: {result.stderr.strip()}")
                return False
            with open(outfile_path, 'w') as f:
                f.write(result.stdout)
            print(f"[SUCCESS] Completed {self.name} in {time.time() - start:.2f}s. Output: {outfile_path}")
            return True
        except subprocess.TimeoutExpired:
            print(f"[ERROR] Timeout in {self.name}")
            return False
        except Exception as e:
            print(f"[ERROR] Failure in {self.name}: {str(e)}")
            return False

    def execute(self):
        raise NotImplementedError("Subclasses must implement execute()")

class SubdomainModule(BaseModule):
    name = "subdomain"
    output_file = "subs.txt"

    def execute(self):
        if not self.check_tool("subfinder"):
            print("[ERROR] Install subfinder via: go install github.com/projectdiscovery/subfinder/v2/cmd/subfinder@latest")
            return False
        outfile = str(self.output_dir / self.output_file)
        cmd = f"subfinder -d {self.target} -silent -o {outfile}"
        if self.config.get('deep'): cmd += " -all"  # Example deep flag extension
        return self.run_cmd(cmd, outfile)

class PortsModule(BaseModule):
    name = "ports"
    output_file = "ports.txt"

    def execute(self):
        if not self.check_tool("naabu"):
            print("[ERROR] Install naabu via: go install github.com/projectdiscovery/naabu/v2/cmd/naabu@latest")
            return False
        outfile = str(self.output_dir / self.output_file)
        port_range = "1-1000" if self.config.get('fast') else "1-65535"
        cmd = f"naabu -host {self.target} -p {port_range} -silent -o {outfile}"
        return self.run_cmd(cmd, outfile)

class HttpProbeModule(BaseModule):
    name = "http_probe"
    output_file = "httpx.txt"

    def execute(self):
        if not self.check_tool("httpx"):
            print("[ERROR] Install httpx via: go install github.com/projectdiscovery/httpx/cmd/httpx@latest")
            return False
        outfile = str(self.output_dir / self.output_file)
        subs_file = str(self.output_dir / 'subs.txt')
        if not os.path.exists(subs_file):
            print("[INFO] Skipping HTTP probe: subs.txt not found")
            return False
        cmd = f"httpx -l {subs_file} -silent -o {outfile} -tech-detect"
        if not self.run_cmd(cmd, outfile):
            return False
        # Python equivalent for tech extraction (Windows-friendly)
        tech_file = str(self.output_dir / "tech.txt")
        try:
            with open(outfile, 'r') as f, open(tech_file, 'w') as tf:
                for line in f:
                    parts = line.split()
                    if len(parts) > 1:
                        tf.write(parts[1] + '\n')
            print(f"[SUCCESS] Tech detection saved to {tech_file}")
            return True
        except Exception as e:
            print(f"[ERROR] Tech extraction failed: {str(e)}")
            return False

class JsDiscoveryModule(BaseModule):
    name = "js_discovery"
    output_file = "endpoints.txt"

    def execute(self):
        if not self.check_tool("curl"):
            print("[ERROR] curl not found. Install curl for Windows or use native requests.")
            return False
        outfile = str(self.output_dir / self.output_file)
        httpx_file = str(self.output_dir / 'httpx.txt')
        if not os.path.exists(httpx_file):
            print("[INFO] Skipping JS discovery: httpx.txt not found")
            return False
        # Simple regex-based endpoint discovery (fetch and parse JS URLs)
        with open(httpx_file, 'r') as f:
            urls = [line.strip() for line in f if line.strip().endswith('.js')]
        endpoints = []
        for url in urls:
            try:
                response = subprocess.run(f"curl -s {url}", shell=True, capture_output=True, text=True)
                found = re.findall(r'[/\w-]+\?\w+=', response.stdout)  # Basic endpoint regex
                endpoints.extend(found)
            except:
                pass
        with open(outfile, 'w') as f:
            f.write('\n'.join(set(endpoints)))
        print(f"[SUCCESS] Found {len(endpoints)} potential endpoints")
        return bool(endpoints)

class DirBruteforceModule(BaseModule):
    name = "dir_bruteforce"
    output_file = "dirs.txt"

    def execute(self):
        if not self.check_tool("ffuf"):
            print("[ERROR] Install ffuf via: go install github.com/ffuf/ffuf/v2@latest")
            return False
        outfile = str(self.output_dir / self.output_file)
        # Customize this path to your wordlist (download from SecLists if needed)
        wordlist = "C:\\Users\\aayus\\Downloads\\common.txt"  # UPDATE THIS PATH!
        if not os.path.exists(wordlist):
            print(f"[ERROR] Wordlist not found at {wordlist}. Download one and update the path.")
            return False
        cmd = f"ffuf -u https://{self.target}/FUZZ -w {wordlist} -mc 200,301 -o {outfile} -of csv"
        return self.run_cmd(cmd, outfile)

class ParamDiscoveryModule(BaseModule):
    name = "param_discovery"
    output_file = "params.txt"

    def execute(self):
        if not self.check_tool("arjun"):
            print("[ERROR] Install arjun via: pip install arjun")
            return False
        outfile = str(self.output_dir / self.output_file)
        cmd = f"arjun -u https://{self.target} --stable -oT {outfile}"
        return self.run_cmd(cmd, outfile)

class ScreenshotModule(BaseModule):
    name = "screenshot"
    output_file = "screenshots/"  # Directory for images

    def execute(self):
        if not self.check_tool("gowitness"):
            print("[ERROR] Install gowitness via: go install github.com/sensepost/gowitness@latest")
            return False
        out_dir = str(self.output_dir / self.output_file)
        os.makedirs(out_dir, exist_ok=True)
        httpx_file = str(self.output_dir / 'httpx.txt')
        if not os.path.exists(httpx_file):
            print("[INFO] Skipping screenshots: httpx.txt not found")
            return False
        cmd = f"gowitness file -f {httpx_file} -P {out_dir} --headless"
        return self.run_cmd(cmd, f"{out_dir}/report.html")  # gowitness generates report

def generate_report(output_dir, format='md'):
    """Basic report generation with content inclusion."""
    report_file = output_dir / f"report.{format}"
    with open(report_file, 'w') as f:
        f.write("# AutoScope Report\n\n")
        for file in output_dir.glob('*.txt'):
            f.write(f"## {file.stem}\n")
            if os.path.getsize(file) == 0:
                f.write("Empty - Module Failed or Skipped\n\n")
            else:
                with open(file, 'r') as content:
                    f.write(content.read() + "\n\n")
    print(f"[INFO] Report generated: {report_file}")

def main():
    parser = argparse.ArgumentParser(description="AutoScope: Modular Recon Framework")
    parser.add_argument('-t', '--target', required=True, help="Target domain/IP or file with targets")
    parser.add_argument('--fast', action='store_true', help="Fast scan profile (limited ports, no deep enum)")
    parser.add_argument('--deep', action='store_true', help="Deep scan profile (full ports, thorough enum)")
    parser.add_argument('--resume', action='store_true', help="Resume from existing output (TODO: implement)")
    parser.add_argument('--only-subdomains', action='store_true', help="Run only subdomain enumeration")
    parser.add_argument('--no-dirs', action='store_true', help="Skip directory bruteforce")
    parser.add_argument('--no-screenshots', action='store_true', help="Skip screenshotting")
    parser.add_argument('--report', choices=['md', 'json', 'csv'], default='md', help="Report format")
    parser.add_argument('--output', default='output', help="Base output directory")
    args = parser.parse_args()

    if args.fast and args.deep:
        print("[ERROR] Cannot use --fast and --deep together")
        return

    config = {'fast': args.fast, 'deep': args.deep, 'timeout': 60 if args.fast else 300}
    output_dir = pathlib.Path(args.output) / args.target.replace('.', '_')  # Sanitize for folder name

    modules = [
        SubdomainModule(args.target, output_dir, config),
        PortsModule(args.target, output_dir, config),
        HttpProbeModule(args.target, output_dir, config),
        JsDiscoveryModule(args.target, output_dir, config),
        DirBruteforceModule(args.target, output_dir, config),
        ParamDiscoveryModule(args.target, output_dir, config),
        ScreenshotModule(args.target, output_dir, config)
    ]

    if args.only_subdomains:
        modules = [m for m in modules if isinstance(m, SubdomainModule)]
    if args.no_dirs:
        modules = [m for m in modules if not isinstance(m, DirBruteforceModule)]
    if args.no_screenshots:
        modules = [m for m in modules if not isinstance(m, ScreenshotModule)]

    for module in modules:
        print(f"[INFO] Executing module: {module.name}")
        module.execute()

    generate_report(output_dir, args.report)
    print("[SUCCESS] AutoScope scan completed!")

if __name__ == "__main__":
    main()
