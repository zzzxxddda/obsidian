---
aliases: '"#104_Item/大模型应用开发/plan"'
tags:
---


ref:[FastAPI 从入门到精通，一篇就够（超详细实战教程）_fastapi入门到精通-CSDN博客](https://blog.csdn.net/inuex/article/details/159203950)

### 介绍
FastAPI 是一个现代、高性能的 Python Web 框架，用于构建 API。它基于 **Starlette**（异步 Web 框架）和 **Pydantic**（数据验证库），结合了异步编程和类型提示，兼顾开发效率与运行性能。


### 核心定位
维度	核心描述
设计目标	快速开发（代码简洁）、高性能（接近 Node.js/Go）、易维护（类型注解 + 自动文档）
技术基础	基于 Python 3.6+ 的类型注解，整合了 Starlette（异步 Web 框架）和 Pydantic（数据校验库）
核心场景	构建 RESTful API、前后端分离项目的后端、微服务接口、数据可视化接口、自动化测试接口
对比传统框架	比 Flask 更现代（原生支持异步、自动校验、自动文档），比 Django 更轻量（无内置 ORM / 模板，可灵活选择）
简单说：FastAPI 是「为 API 而生的框架」—— 它把 Web 开发中 “重复、繁琐的工作”（如参数校验、接口文档、类型提示）自动化，让你聚焦业务逻辑，而非底层细节。


```python
from fastapi import FastAPI, Depends, HTTPException
from pydantic import BaseModel
from typing import Optional

app = FastAPI()

# 定义依赖函数（无参数）
async def get_token_header(x_token: str = Depends()):
    """验证请求头中的X-Token"""
    if x_token != "fake-super-secret-token":
        raise HTTPException(status_code=400, detail="X-Token header invalid")

# 定义带参数的依赖类
class PaginationParams(BaseModel):
    page: int = 1
    size: int = 10

async def get_pagination_params(params: PaginationParams = Depends()):
    """解析分页参数"""
    if params.size > 100:
        params.size = 100  # 限制最大页大小
    return params

# 1. 单个依赖注入
@app.get("/items/")
async def read_items(token: str = Depends(get_token_header)):
    return {"token": token, "items": [{"id": 1}, {"id": 2}]}

# 2. 多个依赖注入 + 嵌套依赖
async def get_current_user(token: str = Depends(get_token_header)):
    """嵌套依赖：先验证token，再获取当前用户"""
    return {"username": "admin", "token": token}

@app.get("/users/me/")
async def read_current_user(
    user: dict = Depends(get_current_user),
    pagination: PaginationParams = Depends(get_pagination_params)
):
    return {"user": user, "pagination": pagination}

# 3. 路由级依赖（对该路由下所有操作生效）
from fastapi import APIRouter

router = APIRouter(dependencies=[Depends(get_token_header)])

@router.get("/private/")
async def private_route():
    return {"message": "This is a private route"}

app.include_router(router)

# 4. 全局依赖（对所有路由生效）
# app = FastAPI(dependencies=[Depends(get_token_header)])
```

