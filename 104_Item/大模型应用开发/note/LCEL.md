 **LCEL（LangChain Expression Language，LangChain 表达式语言）**。

LCEL 是 LangChain 框架中用于**声明式地构建复杂链（Chain）**的一种语法。它让你能用简单的 `|` 管道运算符，像搭积木一样把各种组件（模型、提示词、解析器等）串联起来，形成一个可运行的计算图。

---

### 1. 核心思想：管道运算符 `|`

LCEL 最直观的特点就是使用 `|` 符号。它的工作方式类似于 Unix 管道：**左边对象的输出，会作为右边对象的输入**。

**基础示例：**
```python
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_openai import ChatOpenAI

model = ChatOpenAI(model="gpt-3.5-turbo")
prompt = ChatPromptTemplate.from_template("用一句话解释：{topic}")
parser = StrOutputParser()

# LCEL 链：用 | 串联
chain = prompt | model | parser

# 调用链
result = chain.invoke({"topic": "黑洞"})
print(result)  # 输出：黑洞是时空曲率极大、连光都无法逃逸的天体。
```

在这个例子中，数据流是这样的：
1. `{"topic": "黑洞"}` 传入 `prompt`，生成 `PromptValue`。
2. `PromptValue` 传入 `model`，生成 `ChatMessage`。
3. `ChatMessage` 传入 `parser`，提取出内容字符串。

---

### 2. 为什么使用 LCEL？（核心优势）

-   **声明式与可读性**：代码直观反映业务逻辑，容易理解和维护。
-   **“一切皆为 Runnable”**：所有 LCEL 组件（模型、提示词、检索器、甚至其他链）都实现了 `Runnable` 接口，保证了接口的统一性。
-   **自动支持同步/异步/批量/流式**：用 LCEL 构建的链，自动支持 `.invoke()`（同步）、`.ainvoke()`（异步）、`.batch()`（批量）和 `.stream()`（流式输出），无需额外编写代码。
-   **内置并行执行**：如果链中有多个独立分支，LCEL 会自动并行执行以提升效率。
-   **可观察性**：与 LangSmith 无缝集成，方便调试和追踪。

---

### 3. 常用组件与操作符

除了基础的 `|`，LCEL 还提供了丰富的内置方法：

| 方法/操作符 | 作用 | 示例 |
| :--- | :--- | :--- |
| **`|` (管道)** | 将前一个输出传递给后一个输入 | `prompt \| model` |
| **`.bind()`** | 给模型绑定额外参数（如 `temperature`） | `model.bind(temperature=0.2)` |
| **`.with_config()`** | 配置运行时的元数据（如标签、回调） | `chain.with_config({"run_name": "MyChain"})` |
| **`.with_retry()`** | 为链添加重试逻辑 | `chain.with_retry(stop_after_attempt=3)` |
| **`.with_fallbacks()`** | 主链失败时，使用备用链 | `chain.with_fallbacks([backup_chain])` |
| **`RunnableParallel`** | 并行运行多个分支（可用字典语法） | `{"summary": chain1, "keywords": chain2}` |
| **`RunnablePassthrough`** | 透传数据，不修改，常用于保留上下文 | `RunnablePassthrough()` |
| **`RunnableLambda`** | 将任意 Python 函数包装成 LCEL 组件 | `RunnableLambda(lambda x: x["text"])` |

---

### 4. 进阶模式实战

#### 模式一：多分支并行处理
当你需要同时对输入进行摘要和关键词提取时，可以并行执行：

```python
from langchain_core.runnables import RunnableParallel

chain = RunnableParallel({
    "summary": prompt_summary | model | parser,
    "keywords": prompt_keywords | model | parser,
})

# 一次输入，两个分支并行执行
result = chain.invoke({"text": "一篇长文章..."})
print(result["summary"])
print(result["keywords"])
```

#### 模式二：在中间步骤保留原始输入（使用 `RunnablePassthrough`）
当后续步骤需要同时用到“原始输入”和“中间结果”时：

```python
from langchain_core.runnables import RunnablePassthrough

# 先翻译成英文，再根据英文结果和原始中文进行润色
chain = (
    {"original": RunnablePassthrough(), "translated": translate_chain}
    | polish_prompt
    | model
    | parser
)

# 此时 polish_prompt 可以同时访问 original 和 translated
```

#### 模式三：条件分支（动态选择子链）
使用 `RunnableBranch` 根据条件选择不同的处理路径：

```python
from langchain_core.runnables import RunnableBranch

branch_chain = RunnableBranch(
    (lambda x: "紧急" in x["text"], urgent_chain),  # 条件1
    (lambda x: len(x["text"]) < 10, short_chain),   # 条件2
    default_chain                                   # 默认
)
```

#### 模式四：添加记忆（ConversationBufferMemory）
结合 `RunnableWithMessageHistory` 实现多轮对话：

```python
from langchain_core.runnables.history import RunnableWithMessageHistory

chain_with_history = RunnableWithMessageHistory(
    base_chain,
    get_session_history,  # 用于根据 session_id 获取历史记录的函数
    input_messages_key="input",
    history_messages_key="history"
)
```

---

### 5. LCEL 与 传统 Chain 的区别

| 特性 | 传统 Chain（如 `LLMChain`） | LCEL |
| :--- | :--- | :--- |
| **语法风格** | 面向对象，需继承 `Chain` 类 | 声明式，使用 `\|` 管道 |
| **灵活性** | 较低，改动需修改类结构 | 极高，可随意组合、替换组件 |
| **流式支持** | 部分支持，实现复杂 | **原生、全面支持** |
| **并行执行** | 需手动实现 | 自动并行处理分支 |
| **LangSmith 追踪** | 需要额外配置 | 开箱即用，细粒度追踪 |

---

### 6. 常见陷阱与注意点

-   **输入/输出类型要匹配**：确保前一个组件的输出类型能被后一个组件接受。例如，`model` 输出是 `BaseMessage`，如果直接传给 `StrOutputParser` 没问题，但传给某些需要字典的组件就会报错。
-   **不要在 `RunnableLambda` 中做耗时操作**：它会阻塞事件循环，影响异步性能。若必须使用，考虑用 `RunnableLambda(..., afunc=async_func)` 提供异步版本。
-   **流式输出时避免使用 `RunnableLambda`**：除非你明确处理了逐块（streaming chunk）逻辑，否则它会破坏流式特性。

---

### 7. 总结一句话

**LCEL 是 LangChain 的“万能胶水”**，它用管道语法将提示词、模型、解析器等组件封装成一个统一的 `Runnable` 接口，让你的代码更简洁、更灵活，同时免费获得流式、异步、并行和可观测性等高级能力。

---
