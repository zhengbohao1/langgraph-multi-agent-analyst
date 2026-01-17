# ──────────────────────────────────────────────
# 节点函数：保存 Markdown 报告到文件
# ──────────────────────────────────────────────
import os
from datetime import datetime
from pathlib import Path
from typing import Optional

from langgraph.types import Command

from app.agents.data_analyst_agent.state import AnalystState


async def save_markdown_reports_node1(state: AnalystState) :
    """
    保存三个分析模块的 Markdown 报告到本地文件。
    每个报告保存为独立的 .md 文件，文件名带时间戳和模块标识。

    保存路径建议：可以配置在环境变量或 state 中，这里默认使用当前工作目录下的 reports/ 子目录。
    """
    print("💾 执行 Markdown 报告保存节点...")

    # 定义保存目录（可改为配置项或环境变量）
    output_dir = Path("reports")
    output_dir.mkdir(parents=True, exist_ok=True)

    # 生成时间戳，用于文件名唯一性（格式：YYYYMMDD_HHMMSS）
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    # 三个模块的 Markdown 内容字段（根据你的 state 结构调整）
    report={
        "module": "statistical_analysis",
        "content": state["statistical_result"],
        "prefix": "统计分析报告"
    }

    content = report["content"]
    print(f"待保存内容为：{content}")

    # 生成文件名：prefix_时间戳.md
    filename = f"{report['prefix']}_{timestamp}.md"
    filepath = output_dir / filename

    try:
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(content)
        print(f"✓ 已保存：{filepath}")
    except Exception as e:
        print(f"✗ 保存 {report['prefix']} 失败：{str(e)}")


    print(f"文件已成功保存至{filename}")
    return Command(update={"saved_report_paths":[str(filepath)]})

async def save_markdown_reports_node2(state: AnalystState):
    """
    保存三个分析模块的 Markdown 报告到本地文件。
    每个报告保存为独立的 .md 文件，文件名带时间戳和模块标识。

    保存路径建议：可以配置在环境变量或 state 中，这里默认使用当前工作目录下的 reports/ 子目录。
    """
    print("💾 执行 Markdown 报告保存节点...")

    # 定义保存目录（可改为配置项或环境变量）
    output_dir = Path("reports")
    output_dir.mkdir(parents=True, exist_ok=True)

    # 生成时间戳，用于文件名唯一性（格式：YYYYMMDD_HHMMSS）
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    # 三个模块的 Markdown 内容字段（根据你的 state 结构调整）

    report={
        "module": "trend_prediction",
        "content": state["trend_result"],
        "prefix": "趋势预测报告"
    }


    content = report["content"]
    print(f"待保存内容为：{content}")

    # 生成文件名：prefix_时间戳.md
    filename = f"{report['prefix']}_{timestamp}.md"
    filepath = output_dir / filename

    try:
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(content)
        print(f"✓ 已保存：{filepath}")
    except Exception as e:
        print(f"✗ 保存 {report['prefix']} 失败：{str(e)}")

    print(f"文件已成功保存至{filename}")
    return Command(update={"saved_report_paths": [str(filepath)]})

async def save_markdown_reports_node3(state: AnalystState) :
    """
    保存三个分析模块的 Markdown 报告到本地文件。
    每个报告保存为独立的 .md 文件，文件名带时间戳和模块标识。

    保存路径建议：可以配置在环境变量或 state 中，这里默认使用当前工作目录下的 reports/ 子目录。
    """
    print("💾 执行 Markdown 报告保存节点...")

    # 定义保存目录（可改为配置项或环境变量）
    output_dir = Path("reports")
    output_dir.mkdir(parents=True, exist_ok=True)

    # 生成时间戳，用于文件名唯一性（格式：YYYYMMDD_HHMMSS）
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    report = {
        "module": "anomaly_detection",
        "content": state["anomaly_result"],
        "prefix": "异常检测报告"
    }

    content = report["content"]
    print(f"待保存内容为：{content}")

    # 生成文件名：prefix_时间戳.md
    filename = f"{report['prefix']}_{timestamp}.md"
    filepath = output_dir / filename

    try:
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(content)
        print(f"✓ 已保存：{filepath}")
    except Exception as e:
        print(f"✗ 保存 {report['prefix']} 失败：{str(e)}")

    print(f"文件已成功保存至{filename}")
    return Command(update={"saved_report_paths": [str(filepath)]})