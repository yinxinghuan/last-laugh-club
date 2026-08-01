# 《最后笑的人》技术文档

## 1. 技术栈

- React 18 + TypeScript：界面、五态流程、三小品推进与输入管理。
- Less：黑色流媒体选集视觉系统与 390×844 / 320×568 响应式布局。
- Vite 5：`base: './'`，构建产物可部署到任意子路径。
- HTML5 Video：H.264 + AAC；普通片段 5 秒，第三段成功片段 10 秒。
- WebP：每段建立起帧、共同选择停点与三个结果尾帧。
- 制作期 Python：Aigram transit 生图、首尾帧视频生成、可恢复 manifest 和正式海报。

## 2. 目录结构

```text
src/LastLaughClub/
  LastLaughClub.tsx       # cover/setup/question/performance/verdict 五态与推进
  LastLaughClub.less      # 选集 UI、触控反馈、短屏重排与减弱动效
  data.ts                 # 三段故事、九个分支、中英文结果和 5/10 秒配置
  types.ts                # Sketch、Outcome、Phase、Copy 类型
  i18n/index.ts           # game_locale / 浏览器语言检测与通用词典
public/media/sketch1..3/  # 每段建立视频、停点、结果视频与尾帧
_production/
  generate_sketch_media.py # 配置驱动的可恢复图片/视频生产器
  sketch*-production.json  # 演员、地点、道具、分支动作和时长合同
  sketch*-media-manifest.json
  generate_poster.py       # Aigram 主视觉与英文栅格排版
_qa/
  capture.mjs              # 双视口完整成功路线截图
  verify-flow.mjs          # 失败换位、三段推进、10 秒终局与英文小屏断言
  video-frames/            # 每秒抽帧与终局 5×2 接触表
doc/                       # 需求、视觉与技术文档
```

## 3. 核心模块

### 状态和推进

`LastLaughClub.tsx` 维护 `cover → setup → question → performance → verdict`。`sketchIndex` 指向当前独立小品；失败回到本段并将三个答案循环换位，成功进入下一段，第三段成功后回封面。视频 `onEnded` 是主完成信号，配置时长加 600 ms 的定时器是漏事件兜底。

### 剧情数据

`data.ts` 是运行时真源。每个 `Sketch` 独立声明演员无关的界面文案、媒体目录和三个 `Outcome`；第三段 `music_box_chooses` 的 `videoTime` 为 10，其余结果为 5。共享的是状态机和情绪节奏，不共享人物、场景或荒诞道具。

### 媒体连续性

每段媒体包固定为 `setup_start.webp → setup.mp4 → choice.webp → outcome.mp4 → outcome_end.webp`。建立视频结束在选择停点，三个结果视频都从同一停点起步。`generate_sketch_media.py` 从 JSON 配置读取提示词，支持仅起帧、仅停点、仅尾帧、单分支重建和视频重建；manifest 保存远程 URL、任务 ID、提示词和 `video_time`。轮询间隔为 15 秒，429 视为暂态继续等待。

### 响应式和输入

舞台宽度 `100%`、最大 430 px、高度 `100dvh`，普通 DOM 在短屏内重排，不做整页缩放。320×568 时压缩顶栏、图片说明和间距，三个答案仍全部可见且不低于 44 px。按钮使用 `onPointerDown`；键盘支持 Enter、1–3 与 M。入口含 iOS 长按保护。

### 声音和多语言

视频自带 AAC 声轨；声音开关控制 `muted`，偏好保存在专属键 `last_laugh_club_sound_v1`。`i18n/index.ts` 从 `game_locale` 或浏览器语言选择 zh/en；剧情内容使用 `{zh,en}` 对象，英文 320 px 是发布断言。

## 4. 扩展点

- 改故事、题面或答案：编辑 `src/LastLaughClub/data.ts`，并同步 `doc/requirements.md`。
- 新增小品：增加 `public/media/sketchN/`、生产配置、manifest 和 `sketches` 条目；扩展两份 QA 脚本的成功路线。
- 改演员、地点或道具：先改对应 `sketchN-production.json`，从该段起帧重新生成完整媒体包，不能混用旧停点。
- 调时长：同时修改生产配置 `video_time`、运行时 `videoTime` 和 QA 断言；只用已验证的 5 或 10 秒。
- 改 UI：编辑 `LastLaughClub.less` 并同步 `doc/visual.md`；保持问题页一图、一冲突、一问题、三答案的信息上限。
- 接平台存档或统计：从 `src/shared/runtime` 接入；当前短剧选集不使用头像、排行榜或跨会话进度。
