#!/usr/bin/env python3
"""
从 Accademia/Additional_Rule_For_Clash 仓库下载规则文件并处理
"""

import re
import urllib.request
from pathlib import Path


BASE_URL = "https://raw.githubusercontent.com/Accademia/Additional_Rule_For_Clash/main"


def download_file(url: str) -> str:
    """下载文件内容"""
    print(f"正在下载: {url}")
    with urllib.request.urlopen(url) as response:
        return response.read().decode("utf-8")


def process_geosite_cn() -> None:
    """
    处理 GeositeCN.yaml
    
    规则格式: - DOMAIN-SUFFIX   , domain.com    # comment
    输出格式: DOMAIN-SUFFIX,domain.com
    """
    url = f"{BASE_URL}/GeositeCN/GeositeCN.yaml"
    content = download_file(url)
    
    rules = []
    for line in content.splitlines():
        # 跳过空行
        if not line.strip():
            continue
        
        # 跳过注释行（前导空格后以 # 开头）
        if line.strip().startswith("#"):
            continue
        
        # 跳过不包含 DOMAIN-SUFFIX 的行
        if "DOMAIN-SUFFIX" not in line:
            continue
        
        # 移除行尾注释
        line = re.sub(r"#.*$", "", line)
        
        # 移除前导 "- " 符号
        line = re.sub(r"^\s*-\s*", "", line)
        
        # 移除所有空格
        line = line.replace(" ", "")
        
        if line:
            rules.append(line)
    
    output_path = Path.cwd() / "GeositeCN.list"
    output_path.write_text("\n".join(rules) + "\n", encoding="utf-8")
    print(f"GeositeCN: 共 {len(rules)} 条规则 -> {output_path}")


def process_china_dns_domain() -> None:
    """
    处理 ChinaDNS_Domain.yaml
    
    规则格式: - '+.dns.cn'    # comment 或 - 'dns.114dns.com'    # comment
    输出格式: DOMAIN-SUFFIX,dns.cn
    """
    url = f"{BASE_URL}/ChinaDNS/ChinaDNS_Domain.yaml"
    content = download_file(url)
    
    rules = []
    for line in content.splitlines():
        # 跳过空行
        if not line.strip():
            continue
        
        # 跳过纯注释行（整行以 # 开头）
        if line.strip().startswith("#"):
            continue
        
        # 跳过不包含 "-" 的行
        if "-" not in line:
            continue
        
        # 提取 "-" 后面引号内的字符串
        match = re.search(r"-\s*['\"](.+?)['\"]", line)
        if not match:
            continue
        
        domain = match.group(1)
        
        # 去除 "+." 前缀
        if domain.startswith("+."):
            domain = domain[2:]
        
        rules.append(f"DOMAIN-SUFFIX,{domain}")
    
    output_path = Path.cwd() / "ChinaDNS_Domain.list"
    output_path.write_text("\n".join(rules) + "\n", encoding="utf-8")
    print(f"ChinaDNS_Domain: 共 {len(rules)} 条规则 -> {output_path}")


def process_china_dns_ip() -> None:
    """
    处理 ChinaDNS_IP.yaml
    
    规则格式: - '114.114.114.114/32'    # comment 或 - '240c::6666/64'    # comment
    输出格式: IP-CIDR,114.114.114.114/32,no-resolve 或 IP-CIDR6,240c::6666/64
    """
    url = f"{BASE_URL}/ChinaDNS/ChinaDNS_IP.yaml"
    content = download_file(url)
    
    rules = []
    for line in content.splitlines():
        # 跳过空行
        if not line.strip():
            continue
        
        # 跳过纯注释行（整行以 # 开头）
        if line.strip().startswith("#"):
            continue
        
        # 跳过不包含 "-" 的行
        if "-" not in line:
            continue
        
        # 提取 "-" 后面引号内的字符串
        match = re.search(r"-\s*['\"](.+?)['\"]", line)
        if not match:
            continue
        
        ip_cidr = match.group(1)
        
        # 判断是 IPv6 还是 IPv4
        if ":" in ip_cidr:
            # IPv6
            rules.append(f"IP-CIDR6,{ip_cidr}")
        else:
            # IPv4
            rules.append(f"IP-CIDR,{ip_cidr},no-resolve")
    
    output_path = Path.cwd() / "ChinaDNS_IP.list"
    output_path.write_text("\n".join(rules) + "\n", encoding="utf-8")
    print(f"ChinaDNS_IP: 共 {len(rules)} 条规则 -> {output_path}")


def process_global_dns_domain() -> None:
    """
    处理 GlobalDNS_Domain.yaml
    
    规则格式: - '+.dns.google'    # comment
    输出格式: DOMAIN-SUFFIX,dns.google
    """
    url = f"{BASE_URL}/GlobalDNS/GlobalDNS_Domain.yaml"
    content = download_file(url)
    
    rules = []
    for line in content.splitlines():
        # 跳过空行
        if not line.strip():
            continue
        
        # 跳过纯注释行（整行以 # 开头）
        if line.strip().startswith("#"):
            continue
        
        # 跳过不包含 "-" 的行
        if "-" not in line:
            continue
        
        # 提取 "-" 后面引号内的字符串
        match = re.search(r"-\s*['\"](.+?)['\"]", line)
        if not match:
            continue
        
        domain = match.group(1)
        
        # 去除 "+." 前缀
        if domain.startswith("+."):
            domain = domain[2:]
        
        rules.append(f"DOMAIN-SUFFIX,{domain}")
    
    output_path = Path.cwd() / "GlobalDNS_Domain.list"
    output_path.write_text("\n".join(rules) + "\n", encoding="utf-8")
    print(f"GlobalDNS_Domain: 共 {len(rules)} 条规则 -> {output_path}")


def process_global_dns_ip() -> None:
    """
    处理 GlobalDNS_IP.yaml
    
    规则格式: - '8.8.8.8/32'    # comment 或 - '2001:4860:4860::8888/128'    # comment
    输出格式: IP-CIDR,8.8.8.8/32,no-resolve 或 IP-CIDR6,2001:4860:4860::8888/128
    """
    url = f"{BASE_URL}/GlobalDNS/GlobalDNS_IP.yaml"
    content = download_file(url)
    
    rules = []
    for line in content.splitlines():
        # 跳过空行
        if not line.strip():
            continue
        
        # 跳过纯注释行（整行以 # 开头）
        if line.strip().startswith("#"):
            continue
        
        # 跳过不包含 "-" 的行
        if "-" not in line:
            continue
        
        # 提取 "-" 后面引号内的字符串
        match = re.search(r"-\s*['\"](.+?)['\"]", line)
        if not match:
            continue
        
        ip_cidr = match.group(1)
        
        # 判断是 IPv6 还是 IPv4
        if ":" in ip_cidr:
            # IPv6
            rules.append(f"IP-CIDR6,{ip_cidr}")
        else:
            # IPv4
            rules.append(f"IP-CIDR,{ip_cidr},no-resolve")
    
    output_path = Path.cwd() / "GlobalDNS_IP.list"
    output_path.write_text("\n".join(rules) + "\n", encoding="utf-8")
    print(f"GlobalDNS_IP: 共 {len(rules)} 条规则 -> {output_path}")


def process_block_http_dns_plus() -> None:
    """
    处理 BlockHttpDNSPlus_No_Resolve.yaml
    
    规则格式: - DOMAIN-KEYWORD , httpsdns    # comment
    输出格式: DOMAIN-KEYWORD,httpsdns
    """
    url = f"{BASE_URL}/BlockHttpDNSPlus/BlockHttpDNSPlus_No_Resolve.yaml"
    content = download_file(url)
    
    rules = []
    for line in content.splitlines():
        # 跳过空行
        if not line.strip():
            continue
        
        # 跳过注释行（整行以 # 开头）
        if line.strip().startswith("#"):
            continue
        
        # 跳过不包含 "-" 的行
        if "-" not in line:
            continue
        
        # 移除行尾注释
        line = re.sub(r"#.*$", "", line)
        
        # 移除前导 "- " 符号
        line = re.sub(r"^\s*-\s*", "", line)
        
        # 移除所有空格
        line = line.replace(" ", "")
        
        if line:
            rules.append(line)
    
    output_path = Path.cwd() / "BlockHttpDNSPlus.list"
    output_path.write_text("\n".join(rules) + "\n", encoding="utf-8")
    print(f"BlockHttpDNSPlus: 共 {len(rules)} 条规则 -> {output_path}")


def process_hijacking_plus() -> None:
    """
    处理 HijackingPlus.yaml
    
    规则格式: - DOMAIN-KEYWORD, xxx 或 - IP-CIDR, xxx    # comment
    输出格式: DOMAIN-KEYWORD,xxx 或 IP-CIDR,xxx,no-resolve
    """
    url = f"{BASE_URL}/HijackingPlus/HijackingPlus.yaml"
    content = download_file(url)
    
    rules = []
    for line in content.splitlines():
        # 跳过空行
        if not line.strip():
            continue
        
        # 跳过注释行（整行以 # 开头）
        if line.strip().startswith("#"):
            continue
        
        # 跳过不包含 "-" 的行
        if "-" not in line:
            continue
        
        # 移除行尾注释
        line = re.sub(r"#.*$", "", line)
        
        # 移除前导 "- " 符号
        line = re.sub(r"^\s*-\s*", "", line)
        
        # 移除所有空格
        line = line.replace(" ", "")
        
        if not line:
            continue
        
        # 对于 IP-CIDR 类型，添加 no-resolve
        if line.startswith("IP-CIDR,") and not line.endswith(",no-resolve"):
            line = f"{line},no-resolve"
        
        rules.append(line)
    
    output_path = Path.cwd() / "HijackingPlus.list"
    output_path.write_text("\n".join(rules) + "\n", encoding="utf-8")
    print(f"HijackingPlus: 共 {len(rules)} 条规则 -> {output_path}")


def main():
    print("=" * 50)
    print("开始同步规则文件")
    print("=" * 50)
    
    process_geosite_cn()
    process_china_dns_domain()
    process_china_dns_ip()
    process_global_dns_domain()
    process_global_dns_ip()
    process_block_http_dns_plus()
    process_hijacking_plus()
    
    print("=" * 50)
    print("同步完成")
    print("=" * 50)


if __name__ == "__main__":
    main()
