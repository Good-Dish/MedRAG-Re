# 😎MedRAG-Rebuild

**这是一个关于[MedRAG: Enhancing Retrieval-augmented Generation with Knowledge Graph-Elicited Reasoning for Healthcare Copilot](https://github.com/SNOWTEAM2023/MedRAG). ([paper](https://arxiv.org/abs/2502.04413))的复制实现**

## 🚀 Features

- 删除传统RAG的部分，因为没有与构建的知识图谱匹配的文档
- 添加*从患者输入中提取关键词*部分
- 添加*构建知识图谱*部分
- 使用FAISS方法匹配输入关键字和症状节点（而不是余弦相似度）

## 📢 Acknowledgments of ReferencesREADME_ENG.md

- `utils\logger.py`来自 [CONTHO_RELEASE/lib/core/logger.py](https://github.com/dqj5182/CONTHO_RELEASE/blob/main/lib/core/logger.py)
- `data\medical_default.json`是通过对[KnowledgeGraphBeginner/2.medicalKnowledgeGraph/data/medical.json](https://github.com/JesseYule/KnowledgeGraphBeginner/blob/main/2.medicalKnowledgeGraph/data/medical.json)进行修改得到的

## 📦 Installation

1. 克隆本仓库

```bash
git clone https://github.com/Good-Dish/MedRAG-Rebuild.git
cd MedRAG-Rebuild
```

2. 创建conda环境

``````bash
conda create -n medrag-rebuild python=3.10
conda activate medrag-rebuild
pip install -r requirements.txt
``````

3. 通过运行 `generate_config.ipynb`来生成配置文件

> - 在 `"database"`部分填入您的**neo4j** 知识数据库的信息 ([Native Graph Database | Neo4j Graph Database Platform](https://neo4j.com/product/neo4j-graph-database/))
> - 在`"ask_LLM"`部分填入您的**deepseek** key
> - 默认嵌入模型为**m3e**，有三种类型可以选择 `small/base/large`
> - 默认的知识被命名为“default”，如果您希望修改现有知识内容，请遵循`“data\medical_default. json”`所示的格式结构在JSON文件中组织相关知识
> - `"key"`"在`"extract_keywords"`中的值表示输入关键字与哪些类型的节点匹配

4. 运行 `main.py`

``````bash
python main.py --query your_symptoms
``````

> 为了达到关键词提取的效果，请将您的症状以**中文、词组、用“，”分隔开的形式赋值给'your_symtoms' **. 

## ✅To-Do

- [x] 从知识文件创建知识图谱
- [x] 从患者输入中提取关键字
- [x] 嵌入关键词
- [x] 匹配临床特征和叶结节
- [x] 向上遍历
- [x] 产生诊断差异知识图谱
- [x] 问答系统

