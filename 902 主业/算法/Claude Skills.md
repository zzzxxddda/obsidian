

---

## 🧠 核心概念：Claude Skills (Computer Use / Tool Use)

### 1. 知识定位 (Semantic Network)

- **核心定义**：一套允许 Claude 模型通过外部定义的函数接口（Tools）或直接通过模拟人类 UI 操作（Computer Use）来与外界交互的技术协议。
    
- **知识坐标**：它是 Agent 架构中的 **“执行器官 (Actuators)”**。
    
    - **上位概念**：函数调用 (Function Calling)、外挂能力。
        
    - **区别在于**：传统的 Tool Use 是通过 API 传数据；而 Claude 的 **Computer Use** 是通过“看”屏幕截图并“移动”鼠标，像真人一样操作任何软件。
        

### 2. 深度理解 (Concept & Logic)

- **底层原理**：**视觉-指令闭环 (Vision-Action Loop)**。
    
    Claude 不再仅仅处理文本，它会将屏幕截图作为视觉输入，识别 UI 元素（按钮、输入框），并计算出坐标，生成类似于 `mouse_click(x, y)` 或 `key_combination("ctrl+c")` 的指令。
    
- **关键特征**：
    
    1. **通用性**：不需要为每个软件写 API，只要有图形界面，它就能学着用。
        
    2. **多模态融合**：将推理能力（LLM）与空间理解能力（Vision）实时对齐。
        
    3. **结构化输出**：模型会严格按照特定的 JSON 格式输出指令，以便后台环境执行。
        

### 3. 执行指南 (Procedural Steps)

> **触发场景**：你需要 Claude 帮你填写一张复杂的网页表单，或者在 Excel 和 PPT 之间搬运数据。

1. **Step 1：定义能力 (Definition)**
    
    开发者向 Claude 声明可选的技能列表（如：`get_weather`, `screenshot`, `type_text`）。
    
2. **Step 2：意图识别 (Selection)**
    
    用户输入需求，Claude 判断现有知识不够，需要调用特定的“技能”。
    
3. **Step 3：参数构造 (Call)**
    
    Claude 输出一段符合定义的指令（JSON 格式）。
    
    > `{"action": "mouse_click", "coordinate": [450, 320]}`
    
4. **Step 4：环境反馈 (Result)**
    
    后台执行操作，并将结果（新截图或 API 返回值）回传给 Claude。Claude 根据结果决定下一步。
    

- **操作要点**：**“思维链 (CoT)”**。在执行复杂 Skills 之前，Claude 会先写下思考过程，确保每一步操作都有理有据。
    

### 4. 视觉锚点 (Dual Coding)

- **视觉比喻**：**“远程桌面背后的影子操盘手”**。
    
    想象你在用远程桌面办公。你不需要亲自动手，而是对着麦克风说：“帮我把这张发票的信息填进财务系统。”
    
    - **Claude Skills**：就像一个坐在屏幕另一端的隐形助手。他能看到你屏幕上的所有像素，能像你一样移动鼠标。他不是在破解代码，而是在“操作”软件。
        
- **逻辑结构图**：
    
    Plaintext
    
    ```
    用户指令: "帮我订一张 2 点的电影票"
        ↓
    [ Claude 思考 (Thought) ] -> "我需要打开浏览器"
        ↓
    [ 输出 Skill 调用 ] -> call: open_browser("mtime.com")
        ↓
    [ 环境执行 (Environment) ] -> 渲染网页并截屏
        ↓
    [ 视觉感知 (Vision) ] -> 识别到“登录”按钮坐标 (500, 120)
        ↓
    [ 循环执行 ] -> 移动鼠标 -> 点击 -> 输入数据
    ```
    

### 5. 避坑与检测 (Metacognition)

- **警惕陷阱**：
    
    - **安全与权限**：给 AI “计算机使用权”极具风险。它可能误删文件或发送错误的邮件。必须在隔离的环境（沙箱）中运行。
        
    - **环境延迟**：如果网络卡顿导致截图与实际不符，AI 可能会点错位置（坐标偏移）。
        
- **自测清单**：
    
    1. 为什么 Claude 需要先发一段文字解释它要做什么，再调用 Skill？（提示：通过 CoT 减少决策错误）。
        
    2. 相比于 API 形式的 Tool Use，Computer Use 的核心优势在哪里？（提示：对没有 API 的老旧或复杂软件的兼容性）。
        

---

**至此，我们已经完整走过了从“向量计算”到“控制计算机”的全过程。**

你现在不仅理解了 AI 是如何**思考**的（Transformer, MoE, LoRA），还理解了它是如何**获取信息**的（RAG），以及它是如何**影响物理世界**的（Agent & Skills）。
