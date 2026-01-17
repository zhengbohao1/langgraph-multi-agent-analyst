from __future__ import annotations

from langchain.agents import create_agent
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_core.tools import tool
from typing import Dict, Any, Optional

from langchain_openai import ChatOpenAI
from sqlalchemy import create_engine, text, inspect
import pandas as pd
import re

from app.models.LLM_MODEL import ModelInstances

# 固定写死的 db_url（本地 MySQL，数据库名叫 agent）
FIXED_DB_URL = "mysql+mysqlconnector://agent_user:xijn389m3ji4n2@localhost:3306/agent?charset=utf8mb4"

# ──────────────────────────────────────────────
# 1. 获取当前数据库所有表结构（以字符串形式返回）
# ──────────────────────────────────────────────
def get_database_schema() -> str:
    """
    连接指定数据库，读取所有表名及其字段、类型、主键、外键等信息，
    返回适合塞进Prompt的结构化文本。
    """
    try:
        db_url=FIXED_DB_URL
        engine = create_engine(db_url)
        inspector = inspect(engine)

        schema_str = "当前数据库表结构如下（请严格根据以下信息生成SQL，不要臆想不存在的表或字段）：\n\n"

        for table_name in inspector.get_table_names():
            schema_str += f"表名: {table_name}\n"
            schema_str += "字段信息:\n"

            columns = inspector.get_columns(table_name)
            for col in columns:
                col_type = str(col["type"])
                nullable = "可为空" if col["nullable"] else "不可为空"
                default = f"默认值: {col['default']}" if col.get("default") else ""
                pk = "【主键】" if col.get("primary_key") else ""
                schema_str += f"  - {col['name']:20} {col_type:15} {nullable} {default} {pk}\n"

            # 主键（复合主键也会显示）
            pks = inspector.get_pk_constraint(table_name)
            if pks and pks["constrained_columns"]:
                schema_str += f"主键: {', '.join(pks['constrained_columns'])}\n"

            # 外键（比较重要，强烈建议包含）
            fks = inspector.get_foreign_keys(table_name)
            if fks:
                schema_str += "外键:\n"
                for fk in fks:
                    schema_str += f"  - {fk['constrained_columns']} → {fk['referred_table']}.{fk['referred_columns']}\n"

            schema_str += "\n"

        if not inspector.get_table_names():
            schema_str += "(该数据库中没有任何表)\n"
        print(f"数据库中的表结构如下：{schema_str.strip()}")
        return schema_str.strip()

    except Exception as e:
        return f"获取数据库结构失败: {str(e)}"


# ──────────────────────────────────────────────
# 2. 利用LLM生成SQL的提示词模板 + 后处理提取 <sql> 标签内容
# ──────────────────────────────────────────────
SQL_GENERATION_PROMPT_TEMPLATE = """\
你是一个专业的SQL编写专家。请你根据用户具体的数据库结构和查询需求，生成正确的、可以直接执行的SQL语句。

要求：
1. 只输出SQL语句，不要包含任何解释、markdown、```sql 等标记
2. 必须用 <sql> 和 </sql> 标签包裹完整SQL语句
3. 如果需求不清晰或无法实现，返回 <sql>  无法生成有效SQL，请补充更多信息 </sql>
4. 使用标准SQL语法，优先使用明确的JOIN而不是隐式连接
5. 注意字段名大小写敏感性（根据实际表结构）
6. 如果需要分页、排序，请合理添加（但默认不加limit，除非用户明确要求）
7. 日期使用标准格式，参数化写法优先（但这里只需写纯SQL）

示例1：
用户：帮我分析我们公司的业绩
分析：用户没有明确业绩归属于哪张表，且没有相似标题的表，也没有明确时间范围，判定为需求模糊不清晰
返回：<sql>  无法生成有效SQL，请补充更多信息 </sql>

示例2：
用户：帮我查询user表中zbh用户的密码与电话
分析：需求明确，表名已指定，查询依据已指定。
返回：<sql>SELECT password, mobile FROM user WHERE username = 'zbh222'</sql>

现在直接输出：
"""

USER_INPUT="""\
请帮我处理数据库查询
{db_schema}

我的需求如下：
{user_query}

"""


def generate_sql_with_schema(
    user_query: str
) -> Optional[str]:
    """
    调用LLM生成SQL，并尝试提取 <sql>...</sql> 中的内容

    参数 llm_call_function 是一个函数，签名示例：
    def call_llm(messages, model, temperature) -> str:
        ...
        return response_content
    """
    schema_text = get_database_schema()

    user_prompt = USER_INPUT.format(
        db_schema=schema_text,
        user_query=user_query
    )

    # 你需要替换成自己实际的LLM调用方式
    # 这里仅为示意
    llm=ModelInstances.leader_llm
    # db_agent=create_agent(
    #     model=llm,
    #     tools=[]
    # )
    messages = [SystemMessage(content=SQL_GENERATION_PROMPT_TEMPLATE),HumanMessage(content=user_prompt)]
    raw_response=llm.invoke(messages)

    # 提取 <sql> ... </sql> 中的内容
    pattern = r'<sql>(.*?)</sql>'
    match = re.search(pattern, raw_response.content, re.DOTALL)
    if match:
        sql = match.group(1).strip()
        # 简单清理一下常见的残留标记
        sql = re.sub(r'^```sql\s*|\s*```$', '', sql.strip())
        return sql
    else:
        # 没找到标签，尝试整段当作SQL（但不推荐）
        return None  # 或者根据需要抛异常 / 返回 raw_response


# ──────────────────────────────────────────────
# 3. 最终对外暴露的 Tool 函数（最推荐放在LangChain / LlamaIndex / AutoGen / smolagents 等框架中使用）
# ──────────────────────────────────────────────
@tool
def _query_database(
    question: str,
    params: Optional[Dict[str, Any]] = None,
) -> Dict[str, Any]:
    """
    用于自然语言查询本地固定的 MySQL 数据库（数据库名：agent）。

    功能：
    - 根据用户用自然语言描述的需求，自动生成并执行对应的 SQL 查询
    - 数据库连接已固定，无需用户提供 db_url
    - 仅能查询 users 数据库中的表

    重要约束：
    - 如果用户问题中没有明确或可推断出要查询哪个表，必须返回 success=false，并提示用户提供表名
    - 不要臆造表名、字段名，必须基于实际数据库结构生成 SQL

    输入示例：
    {
      "question": "查询最近注册的10个用户的信息，包括用户名和注册时间",
      "params": {}           // 可选，用于未来参数化（目前通常为空）
    }

    返回格式（始终为 dict）：
    {
      "success": bool,                  // 是否成功执行并返回数据
      "sql": str | null,                // 生成并执行的 SQL 语句
      "columns": list[str],             // 返回的列名（已规范化为小写下划线风格）
      "rows": list[dict],               // 查询结果，每行一个 dict
      "error": str | null,              // 错误信息（成功时为 null）
      "message": str                    // 简要说明或错误提示
    }

    使用注意：
    - 当 success=false 时，请在 message 中清晰说明原因（尤其是缺少表名的情况）
    - 返回的数据已做列名规范化处理（小写、下划线）
    """
    result = {"success": False, "sql": None, "columns": [], "rows": [], "error": None, "message": ""}

    try:
        # Step 1: 用LLM生成SQL
        generated_sql = generate_sql_with_schema(
            user_query=question
        )

        if generated_sql == "无法生成有效SQL，请补充更多信息":
            result["error"] = "无法生成有效SQL，请补充更多信息"
            result["message"] = "未能从模型输出中提取到SQL"
            return result

        result["sql"] = generated_sql

        # Step 2: 执行SQL
        db_url=FIXED_DB_URL
        engine = create_engine(db_url)
        with engine.connect() as conn:
            df = pd.read_sql(text(generated_sql), conn, params=params or {})

        # 规范化列名（可选，但推荐）
        df.columns = [
            str(c).strip().lower().replace(" ", "_").replace("-", "_")
            for c in df.columns
        ]

        result["columns"] = list(df.columns)
        result["rows"] = df.to_dict(orient="records")
        if len(result["rows"]) == 0:
            result["success"] = False
            result["message"] = f"查询失败，不是sql问题，而是数据库中没有符合用户查询的信息"
        else:
            result["success"] = True
            result["message"] = f"查询成功，返回 {len(result['rows'])} 条记录"

    except Exception as e:
        result["error"] = str(e)
        result["message"] = "执行SQL时发生错误"

    return result

if __name__ == "__main__":
    print(_query_database(question="请帮我分析最近一周的fact_order_summary汇总情况"))