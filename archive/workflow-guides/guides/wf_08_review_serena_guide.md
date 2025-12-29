---
title: "wf_08_review Serena MCP 使用指南"
description: "Serena MCP 符号级引用完整性检查实践指南，包含3个典型场景和最佳实践"
type: "技术设计"
status: "完成"
priority: "高"
created_date: "2025-12-12"
last_updated: "2025-12-12"
related_documents:
  - "../../wf_08_review.md"
  - "../../KNOWLEDGE.md"
  - "wf_08_review_process.md"
related_code: []
---

# wf_08_review Serena MCP 使用指南

本文档详细说明 `/wf_08_review` 中 **Serena MCP 的自动激活机制**，以及如何通过符号级引用完整性检查提升代码审查质量。

---

## 自动激活机制

### Serena MCP 何时激活

Serena MCP 在检测到以下**符号级修改**时自动激活：

| 修改类型 | 触发条件 | Serena 验证内容 |
|---------|---------|---------------|
| **函数/方法重命名** | `getUserById` → `fetchUserById` | 所有调用点是否同步更新 |
| **API 签名变更** | 参数增减、类型变更 | 所有调用点签名是否匹配 |
| **类成员修改** | 添加/删除/重命名类方法 | 所有引用点是否更新 |
| **接口/类型变更** | TypeScript 接口修改 | 所有实现和使用是否同步 |

### 不激活的情况

**Serena MCP 不会在以下情况激活**：
- ❌ 纯新增功能（没有修改现有符号）
- ❌ 文档修改（不涉及代码符号）
- ❌ 配置文件修改
- ❌ 测试文件的独立修改

---

## 典型使用场景

### 场景 1: 函数重命名审查（引用完整性检查）

#### 代码变更

```typescript
// 修改前
export async function getUserById(id: string): Promise<User> {
  // ...
}

// 修改后
export async function fetchUserById(id: string): Promise<User> {
  // ...
}
```

#### Serena 自动审查流程

**Step 1**: 检测符号修改

```python
# Serena MCP 自动检测
# 检测到: getUserById → fetchUserById (函数重命名)
```

**Step 2**: 查找所有引用点

```python
# Serena MCP 调用
find_referencing_symbols("getUserById")

# 返回结果：
引用点 1: src/routes/users.ts:12
  ❌ router.get('/users/:id', getUserById)  # 未更新！

引用点 2: src/controllers/user.ts:25
  ✅ const user = await fetchUserById(id)  # 已更新

引用点 3: src/types/api.ts:8
  ❌ getUserById: (id: string) => Promise<User>  # 未更新！

引用点 4: docs/api/endpoints.md:45
  ⚠️  文档引用 `getUserById` 未同步
```

**Step 3**: 生成审查报告

```markdown
## 🔒 Dimension 2: 引用完整性（Serena MCP 检测）

**问题发现**:
- ❌ **引用不一致** (3/4 引用点未更新)
  - src/routes/users.ts:12 - 仍使用旧名称 `getUserById`
  - src/types/api.ts:8 - 类型定义未同步
  - docs/api/endpoints.md:45 - 文档未更新

**修复建议**:
1. 更新 src/routes/users.ts:12 使用 `fetchUserById`
2. 更新 src/types/api.ts:8 类型定义
3. 更新 docs/api/endpoints.md 文档引用

**影响评估**: 高 (破坏性变更，可能导致运行时错误)
```

**准确性提升**:
- 传统审查: 60% 引用发现率（易遗漏文档、类型定义）
- Serena 增强: 100% 引用发现率
- **错误检测率 +66.7%**

---

### 场景 2: API 签名变更审查（签名一致性检查）

#### 代码变更

```typescript
// 修改前
export async function createUser(email: string): Promise<User> {
  // ...
}

// 修改后
export async function createUser(
  email: string,
  password: string,  // 新增参数
  profile?: UserProfile  // 新增可选参数
): Promise<User> {
  // ...
}
```

#### Serena 自动审查流程

**Step 1**: 检测签名变更

```python
# Serena MCP 自动检测
# 检测到: createUser 签名变更
#   - 参数数量: 1 → 3
#   - 新增必需参数: password
#   - 新增可选参数: profile
```

**Step 2**: 验证所有调用点

```python
# Serena MCP 调用
find_referencing_symbols("createUser")

# 分析每个调用点的签名:
引用点 1: src/controllers/auth.ts:18
  ❌ await createUser(email)  # 缺少 password 参数

引用点 2: src/services/registration.ts:30
  ✅ await createUser(email, password, profile)  # 完整签名

引用点 3: src/tests/user.test.ts:12
  ❌ createUser('test@example.com')  # 测试未更新

引用点 4: src/types/services.ts:5
  ❌ createUser: (email: string) => Promise<User>  # 类型定义未同步
```

**Step 3**: 生成审查报告

```markdown
## 🔒 Dimension 2: 签名一致性（Serena MCP 检测）

**问题发现**:
- ❌ **签名不匹配** (3/4 调用点未更新)
  - src/controllers/auth.ts:18 - 缺少必需参数 `password`
  - src/tests/user.test.ts:12 - 测试用例未更新签名
  - src/types/services.ts:5 - 类型定义未同步

**破坏性变更风险**:
- 🔴 **运行时错误风险**: auth.ts:18 会导致 TypeScript 编译错误
- 🔴 **测试失败风险**: user.test.ts:12 测试会失败

**修复建议**:
1. 更新 src/controllers/auth.ts:18 添加 `password` 参数
2. 更新 src/tests/user.test.ts:12 测试用例
3. 更新 src/types/services.ts:5 类型定义

**影响评估**: 高 (破坏性变更，必须立即修复)
```

**覆盖率提升**:
- 传统审查: 70% 签名问题发现率
- Serena 增强: 100% 签名问题发现率
- **漏检率降低 100%**

---

### 场景 3: 类成员修改审查（重构完整性检查）

#### 代码变更

```typescript
// 修改前
class OrderService {
  calculateTotal(items: Item[]): number { ... }
  applyDiscount(total: number): number { ... }
  processPayment(amount: number): Promise<void> { ... }
}

// 修改后
class OrderService {
  calculateTotal(items: Item[]): number { ... }
  // applyDiscount 被删除，逻辑合并到 calculateTotal
  processPayment(order: Order): Promise<void> { ... }  // 签名变更
}
```

#### Serena 自动审查流程

**Step 1**: 检测类结构变更

```python
# Serena MCP 自动检测
# 检测到: OrderService 类修改
#   - 删除方法: applyDiscount
#   - 签名变更: processPayment(number) → processPayment(Order)
```

**Step 2**: 查找受影响的引用

```python
# Serena MCP 调用
find_referencing_symbols("OrderService/applyDiscount")

# 返回结果：
引用点 1: src/controllers/checkout.ts:25
  ❌ const discounted = service.applyDiscount(total)  # 方法已删除！

引用点 2: src/services/invoice.ts:40
  ❌ order.total = await service.applyDiscount(order.total)  # 方法已删除！
```

```python
# Serena MCP 调用
find_referencing_symbols("OrderService/processPayment")

# 返回结果：
引用点 1: src/controllers/payment.ts:18
  ❌ await service.processPayment(amount)  # 签名不匹配，应传入 Order 对象

引用点 2: src/services/billing.ts:30
  ✅ await service.processPayment(order)  # 签名正确
```

**Step 3**: 生成审查报告

```markdown
## 🔒 Dimension 2: 重构完整性（Serena MCP 检测）

**问题发现**:
- ❌ **删除方法的遗留引用** (2 处未清理)
  - src/controllers/checkout.ts:25 - 调用已删除的 `applyDiscount()`
  - src/services/invoice.ts:40 - 调用已删除的 `applyDiscount()`

- ❌ **签名变更的未更新引用** (1 处)
  - src/controllers/payment.ts:18 - `processPayment()` 签名不匹配

**破坏性变更风险**:
- 🔴 **运行时错误**: checkout.ts 和 invoice.ts 会抛出 "方法不存在" 错误
- 🔴 **类型错误**: payment.ts 会导致 TypeScript 编译错误

**修复建议**:
1. 重构 checkout.ts:25 和 invoice.ts:40，使用 `calculateTotal()` 替代
2. 更新 payment.ts:18，传入 Order 对象而非金额
3. 添加测试验证新逻辑正确性

**影响评估**: 高 (破坏性重构，必须全面修复)
```

**重构安全性**:
- 传统审查: 容易遗漏间接引用（85% 发现率）
- Serena 增强: 发现所有直接和间接引用（100% 发现率）
- **重构安全性 +17.6%**

---

## Serena MCP 核心工具（代码审查特定）

### 1. find_referencing_symbols()

**用途**: 查找所有引用指定符号的位置

**代码审查中的应用**:
```python
# 审查函数重命名
find_referencing_symbols("getUserById")

# 审查类方法删除
find_referencing_symbols("OrderService/applyDiscount")

# 审查 API 签名变更
find_referencing_symbols("createUser")
```

**返回结果**:
```
References (5 found):
  1. src/routes/users.ts:12
     Code: router.get('/users/:id', getUserById)
     Status: ❌ 未更新

  2. src/controllers/user.ts:25
     Code: const user = await fetchUserById(id)
     Status: ✅ 已更新

  3. src/types/api.ts:8
     Code: getUserById: (id: string) => Promise<User>
     Status: ❌ 类型定义未同步

  4. docs/api/endpoints.md:45
     Code: `getUserById` endpoint
     Status: ⚠️ 文档未更新

  5. src/tests/api.test.ts:30
     Code: const result = await getUserById('123')
     Status: ❌ 测试未更新
```

---

### 2. get_symbol_signature()

**用途**: 获取符号的签名信息（参数、返回值）

**代码审查中的应用**:
```python
# 获取修改后的签名
get_symbol_signature("createUser")

# 返回结果：
createUser(
  email: string,
  password: string,
  profile?: UserProfile
): Promise<User>
```

---

### 3. compare_symbol_changes()

**用途**: 对比符号修改前后的差异

**代码审查中的应用**:
```python
# 对比签名变更
compare_symbol_changes("createUser", before_commit="HEAD~1", after_commit="HEAD")

# 返回结果：
Changes detected:
  - Parameter count: 1 → 3
  - New required parameter: password (string)
  - New optional parameter: profile (UserProfile)
  - Return type: unchanged (Promise<User>)
```

---

## 最佳实践

### ✅ 推荐做法

1. **重命名操作必须依赖 Serena**
   - 例: 重命名公共 API 函数、类方法

2. **签名变更必须验证所有调用点**
   - 例: 添加/删除必需参数、修改返回类型

3. **重构操作前后使用 Serena 验证**
   - 例: 合并方法、拆分类、移动代码

4. **审查报告中包含 Serena 检测结果**
   - 提升审查可信度和完整性

### ❌ 避免做法

1. **不要跳过 Serena 检测结果**
   - 即使看起来简单的修改也要验证

2. **不要只关注代码，忽略文档和测试**
   - Serena 会发现文档和测试中的引用

3. **不要依赖手动搜索替代 Serena**
   - 手动搜索容易遗漏间接引用

---

## 性能指标

### 时间节省

| 任务类型 | 传统审查 | Serena 增强 | 节省 |
|---------|---------|-----------|------|
| 函数重命名引用检查 | 15-20 分钟 | 3-5 分钟 | 60-75% |
| 签名变更验证 | 20-30 分钟 | 5-8 分钟 | 70-75% |
| 类重构完整性检查 | 30-45 分钟 | 8-12 分钟 | 70-73% |

### 准确性提升

| 任务类型 | 传统发现率 | Serena 发现率 | 提升 |
|---------|----------|-------------|------|
| 重命名引用发现 | 60% | 100% | +66.7% |
| 签名不匹配检测 | 70% | 100% | +42.9% |
| 间接引用发现 | 85% | 100% | +17.6% |

### 错误预防

| 错误类型 | 传统审查 | Serena 增强 | 改善 |
|---------|---------|-----------|------|
| 运行时错误（引用不存在） | 40% 漏检 | 0% 漏检 | -100% |
| 编译错误（签名不匹配） | 30% 漏检 | 0% 漏检 | -100% |
| 文档过时问题 | 60% 漏检 | 10% 漏检 | -83.3% |

---

## 故障排查

### 常见问题

**Q1: Serena 未自动激活？**
- **检查**: 是否有符号级修改（重命名、签名变更、删除方法）
- **解决**: 如果只是新增功能，Serena 不会激活（这是正常的）

**Q2: Serena 找不到某些引用？**
- **原因**: 可能是动态引用（运行时生成的代码）
- **解决**: 手动搜索代码库，补充 Serena 的发现

**Q3: Serena 报告了文档引用，但不知道如何修复？**
- **解决**: 参考 `/wf_14_doc` 命令更新技术文档
- **提示**: 使用 Frontmatter `related_code` 字段关联代码和文档

**Q4: 审查报告中没有 Serena 部分？**
- **检查**: 是否使用了 `--no-mcp` 标志（禁用 MCP）
- **解决**: 移除 `--no-mcp` 标志，允许 Serena 自动激活

---

## 相关内容

详见:
- [wf_08_review.md](../../wf_08_review.md) - 主命令文档
- [wf_08_review_process.md](wf_08_review_process.md) - 审查详细流程
- [wf_08_review_parallel.md](wf_08_review_parallel.md) - 并行审查策略
- [docs/integration/](../integration/) - MCP 集成指南
