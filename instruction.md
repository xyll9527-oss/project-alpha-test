# 项目Alpha的指令Instruction

## Project Alpha的需求和设计文档

构建一个简单的试用标签分类和管理Ticket的工具,它基于postgresql数据库,前端基于vue3 + element-plus,后端基于python + fastapi.无需用户系统,当前用户可以：
- 创建/删除/编辑/完成/取消完成 Ticket
- 添加/删除 Ticket的标签
- 根据不同的标签过滤出Ticket
- 根据名称搜索Ticket,并显示搜索结果,支持分页,默认为10条/页,可以调整pageSize大小【10条/页,20条/页,30条/页】

按照这个想法详细的帮我生成需求和设计文档,输出为中文格式,保存到文件`project-alpha-design.md`中

## Project Alpha的实现计划文档
按照`project-alpha-design.md`中的需求和设计文档,生成一个详细的实现计划,输出为中文格式,保存到文件`project-alpha-implementation.md`中

# 分阶段实现
根据生成的`project-alpha-implementation.md` 完整实现这个项目的后端代码
根据生成的`project-alpha-implementation.md` 完整实现这个项目的前端代码