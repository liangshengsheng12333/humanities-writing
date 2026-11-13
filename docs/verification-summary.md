# 验证摘要与来源说明

## 版本与验证

- 版本：humanities-writing 1.0.1。
- Skill核心目录：35个文件；官方结构验证通过。
- 本地自动化检查：27项通过，覆盖引文保护、标题识别、保守去重、元数据、依赖失败、查询、链接、TLS和内部文件关系。
- 压缩包与完整目录逐一一致。ZIP的SHA-256：`f900a9dea886a65d3712a13500163647ee7b4407731244bfa48b3f0093e2a629`。
- 尚未联网实测外部数据库，未做独立模型端到端评测，未逐条核验理论及术语资料。

## 来源与许可

本Skill整合了用户提供的humanities-thesis和rational-humanistic-writing两份材料，已按学术与一般写作模式改写协调规则。

humanities-thesis原包的MIT许可已完整保留为Skill目录中的LICENSE-humanities-thesis.txt。第二份原包未附单独许可文件，因此不能据此把整个合并版声明为统一采用MIT许可。来源及修改范围见humanities-writing/references/provenance.md；如果上传平台要求选择统一授权，请先确认第二份来源的授权条件。

## 使用条件

核心规则无需Python或网络。可选脚本需Python 3.10及以上，网页解析可选依赖为beautifulsoup4。账号配置和接口权限取决于实际服务与运行平台。首次实际检索前测试所用来源；正式引用前核对相关概念、译法、引语及原文。无需预先安装原始两份Skill。

效果HTML为自拟示意，已在页面明确标注，不能替代实际效果评测。截图中的效果文件为可选项，可以按需要上传。
