---
title: "案例2: 组件重构（class→hooks）"
description: "React组件从class到function+hooks的分层并行重构实战案例"
type: "示例文档"
status: "完成"
priority: "中"
created_date: "2025-12-03"
last_updated: "2025-12-07"
related_documents:
  - "wf_05_code.md"
  - "docs/examples/parallel_execution_overview.md"
tags: ["并行执行", "代码实现", "React重构", "Hooks", "实战案例"]
---

# 案例2: 组件重构（class→hooks）

**版本**: v2.0 (拆分优化版)
**最后更新**: 2025-12-07

## 📋 目录

- [场景描述](#场景描述)
- [并行执行方案](#并行执行方案)
- [性能对比](#性能对比)

---

## 场景描述

**任务**: 重构 `UserComponent` 及其所有依赖组件，将 class 组件改为 function 组件

**问题**:
- 涉及5个文件：主组件 + 3个子组件 + 1个工具函数
- 需要修改 state 管理、生命周期、props 传递
- 顺序执行预计需要 60 分钟

---

## 并行执行方案

### Wave 1: 并行读取（8秒）

```javascript
// 读取5个相关文件
[
  Read("components/User.jsx"),
  Read("components/UserProfile.jsx"),
  Read("components/UserSettings.jsx"),
  Read("utils/userHelpers.js"),
  Read("tests/User.test.js")
]

// 识别依赖关系
User.jsx
  ├─ UserProfile.jsx (props: user, onUpdate)
  ├─ UserSettings.jsx (props: settings, onChange)
  └─ userHelpers.js (formatUserData, validateUser)
```

### Checkpoint: 重构策略设计（顺序，5分钟）

```
重构计划:
┌──────────────────────────────────────┐
│ Phase A: 工具函数（无依赖）           │
│   - userHelpers.js: 保持不变         │
└──────────────────────────────────────┘
         ↓
┌──────────────────────────────────────┐
│ Phase B: 子组件（依赖工具函数）       │
│   - UserProfile.jsx                  │
│     * class → function                │
│     * this.state → useState           │
│     * componentDidMount → useEffect   │
│   - UserSettings.jsx                 │
│     * class → function                │
│     * this.props → props 解构         │
└──────────────────────────────────────┘
         ↓
┌──────────────────────────────────────┐
│ Phase C: 主组件（依赖子组件）         │
│   - User.jsx                         │
│     * class → function                │
│     * 复杂 state 管理 → useReducer    │
│     * lifecycle → hooks               │
└──────────────────────────────────────┘
```

### Wave 2: 并行重构 Phase B（10秒）

```javascript
// 同时重构2个子组件（Phase A 不需要改动）
[
  Edit("components/UserProfile.jsx", refactor_to_hooks),
  Edit("components/UserSettings.jsx", refactor_to_hooks)
]
```

**UserProfile.jsx 重构示例**:

```javascript
// 原代码（class）:
class UserProfile extends Component {
  constructor(props) {
    super(props);
    this.state = { loading: false, data: null };
  }

  componentDidMount() {
    this.loadData();
  }

  async loadData() {
    this.setState({ loading: true });
    const data = await fetchUserProfile(this.props.user.id);
    this.setState({ loading: false, data });
  }

  render() {
    const { loading, data } = this.state;
    if (loading) return <Spinner />;
    return <ProfileDisplay data={data} />;
  }
}

// 新代码（function + hooks）:
function UserProfile({ user, onUpdate }) {
  const [loading, setLoading] = useState(false);
  const [data, setData] = useState(null);

  useEffect(() => {
    loadData();
  }, [user.id]);

  async function loadData() {
    setLoading(true);
    const data = await fetchUserProfile(user.id);
    setLoading(false);
    setData(data);
  }

  if (loading) return <Spinner />;
  return <ProfileDisplay data={data} />;
}
```

**UserSettings.jsx 重构示例**:

```javascript
// 原代码（class）:
class UserSettings extends Component {
  constructor(props) {
    super(props);
    this.handleChange = this.handleChange.bind(this);
  }

  handleChange(field, value) {
    this.props.onChange({ ...this.props.settings, [field]: value });
  }

  render() {
    const { settings } = this.props;
    return (
      <div>
        <Input value={settings.email} onChange={(v) => this.handleChange('email', v)} />
        <Toggle checked={settings.notifications} onChange={(v) => this.handleChange('notifications', v)} />
      </div>
    );
  }
}

// 新代码（function + hooks）:
function UserSettings({ settings, onChange }) {
  function handleChange(field, value) {
    onChange({ ...settings, [field]: value });
  }

  return (
    <div>
      <Input value={settings.email} onChange={(v) => handleChange('email', v)} />
      <Toggle checked={settings.notifications} onChange={(v) => handleChange('notifications', v)} />
    </div>
  );
}
```

### Wave 3: 重构主组件（顺序，5秒）

```javascript
// Phase C: 单独处理主组件（依赖 Phase B 完成）
Edit("components/User.jsx", refactor_main_to_hooks)
```

**User.jsx 复杂 state 管理示例**:

```javascript
// 原代码（class）:
class User extends Component {
  constructor(props) {
    super(props);
    this.state = {
      user: null,
      settings: {},
      editing: false,
      error: null
    };
  }

  componentDidMount() {
    this.fetchUser();
  }

  // 多个 setState 调用...
}

// 新代码（function + useReducer）:
const initialState = {
  user: null,
  settings: {},
  editing: false,
  error: null
};

function userReducer(state, action) {
  switch (action.type) {
    case 'SET_USER':
      return { ...state, user: action.payload };
    case 'UPDATE_SETTINGS':
      return { ...state, settings: action.payload };
    case 'TOGGLE_EDITING':
      return { ...state, editing: !state.editing };
    case 'SET_ERROR':
      return { ...state, error: action.payload };
    default:
      return state;
  }
}

function User() {
  const [state, dispatch] = useReducer(userReducer, initialState);

  useEffect(() => {
    fetchUser();
  }, []);

  async function fetchUser() {
    try {
      const user = await api.getUser();
      dispatch({ type: 'SET_USER', payload: user });
    } catch (error) {
      dispatch({ type: 'SET_ERROR', payload: error.message });
    }
  }

  return (
    <div>
      <UserProfile user={state.user} onUpdate={handleUpdate} />
      <UserSettings settings={state.settings} onChange={handleSettingsChange} />
    </div>
  );
}
```

### Wave 4: 更新测试（3秒）

```javascript
Edit("tests/User.test.js", update_tests_for_hooks)

// 测试更新示例
// 原测试: wrapper.instance().setState(...)
// 新测试: act(() => { /* use hooks testing utilities */ })
```

**测试代码更新**:

```javascript
// 原测试（enzyme + instance）:
it('should update user on mount', () => {
  const wrapper = mount(<User />);
  wrapper.instance().componentDidMount();
  expect(wrapper.state('user')).toBeTruthy();
});

// 新测试（React Testing Library + hooks）:
it('should update user on mount', async () => {
  render(<User />);
  await waitFor(() => {
    expect(screen.getByText(/User Profile/i)).toBeInTheDocument();
  });
});
```

### Final: 集成验证（2分钟）

```
验证清单:
✅ 所有组件都转换为 function 组件
✅ useState/useEffect/useReducer 正确使用
✅ Props 传递保持一致
✅ 测试全部通过（35/35）
✅ 无 ESLint 警告
✅ 组件功能无回归

功能验证:
- 用户数据正确加载
- 设置修改正常工作
- 编辑模式切换正常
- 错误处理保持一致
```

---

## 性能对比

| 指标 | 顺序执行 | 并行执行 | 提升 |
|------|---------|---------|------|
| 总时间 | 60 分钟 | 18 分钟 | 3.3x |
| 读取阶段 | 15s | 8s | 1.9x |
| 编辑阶段 | 45s | 18s | 2.5x |
| 重构文件数 | 4 | 4 | 相同 |

**关键成果**:
- 组件架构现代化（class → hooks）
- 代码行数减少 15%（hooks 更简洁）
- 测试覆盖率保持 100%
- 性能提升（减少不必要的重渲染）

**技术亮点**:
- 分层执行：先子组件后主组件
- 复杂状态使用 useReducer
- 测试迁移到 React Testing Library
- 保持向后兼容

---

## 相关资源

- **主命令文档**: [wf_05_code.md](../../wf_05_code.md)
- **并行执行概览**: [parallel_execution_overview.md](./parallel_execution_overview.md)
- **其他案例**:
  - [案例1: 多文件日志功能](./parallel_execution_case1_logging.md)
  - [案例3: API 批量修改](./parallel_execution_case3_api_batch.md)
  - [案例4: 测试套件更新](./parallel_execution_case4_test_update.md)
- **优化技巧**: [parallel_execution_tips.md](./parallel_execution_tips.md)

---

**维护者**: AI Workflow System
**版本**: v2.0 (拆分优化版)
**最后更新**: 2025-12-07
