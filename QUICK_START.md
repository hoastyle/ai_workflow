# 🚀 WF_ 工作流系统 - 5分钟快速上手

## 1️⃣ 第一次使用？3个命令搞定！

```bash
# 1. 创建项目规划
@wf_planning.md 我的项目

# 2. 生成任务列表
@wf_task.md create

# 3. 开始工作
@wf_prime.md
```

## 2️⃣ 日常开发 - 记住这个循环

```bash
@wf_prime.md          # 早上：加载项目
@wf_code.md 新功能    # 开发
@wf_test.md          # 测试
@wf_commit.md        # 提交
@wf_task.md update   # 更新进度
```

## 3️⃣ 遇到问题？

```bash
# 有错误？
@wf_debug.md 错误描述

# 需要帮助？
@wf_ask.md 你的问题

# 代码需要优化？
@wf_refactor.md 目标代码
```

## 4️⃣ 上下文太大？

```bash
/clear               # 清理
@wf_prime.md        # 重新加载，继续工作！
```

## 5️⃣ 三个救命命令

| 迷茫时 | 用这个 |
|--------|--------|
| 忘记命令了 | `@wf_help.md` |
| 不知道流程 | `@wf_guide.md` |
| 要快速查找 | `@wf_quick.md` |

---

## 🎯 黄金法则

1. **永远先 prime** - 每个会话开始运行 `@wf_prime.md`
2. **经常 update** - 完成工作就 `@wf_task.md update`
3. **遇事不决问** - 不确定就 `@wf_ask.md`

## 📝 真实示例

### 实现登录功能
```bash
@wf_prime.md                    # 加载项目
@wf_ask.md 登录功能最佳实践？      # 咨询
@wf_code.md 实现JWT登录          # 编码
@wf_test.md 登录模块             # 测试
@wf_commit.md                   # 提交
```

### 修复Bug
```bash
@wf_prime.md                    # 加载项目
@wf_debug.md 用户无法登录         # 调试
@wf_test.md 登录修复             # 验证
@wf_commit.md fix: 修复登录问题  # 提交
```

---

**记住**: 所有命令都以 `wf_` 开头 = **W**ork**F**low（工作流）

💡 **Pro Tip**: 打印这个页面放在手边，直到熟练为止！