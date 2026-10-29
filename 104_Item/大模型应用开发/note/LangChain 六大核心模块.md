### 认识 LangChain 六大核心模块

理解每个模块的职责，是高效使用 LangChain 的基础[](https://cloud.baidu.com/article/3364149)。你可以参考下表，对它们建立一个整体认知：

| 模块名称          | 核心职责                                                                        | 一句话解释                 |
| ------------- | --------------------------------------------------------------------------- | --------------------- |
| **Model I/O** | 管理大语言模型(LLM)的输入（提示词）和输出（解析）[](https://cloud.baidu.com/article/3364149)      | 应用与AI模型沟通的“翻译官”。      |
| **Retrieval** | 从外部数据源（如向量数据库）检索与问题相关的信息[](https://cloud.baidu.com/article/3364149)         | 为AI提供外部知识的“图书馆管理员”。   |
| **Chains**    | 将多个组件（模型、提示词等）按顺序组合，构建复杂的工作流[](https://cloud.baidu.com/article/3364149)     | 串联所有步骤的“流水线”。         |
| **Memory**    | 在对话或链的执行过程中，存储和传递上下文状态[](https://cloud.baidu.com/article/3364149)           | 让AI拥有“记忆”的“便签本”。      |
| **Agents**    | 让LLM自主决定执行哪些“工具”（Tools）以及按什么顺序执行[](https://cloud.baidu.com/article/3364149) | 能够自主决策和行动的“智能机器人”。    |
| **Callbacks** | 提供钩子函数，用于日志记录、监控、流式输出等[](https://cloud.baidu.com/article/3364149)           | 隐藏在幕后负责“监控和记录”的“观察员”。 |

#### 模块详解与关键子概念

- **Model I/O**：这是最基础的模块，核心是 **Prompts（提示词）**、**LLMs/Chat Models（大语言模型）** 和 **Output Parsers（输出解析器）**。它负责格式化输入给模型，并解析模型的原始输出。
    
- **Retrieval**：这是实现 RAG（检索增强生成）的基础。关键组件包括 **Document Loaders（文档加载器）**、**Text Splitters（文本分割器）**、**Embeddings（嵌入模型）** 和 **Vector Stores（向量数据库）**。
    
- **Chains**：这是LangChain的“粘合剂”，用于构建复杂逻辑[](https://cloud.baidu.com/article/3364149)。
    
    - **LLMChain**：最基础的链，组合了提示词和模型[](https://cloud.baidu.com/article/3364149)。
        
    - **Sequential Chain**：按顺序执行一系列链[](https://cloud.baidu.com/article/3364149)。
        
    - **RouterChain**：根据输入动态选择下一个要执行的链[](https://cloud.baidu.com/article/3364149)。
        
- **Memory**：用于在多次调用或对话轮次间保存状态。有 `ConversationBufferMemory`（缓存全部历史）、`ConversationSummaryMemory`（总结历史）等多种实现。
    
- **Agents**：赋予LLM使用工具的能力。Agent 的核心是**工具（Tools）** 和**决策逻辑**，它通过 ReAct（推理+行动）等框架来思考并调用工具[](https://openi.pcl.ac.cn/Lesley_god/chain/src/branch/harrison/combine-docs-parse/docs/index.rst)。
    
- **Callbacks**：提供了一种机制，让你可以在链的不同执行阶段（如开始、结束、出错时）插入自定义逻辑。