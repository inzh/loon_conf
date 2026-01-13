#!/usr/bin/env python3
"""
从 Accademia/Additional_Rule_For_Clash 仓库下载 GeositeCN.yaml
提取有效的 DOMAIN-SUFFIX 规则，保存为 GeositeCN.list
"""

import re
import urllib.request
from pathlib import Path


YAML_URL = "https://raw.githubusercontent.com/Accademia/Additional_Rule_For_Clash/main/GeositeCN/GeositeCN.yaml"
OUTPUT_FILE = "GeositeCN.list"


def download_yaml(url: str) -> str:
    """下载 YAML 文件内容"""
    with urllib.request.urlopen(url) as response:
        return response.read().decode("utf-8")


def extract_rules(content: str) -> list[str]:
    """
    从 YAML 内容中提取有效规则
    
    规则格式: - DOMAIN-SUFFIX   , domain.com    # comment
    输出格式: DOMAIN-SUFFIX,domain.com
    """
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
        
        # 跳过处理后的空行
        if line:
            rules.append(line)
    
    return rules


def main():
    print(f"正在下载: {YAML_URL}")
    content = download_yaml(YAML_URL)
    
    print("正在提取规则...")
    rules = extract_rules(content)
    
    # 写入输出文件
    output_path = Path(__file__).parent.parent / OUTPUT_FILE
    output_path.write_text("\n".join(rules) + "\n", encoding="utf-8")
    
    print(f"处理完成，共 {len(rules)} 条规则")
    print(f"输出文件: {output_path}")
    
    # 显示前 5 条规则
    print("\n前 5 条规则:")
    for rule in rules[:5]:
        print(f"  {rule}")


if __name__ == "__main__":
    main()
