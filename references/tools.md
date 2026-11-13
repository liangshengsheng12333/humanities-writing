# 可选辅助工具

核心写作规则不依赖Python或网络。可选脚本要求Python 3.10及以上，以下脚本在具备相应条件时辅助工作；路径以本skill所在目录为基准。

## 本地文本提示

    python scripts/review.py paper.md --mode academic --unit fragment --format json
    python scripts/review.py essay.md --mode general --unit document

仅全文有明确结构要求时，逐项指定需要检查的标题：

    python scripts/review.py paper.md --mode academic --unit document --require 摘要 --require 参考文献

脚本使用Python标准库，检查待补充标记、模糊归因、未来年份候选、空注释及少量表达信号。代码块、Markdown引用块、行内代码和常见成对引号里的文字不做提示扫描，支持跨行及嵌套引号。引号未闭合时保守保护其后文本；异常排版仍需人工复核。全文标题检查兼容编号、加粗及中文标题中的空格。未来年份只提示核查，可能属于已接受待刊文献。

所有结果均为提示，不自动改稿。不以“而是”“不仅”、专业词数量、连接词数量、标题数量判断质量；零提示不证明事实、引文或逻辑正确。没有指定必需标题就不报告缺摘要；片段模式不检查全文结构。

如需禁用具体句式，依用户要求人工或模型复核受保护范围；脚本不取代这种语境判断。

## 文献搜索

    python scripts/search.py "研究关键词" --sources openalex,crossref --limit 5 --format json

保留原包的八个数据源适配器，修复入口和库导入。默认只尝试OpenAlex、Semantic Scholar、Crossref；其他来源需明确指定。接口可用性、字段和认证要求可能变化。本版未实测外部数据库，不能保证实时可用。

配置优先级：已有环境变量优先；其次读取HUMANITIES_WRITING_CONFIG明确指定的配置文件；未指定时仅查本skill的scripts/.env，不读取当前工作目录中的.env。显式路径建议使用绝对路径，指定后不再回退到其他文件。可配置项：CNKI_COOKIE、SERPAPI_KEY、S2_API_KEY、CORE_API_KEY、OPENALEX_EMAIL、CROSSREF_EMAIL。是否需要某项及是否收费，按实际服务要求确认；配置检查只说明本地条件，不代表接口联网成功。

知网、万方、国家哲学社会科学文献中心及Google Scholar直连的网页解析需要BeautifulSoup，缺失时明确报错，不表示检索到零条文献；可选依赖列于requirements.txt，不自行安装。优先使用已有工具，工具失败时使用用户导出材料。脚本不自动复用浏览器会话或安装浏览器控制工具。

Key和Cookie只在相应搜索获授权且用户已经配置时使用，不显示到作品、日志、示例或包中。不要从浏览器擅自提取凭据。HTTP请求保留证书验证，证书失败就停止，不降级到未验证连接。

输出中的分数仅为原始元数据排序启发，不是质量评级。引文是简化草稿，需对照来源与目标格式；文献类型未知时标为“类型待核对”，不因缺少期刊名推断为专著。链接默认为文献记录，只有上游明确的全文地址才作相应标注，访问情况仍未验证。去重优先按DOI；不同非空DOI不合并，缺DOI时需同标题、同作者、同年份支持。元数据冲突通过metadata_conflicts保留，歧义记录分别保留。搜索元数据、摘要和全文应分别标明；出现接口错误时说明哪一来源失败，不把失败解释成没有文献。

## 文件处理

PDF、DOCX与OCR调用当前平台的可用能力；不预装工具，不假定上传目录。脚本并不提供完整的Word排版、OCR或投稿服务。

查询扩展位于scripts/lib/query.py，使用独立小型字典，不读取术语表，默认搜索入口也不自动调用它。扩展建议保留未映射片段、数字与原始查询；混合语言建议需人工核对，不能当作完整英译。
