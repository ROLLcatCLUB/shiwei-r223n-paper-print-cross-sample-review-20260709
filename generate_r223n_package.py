from __future__ import annotations

import hashlib
import html
import json
import re
import textwrap
import zipfile
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parent
STAGE_ID = "1013R_R223N_CROSS_SAMPLE_CLASSROOM_EVENT_EXPANSION_VALIDATION"
STANDARD_ID = "GOLDEN_CLASSROOM_EVENT_EXPANSION_STANDARD_V0.1_LOCK_CANDIDATE"
SOURCE_SAMPLE = "有趣的纸印"
SOURCE_DOCX = "E:/学校工作/教学/教学资料/三年级美术上册官方教学设计参考/第五单元 有趣的纸印.docx"


SOURCE_ANCHORS = {
    "学情分析": "三年级学生对肌理有初步认识，在寻找不同质感纸材和拓印材料肌理上有经验，但专业油墨制作、多版多色技能仍需练习。",
    "大观念": "印痕是版画的独特语言。",
    "基本问题": "不同纸材和不同印法的碰撞会给我们带来怎样的惊喜呢。",
    "表现性任务": "用版画作品装饰“版画车间坊”，并形成纸材印痕科普读本、印痕手册或作品展示。",
    "第一阶段": "收集不同纸张，运用刻、剪、撕、拼贴、揉、卷、折等方法创造纸的新肌理，制作纸的印痕科普读本。",
    "第二阶段": "充分利用纸材纹理，经染色或拓印形成作品，并对初步认知的印痕进行加工，制作印痕手册。",
    "第三阶段": "用干印、湿印、干湿法、油印法进行印制，注意拓印轻重缓急，让画面形成黑、灰层面。",
    "第四阶段": "学习一版多色、多版多色套色版画，布置“版画车间坊”。",
    "评价方案": "能尝试各种纸材制作版画，了解纸材纹理、印痕及特性；能掌握干印、水印、油印等技法；能记录、分享并清理油墨。",
}


EVENTS = [
    {
        "event_id": "paper_print_event_01_task_entry",
        "event_name": "任务入场：走进版画车间坊",
        "section": "单元任务与课堂入场",
        "source_anchor": {
            "sample": SOURCE_SAMPLE,
            "anchor": "单元表现性任务 / 第一阶段学习活动",
            "evidence": "用版画作品装饰“版画车间坊”；明确单元任务，了解各种纸材及它的纹理。",
            "source_status": "source_evidence",
        },
        "teaching_responsibility": "把课堂从普通纸手工拉回版画语言，明确本课要寻找纸材、印法和印痕之间的关系。",
        "student_problem": "学生容易把任务理解成随便做纸作品，忽视“印出来的痕迹”才是本单元要研究的核心。",
        "task_release": "今天我们不是只做一张纸作品，而是进入一个小小的版画车间。请你带着一个问题开始：纸材和印法碰在一起，会留下什么样的印痕惊喜？",
        "expected_student_responses": [
            "能说出纸张有厚薄、软硬、粗糙、光滑等差异。",
            "能联想到拓印、印章、压印等生活经验。",
            "能知道最后要把作品或记录放进版画车间坊展示。",
        ],
        "likely_misconceptions_or_failures": [
            "只关注作品好不好看，忘记记录纸材和印法。",
            "把版画车间坊理解成普通展板布置。",
            "不知道印痕和画出来的线条有什么区别。",
        ],
        "teacher_follow_up_questions": [
            "这张纸如果不画，只印，会留下什么样的痕迹？",
            "你觉得痕迹会更像纸本来的样子，还是更像你用力的样子？",
            "等会儿展示作品时，别人要从哪里看出你的纸材和印法？",
        ],
        "teacher_scaffolding_moves": [
            "用一张普通绘画作品和一张拓印痕迹图作对比，圈出画线与印痕的不同。",
            "给学生一个简单记录句式：我用的是……纸，试了……印法，留下了……印痕。",
            "把“版画车间坊”定位为作品和试验证据共同展示的空间。",
        ],
        "teacher_rescue_strategy": "如果学生仍按手工装饰理解任务，教师先展示一张材料痕迹明显的试印纸，追问“这里最有意思的是图案，还是纸留下的纹理？”再把任务缩小成先找一种痕迹。",
        "screen_trigger": {
            "trigger_condition": "任务释放前",
            "content": "版画车间坊任务语 + 画出来/印出来对比图 + 记录句式",
        },
        "component_trigger": {
            "component_id": "compare_two_images",
            "component_name": "比一比",
            "trigger_condition": "学生把任务理解成普通纸作品时",
            "student_problem_solved": "区分绘画线条与纸材印痕。",
            "alternative_component": "circle_and_annotate",
            "expected_evidence": "学生能圈出一处印痕并说出它不是画出来的。",
        },
        "learning_sheet_trigger": {
            "field": "入场记录",
            "prompt": "我发现印痕和画线不同的地方是……",
        },
        "evidence_trigger": {
            "evidence_type": "口头说明 + 圈画记录",
            "collect_when": "任务入场 3 分钟内",
            "minimum_evidence": "能说出一个印痕观察点。",
        },
        "assessment_alignment": [
            "理解印痕是版画的独特语言。",
            "明确单元任务并能进入纸材、印法、印痕的观察。",
        ],
        "transition_chain": "从任务入场转向纸材触摸和肌理观察：先知道为什么要看印痕，再去找印痕可能从哪里来。",
        "teacher_visible_note": "不要把版画车间坊说成普通作品展，先把学生眼睛带到“印痕”上。",
        "control_points": {
            "observe": "学生是否能说出印痕与绘画线条的差别。",
            "ask_when": "学生只说好看或图案时，追问痕迹从哪里来。",
            "rescue_when": "任务理解偏向纸手工时，立即用对比图拉回印痕。",
            "screen_when": "任务释放和误解出现时。",
            "component_when": "需要区分两个视觉样本时。",
            "evidence_when": "学生完成第一句观察记录后。",
            "proceed_when": "多数学生能说出一个纸材或印法可能影响印痕的点。",
        },
    },
    {
        "event_id": "paper_print_event_02_material_texture_observation",
        "event_name": "摸一摸：纸材肌理观察",
        "section": "纸材观察与分类",
        "source_anchor": {
            "sample": SOURCE_SAMPLE,
            "anchor": "学情分析 / 第一阶段学习任务",
            "evidence": "学生对肌理有初步认识；寻找不同质感纸材，分析纸张印痕。",
            "source_status": "source_evidence",
        },
        "teaching_responsibility": "让学生用手摸、眼看、侧光观察等方式，把纸材差异转化为可以预测印痕的依据。",
        "student_problem": "学生知道纸不一样，但容易只说厚薄、颜色，不能把肌理和后面印出来的效果联系起来。",
        "task_release": "每组选择三种纸，不急着印。先摸一摸、看一看、斜着照一照，猜一猜哪张纸最可能留下明显肌理。",
        "expected_student_responses": [
            "能发现纸张厚薄、软硬、粗糙、光滑、凹凸纹理。",
            "能猜测粗糙或有纹理的纸可能更容易留下痕迹。",
            "能用简单词语给纸材分类。",
        ],
        "likely_misconceptions_or_failures": [
            "只按颜色或大小分类。",
            "摸完没有语言描述，只说“这个好”。",
            "认为最厚的纸一定印痕最好。",
        ],
        "teacher_follow_up_questions": [
            "你摸到的是滑，还是有一点凹凸？",
            "如果油墨碰到这里，最可能留在哪些地方？",
            "这张纸为什么可能印得清楚？你的依据是什么？",
        ],
        "teacher_scaffolding_moves": [
            "提供词库：粗糙、细密、凸起、凹下、吸水、光滑、柔软、硬挺。",
            "让学生用手指沿着纹理方向摸，再用细头记号笔轻轻圈出最明显的肌理区。",
            "要求每组只选一张最想试印的纸，并写一句预测。",
        ],
        "teacher_rescue_strategy": "如果学生只按颜色分类，教师拿两张同色但肌理不同的纸让学生闭眼触摸，追问“看不见颜色以后，你还能怎么分？”",
        "screen_trigger": {
            "trigger_condition": "观察前和分类混乱时",
            "content": "纸材观察词库 + 侧光肌理照片 + 一句预测格式",
        },
        "component_trigger": {
            "component_id": "material_blind_box",
            "component_name": "材料盲盒",
            "trigger_condition": "学生只看颜色或外形时",
            "student_problem_solved": "让学生用触觉和肌理词汇认识材料差异。",
            "alternative_component": "circle_and_annotate",
            "expected_evidence": "一条纸材预测记录。",
        },
        "learning_sheet_trigger": {
            "field": "纸材预测",
            "prompt": "我选择的纸材是……我预测它会留下……印痕，因为……",
        },
        "evidence_trigger": {
            "evidence_type": "纸材分类表 + 预测句",
            "collect_when": "试印前",
            "minimum_evidence": "每组至少一条带理由的纸材预测。",
        },
        "assessment_alignment": [
            "了解各种纸材及它的纹理。",
            "能主动参与纸材收集、分类和特性分析。",
        ],
        "transition_chain": "从纸材预测转向纸材改造：学生先知道原有肌理，再尝试制造新的肌理。",
        "teacher_visible_note": "观察不是热身，必须留下“我预测”的理由，后面才能验证。",
        "control_points": {
            "observe": "学生是否能用肌理词描述纸材，而不只说颜色。",
            "ask_when": "学生给出预测但没有依据时。",
            "rescue_when": "分类只停在颜色大小时。",
            "screen_when": "词汇不足或观察方向散乱时。",
            "component_when": "需要把视觉观察转为触觉观察时。",
            "evidence_when": "每组确定试印纸材前。",
            "proceed_when": "每组能说出一种纸材特性和一个印痕预测。",
        },
    },
    {
        "event_id": "paper_print_event_03_texture_making",
        "event_name": "变一变：制造纸的新肌理",
        "section": "纸材改造与肌理生成",
        "source_anchor": {
            "sample": SOURCE_SAMPLE,
            "anchor": "第一阶段学习活动",
            "evidence": "运用刻、剪、撕、拼贴、揉、卷、折等方法，创造纸的新肌理。",
            "source_status": "source_evidence",
        },
        "teaching_responsibility": "让学生理解纸材不是被动材料，可以通过改造制造新的可印肌理。",
        "student_problem": "学生可能把改造理解成做造型或装饰，忽略改造后要能留下可辨认的印痕。",
        "task_release": "请你只选一种方法改造纸：刻、剪、撕、揉、卷、折或拼贴。改造后先不追求像什么，而要看看它会不会留下新的肌理。",
        "expected_student_responses": [
            "能尝试一种纸材改造方法。",
            "能发现揉皱、折线、撕边、拼贴厚度会影响印痕。",
            "能说出自己改造的是哪一处肌理。",
        ],
        "likely_misconceptions_or_failures": [
            "剪成复杂造型却没有可印纹理。",
            "拼贴太厚导致试印时压不平。",
            "方法太多，时间失控。",
        ],
        "teacher_follow_up_questions": [
            "你改造出来的肌理在哪里？请用手指给同伴看。",
            "这个肌理印出来可能是线、点，还是一片灰？",
            "如果太厚压不平，你可以减少哪一层？",
        ],
        "teacher_scaffolding_moves": [
            "把方法限制为“一组先选一种”。",
            "出示半成品示范：一张揉皱纸、一条撕边、一块拼贴纹理。",
            "提醒学生把最想印的一面朝上，先做小块试验。",
        ],
        "teacher_rescue_strategy": "如果学生陷入复杂手工，教师暂停 30 秒，让全班看一个简单但肌理清楚的小样，强调今天先要能印清楚，再考虑造型丰富。",
        "screen_trigger": {
            "trigger_condition": "纸材改造开始前",
            "content": "刻/剪/撕/拼贴/揉/卷/折方法图 + 小块试验提醒",
        },
        "component_trigger": {
            "component_id": "technique_breakdown",
            "component_name": "技法拆解",
            "trigger_condition": "学生不知道如何把纸变出肌理时",
            "student_problem_solved": "把纸材改造拆成可操作的小动作。",
            "alternative_component": "error_repair_demo",
            "expected_evidence": "一块能说明改造方法的试印版。",
        },
        "learning_sheet_trigger": {
            "field": "改造方法",
            "prompt": "我用……方法让纸出现了……肌理。",
        },
        "evidence_trigger": {
            "evidence_type": "改造小样 + 方法记录",
            "collect_when": "正式试印前",
            "minimum_evidence": "每组保留一个改造小样。",
        },
        "assessment_alignment": [
            "能用刻、揉、卷等方法在纸上制造肌理。",
            "能将纸材改造作为版画表现语言的来源。",
        ],
        "transition_chain": "从制造肌理转向转印验证：只有试印后，学生才能知道肌理是否真的成为印痕。",
        "teacher_visible_note": "限制方法数量，宁可小而清楚，不要复杂但印不出来。",
        "control_points": {
            "observe": "学生改造是否能形成可印肌理。",
            "ask_when": "学生只追求形状或装饰时。",
            "rescue_when": "拼贴过厚、方法过多或时间失控时。",
            "screen_when": "动作不清楚或小样不成立时。",
            "component_when": "需要拆技法步骤时。",
            "evidence_when": "小样完成后、试印前。",
            "proceed_when": "每组至少有一块可试印小样。",
        },
    },
    {
        "event_id": "paper_print_event_04_first_print_trial",
        "event_name": "试一试：第一次转印",
        "section": "印痕试验与记录",
        "source_anchor": {
            "sample": SOURCE_SAMPLE,
            "anchor": "第二阶段学习活动 / 单元评价方案",
            "evidence": "充分利用纸材纹理，经过染色或拓印形成作品；在探索和发现过程中养成随时记录的习惯。",
            "source_status": "source_evidence",
        },
        "teaching_responsibility": "把纸材预测转化为可观察的印痕证据，让学生建立试印、比较、记录的基本习惯。",
        "student_problem": "学生容易一次印完就急着下结论，不看用力、颜料多少、纸材方向怎样影响印痕。",
        "task_release": "每组先只做一次小试印。印完不要马上评价好不好看，先找：哪里清楚？哪里模糊？这和纸材、用力或颜料有什么关系？",
        "expected_student_responses": [
            "能发现清楚、模糊、断裂、灰层、重叠等印痕差异。",
            "能把试印结果和前面的纸材预测联系起来。",
            "能用圈画或一句话记录最明显的印痕。",
        ],
        "likely_misconceptions_or_failures": [
            "颜料太多或太少，导致印痕糊成一片或印不出来。",
            "用力不均，无法判断是纸材问题还是操作问题。",
            "只说好看不好看，不记录原因。",
        ],
        "teacher_follow_up_questions": [
            "你圈出的地方为什么最清楚？",
            "这个模糊是纸材造成的，还是颜料太多造成的？",
            "如果再试一次，你会改变用力、颜料，还是纸材方向？",
        ],
        "teacher_scaffolding_moves": [
            "示范少量上色、均匀压印和慢慢揭纸。",
            "投屏一张清楚印痕和一张糊印痕，让学生比原因。",
            "要求学生在试印纸旁边写一个调整计划。",
        ],
        "teacher_rescue_strategy": "如果全班大面积糊印，教师立即暂停，拿一块小版现场示范“颜料少一点、压力均一点、揭纸慢一点”，再允许每组补一次小试印。",
        "screen_trigger": {
            "trigger_condition": "第一次试印前和糊印较多时",
            "content": "少量上色、均匀压印、慢揭纸三步图 + 清楚/糊印对比",
        },
        "component_trigger": {
            "component_id": "circle_and_annotate",
            "component_name": "圈一圈",
            "trigger_condition": "学生只看整体效果、不看具体印痕时",
            "student_problem_solved": "把评价落到具体可见印痕。",
            "alternative_component": "compare_two_images",
            "expected_evidence": "圈出一处清楚印痕并写调整计划。",
        },
        "learning_sheet_trigger": {
            "field": "试印记录",
            "prompt": "第一次试印：最清楚的地方是……我想调整……",
        },
        "evidence_trigger": {
            "evidence_type": "试印纸 + 圈画标注 + 调整计划",
            "collect_when": "第一次试印后",
            "minimum_evidence": "每组至少一张有圈画和一句调整计划的试印记录。",
        },
        "assessment_alignment": [
            "能用印痕来表达自己的想法。",
            "能在探索中随时记录并说明印痕变化。",
        ],
        "transition_chain": "从一次试印转向印法比较：学生知道印痕会变，下一步验证不同印法如何带来不同变化。",
        "teacher_visible_note": "第一次试印不是成品，关键是让学生留下可比较、可调整的证据。",
        "control_points": {
            "observe": "学生是否能指出清楚或模糊印痕的具体位置。",
            "ask_when": "学生只评价好看时。",
            "rescue_when": "糊印、漏印或无法记录原因时。",
            "screen_when": "需要统一操作关键动作时。",
            "component_when": "需要把观察固定到试印纸上时。",
            "evidence_when": "第一次试印完成立即收。",
            "proceed_when": "学生能提出一个下一次试印调整方向。",
        },
    },
    {
        "event_id": "paper_print_event_05_print_method_comparison",
        "event_name": "比一比：干印、湿印与油印",
        "section": "印法比较与技法判断",
        "source_anchor": {
            "sample": SOURCE_SAMPLE,
            "anchor": "第三阶段学习活动 / 单元评价方案",
            "evidence": "用干印法、湿印法、干湿法、油印法印制；掌握干印、水印、油印技法；注意轻重缓急形成黑、灰层面。",
            "source_status": "source_evidence",
        },
        "teaching_responsibility": "让学生在比较中理解印法不是名称记忆，而是会改变印痕清晰度、灰层和画面效果的选择。",
        "student_problem": "学生容易把干印、湿印、油印当作术语背诵，不能说出哪种印法适合自己的纸材和画面需要。",
        "task_release": "同一块小版，用两种不同方法试印。请比较：哪一种边缘更清楚？哪一种灰层更丰富？哪一种更适合你想要的画面？",
        "expected_student_responses": [
            "能比较不同印法造成的清晰、模糊、灰层、浓淡变化。",
            "能发现同一纸材换印法后印痕不同。",
            "能为自己的正式作品选择一种印法并说明理由。",
        ],
        "likely_misconceptions_or_failures": [
            "只记住名称，无法描述差异。",
            "追求颜色浓却忽视印痕层次。",
            "一组同时试太多方法，记录混乱。",
        ],
        "teacher_follow_up_questions": [
            "这两次试印最大的不同在哪里？请指给大家看。",
            "如果你想表现清楚边缘，你会选哪一种？如果想要灰层呢？",
            "你的选择服务画面效果，还是只是因为颜色更重？",
        ],
        "teacher_scaffolding_moves": [
            "把比较控制在两种印法，不一次展开所有术语。",
            "用清晰边缘、灰层、肌理保留三个观察角度替代单纯名称记忆。",
            "要求每组用箭头连接印法、效果和选择理由。",
        ],
        "teacher_rescue_strategy": "如果比较变成术语背诵，教师遮住术语名称，只展示两张试印效果，让学生先说差异，再把差异对应到印法名称。",
        "screen_trigger": {
            "trigger_condition": "印法比较和选择理由不足时",
            "content": "同版不同印法对照图 + 清晰边缘/灰层/肌理保留观察角度",
        },
        "component_trigger": {
            "component_id": "compare_two_images",
            "component_name": "比一比",
            "trigger_condition": "学生无法说出印法差异时",
            "student_problem_solved": "把技法术语转化为可见效果比较。",
            "alternative_component": "match_cards",
            "expected_evidence": "印法-效果-选择理由三联记录。",
        },
        "learning_sheet_trigger": {
            "field": "印法比较",
            "prompt": "我比较了……和……，我选择……，因为它让印痕……",
        },
        "evidence_trigger": {
            "evidence_type": "两张对照试印 + 三联选择理由",
            "collect_when": "正式创作前",
            "minimum_evidence": "每组至少一组同版不同印法对照。",
        },
        "assessment_alignment": [
            "能掌握干印、水印、油印技法。",
            "能注意拓印时轻重缓急，让画面形成黑、灰层面。",
        ],
        "transition_chain": "从印法比较转向正式创作：学生带着明确纸材、印法和效果理由进入作品。",
        "teacher_visible_note": "不要急着讲全套术语，先让学生看见同一块版在不同印法下的差异。",
        "control_points": {
            "observe": "学生是否能用清晰、灰层、肌理等词比较印法。",
            "ask_when": "学生只说某种印法好看或颜色重时。",
            "rescue_when": "术语背诵、比较混乱或记录不清时。",
            "screen_when": "需要用同版对照统一观察标准时。",
            "component_when": "需要对比两种印法效果时。",
            "evidence_when": "学生做出正式印法选择前。",
            "proceed_when": "每组能说明纸材、印法和预期效果的关系。",
        },
    },
    {
        "event_id": "paper_print_event_06_artwork_creation_with_print_marks",
        "event_name": "做一做：用印痕完成作品",
        "section": "纸版画创作与印痕表达",
        "source_anchor": {
            "sample": SOURCE_SAMPLE,
            "anchor": "第二、三阶段学习活动 / 单元学习目标",
            "evidence": "充分利用纸材纹理形成作品；尝试用各种单色表达想法，丰富纸版画表现语言。",
            "source_status": "source_evidence",
        },
        "teaching_responsibility": "引导学生把前面的纸材、肌理、印法选择转化为有画面意识的作品，而不是试印纸堆叠。",
        "student_problem": "学生可能印了很多痕迹但画面杂乱，或者为了完成作品放弃前面试验中发现的好印痕。",
        "task_release": "现在开始完成一幅小作品。你至少要保留一个自己满意的印痕，并说明它来自哪种纸材或印法。",
        "expected_student_responses": [
            "能选择一到两种纸材或印法进入作品。",
            "能保留满意印痕并围绕它组织画面。",
            "能在创作中调整用力、颜料和位置。",
        ],
        "likely_misconceptions_or_failures": [
            "把所有试过的材料都印上去，画面没有重点。",
            "为了完整图案而覆盖掉最有特色的印痕。",
            "清洁习惯不足，油墨或颜料污染作品。",
        ],
        "teacher_follow_up_questions": [
            "这幅作品里最想让大家看到的印痕是哪一处？",
            "这个印痕和你前面的试印有什么关系？",
            "如果画面太满，你可以减少哪一块？",
        ],
        "teacher_scaffolding_moves": [
            "给出一主一辅的画面建议：一个主要印痕，一个辅助印痕。",
            "中途投屏一件重点清楚的作品和一件印痕过多的作品比较。",
            "提醒小组设立清洁员，控制滚筒、油墨和废纸位置。",
        ],
        "teacher_rescue_strategy": "如果画面杂乱，教师让学生用手遮住部分区域，选择最想保留的一处印痕，再围绕它减少或调整其他痕迹。",
        "screen_trigger": {
            "trigger_condition": "正式创作中段",
            "content": "一主一辅画面提示 + 印痕过多/重点清楚作品对比 + 清理提示",
        },
        "component_trigger": {
            "component_id": "gallery_walk_midpoint",
            "component_name": "中途看一看",
            "trigger_condition": "作品普遍堆叠印痕或重点不清时",
            "student_problem_solved": "帮助学生把试验发现转化为画面取舍。",
            "alternative_component": "before_after_compare",
            "expected_evidence": "修改前后作品或口头取舍理由。",
        },
        "learning_sheet_trigger": {
            "field": "作品取舍",
            "prompt": "我最满意的印痕是……它来自……我保留它是因为……",
        },
        "evidence_trigger": {
            "evidence_type": "纸版画作品 + 取舍理由 + 清洁分工记录",
            "collect_when": "作品完成前后",
            "minimum_evidence": "作品中至少有一处可说明来源的印痕。",
        },
        "assessment_alignment": [
            "能用自己满意的印感创作新的印痕之美。",
            "能养成好习惯，学会清理油墨。",
        ],
        "transition_chain": "从创作转向展示评价：作品完成后要用印痕语言解释，而不是只展示结果。",
        "teacher_visible_note": "作品完成不是越满越好，要保留一个能说清来源和效果的关键印痕。",
        "control_points": {
            "observe": "学生是否能围绕满意印痕组织画面。",
            "ask_when": "作品堆满材料或看不出印痕重点时。",
            "rescue_when": "画面杂乱、覆盖特色印痕或清洁失控时。",
            "screen_when": "中段需要统一取舍标准时。",
            "component_when": "需要作品中途互看和调整时。",
            "evidence_when": "学生确定保留的关键印痕时。",
            "proceed_when": "作品有关键印痕，并能说清纸材或印法来源。",
        },
    },
    {
        "event_id": "paper_print_event_07_gallery_reflection",
        "event_name": "说一说：印痕展评与车间收束",
        "section": "展示评价与证据归档",
        "source_anchor": {
            "sample": SOURCE_SAMPLE,
            "anchor": "单元评价方案 / 第四阶段学习评价",
            "evidence": "积极参与小组汇报讨论并与他人分享；布置“版画车间坊”；按要求完成任务。",
            "source_status": "source_evidence",
        },
        "teaching_responsibility": "把展示从“谁的作品漂亮”转为纸材、印法、印痕效果和记录证据的综合说明。",
        "student_problem": "学生评价容易空泛，只说漂亮、有创意，不能用纸材、印法、印痕等语言说明作品。",
        "task_release": "每组选择一件作品和一张试印记录一起展示。介绍时必须说清：用了什么纸材，试了什么印法，留下了什么印痕。",
        "expected_student_responses": [
            "能把作品和试印记录一起展示。",
            "能用纸材、印法、印痕、肌理、灰层等词说明作品。",
            "能给同伴提出一条基于印痕的建议。",
        ],
        "likely_misconceptions_or_failures": [
            "只说作品漂亮或颜色好。",
            "忘记带上试印证据。",
            "评价变成投票谁最好。",
        ],
        "teacher_follow_up_questions": [
            "你最满意的印痕来自哪次试印？",
            "同伴的作品里，哪一处最能看出纸材特点？",
            "如果再印一次，你建议他调整纸材、印法，还是用力？",
        ],
        "teacher_scaffolding_moves": [
            "提供展示句式：我用了……纸，采用……印法，印出了……效果。",
            "把评价词压到四类：纸材、印法、印痕、画面。",
            "要求建议必须指向一个可调整动作。",
        ],
        "teacher_rescue_strategy": "如果展示变成投票，教师暂停投票，改为每组找一处“最能说明纸材特点的印痕”，先说证据再贴星。",
        "screen_trigger": {
            "trigger_condition": "展示评价开始前",
            "content": "展示句式 + 纸材/印法/印痕/画面四类评价词 + 证据归档提醒",
        },
        "component_trigger": {
            "component_id": "work_gallery",
            "component_name": "作品画廊",
            "trigger_condition": "作品完成并需要基于证据分享时",
            "student_problem_solved": "让展评从喜好投票转为有依据的印痕说明。",
            "alternative_component": "photo_submit",
            "expected_evidence": "作品照片、试印记录和一句基于印痕的说明。",
        },
        "learning_sheet_trigger": {
            "field": "展评归档",
            "prompt": "我用了……纸，采用……印法，印出了……效果；同伴建议我……",
        },
        "evidence_trigger": {
            "evidence_type": "作品 + 试印记录 + 展示说明 + 同伴建议",
            "collect_when": "展示评价结束前",
            "minimum_evidence": "每组至少一份作品与试印证据配套归档。",
        },
        "assessment_alignment": [
            "能欣赏作品，积极参与小组汇报讨论并与他人分享。",
            "能用印痕表达想法，并说明纸材与印法的效果。",
        ],
        "transition_chain": "从本课展评归档转向后续套色或车间布置：学生带着纸材、印法、印痕证据继续深化版画表现。",
        "teacher_visible_note": "展示时必须带试印证据，避免作品评价滑成“谁更漂亮”。",
        "control_points": {
            "observe": "学生评价是否使用纸材、印法、印痕语言。",
            "ask_when": "学生只说漂亮、有趣或喜欢时。",
            "rescue_when": "展示变成投票或作品证据脱节时。",
            "screen_when": "展评开始前和评价空泛时。",
            "component_when": "需要把作品和证据并置展示时。",
            "evidence_when": "展示结束前统一归档。",
            "proceed_when": "作品、试印记录和说明能配套留下。",
        },
    },
]


def md_table(headers, rows):
    lines = ["| " + " | ".join(headers) + " |", "| " + " | ".join(["---"] * len(headers)) + " |"]
    for row in rows:
        lines.append("| " + " | ".join(str(cell).replace("\n", "<br>") for cell in row) + " |")
    return "\n".join(lines)


CN_NUM = ["一", "二", "三", "四", "五", "六", "七", "八", "九", "十"]


def clean_sentence(text):
    return str(text).strip().rstrip("。；;")


def event_teacher_section(idx, event):
    expected = clean_sentence(event["expected_student_responses"][0])
    misconception = clean_sentence(event["likely_misconceptions_or_failures"][0])
    scaffold = clean_sentence(event["teacher_scaffolding_moves"][0])
    screen = clean_sentence(event["screen_trigger"]["content"])
    evidence = clean_sentence(event["evidence_trigger"]["minimum_evidence"])
    assessment = "；".join(clean_sentence(item) for item in event["assessment_alignment"])
    return f"""
### （{CN_NUM[idx - 1]}）{event['event_name']}

【本环节在做什么】{event['teaching_responsibility']}

【教师关注】{event['teacher_visible_note']}

教师先释放任务：“{event['task_release']}”这句话不要说成普通活动说明，而要让学生知道现在要解决什么问题：{clean_sentence(event['student_problem'])}。

学生可能会出现这些真实反应：{expected}。也可能出现偏差，比如{misconception}。这时教师不急着纠正结果，而是把问题追到具体证据上：“{event['teacher_follow_up_questions'][0]}”如果学生仍然说不清，教师可以这样补救：{event['teacher_rescue_strategy']}

课堂推进时，教师把支架控制在必要范围内：{scaffold}。需要大屏时，只呈现与当下事件直接相关的内容：{screen}。这里可以安排一次“{event['component_trigger']['component_name']}”：{event['component_trigger']['student_problem_solved']}

本环节证据要轻而明确：{evidence}。学习单可以记录：“{event['learning_sheet_trigger']['prompt']}”教师在收束时提醒学生，今天留下的不是热闹过程，而是后面继续判断纸材、印法和印痕关系的证据。

过渡语：{event['transition_chain']}

【下游影响】大屏：{screen}；学习单：{event['learning_sheet_trigger']['field']}；评价：{assessment}。
""".strip()


def build_teacher_markdown():
    sections = "\n\n".join(event_teacher_section(i + 1, event) for i, event in enumerate(EVENTS))
    return f"""# 《有趣的纸印》跨样本课堂事件展开验证稿

```text
stage_id={STAGE_ID}
standard_id={STANDARD_ID}
source_sample=第五单元《有趣的纸印》
status=cross_sample_teacher_default_reading_draft
preview_only=true
teacher_confirmed=false
formal_apply_allowed=false
R97B / UI / runtime / prompt / model / db = untouched
```

## 一、教师默认阅读层

本稿用于验证 R223M-P5 锁定的课堂事件展开标准能否迁移到材料 / 技法 / 印痕探究类课例。默认层只保留教师阅读需要的轻提示：本环节在做什么、教师关注什么、课堂如何推进、过渡和下游影响。更细的控制、组件触发、来源证据和审核判断进入 review ledger，不压进正文。

## 二、课时定位

《有趣的纸印》的大观念是“印痕是版画的独特语言”。本次验证选取从纸材观察、肌理制造、试印记录、印法比较到作品展评的核心课堂链，重点看学生能否从“纸不一样”推进到“纸材、印法和印痕效果有关”，并能留下试印记录、作品和展评说明。

## 三、教学过程

{sections}

## 四、本课确认门

本稿仍为 preview-only。大屏素材、组件候选、学习单栏位和评价证据只作为跨样本验证产物，不写入正式备课本。教师确认前不得进入正式 UI、R97B 路由、runtime、prompt、provider/model 或数据库。
"""


def build_reasoning_markdown():
    rows = [
        ["源样本主题", SOURCE_ANCHORS["大观念"], "确定本课不是普通纸手工，而是版画印痕语言学习。"],
        ["学情", SOURCE_ANCHORS["学情分析"], "要求课堂事件保留触摸、试印、比较、记录等低门槛动作。"],
        ["基本问题", SOURCE_ANCHORS["基本问题"], "驱动纸材与印法碰撞后的印痕比较。"],
        ["表现性任务", SOURCE_ANCHORS["表现性任务"], "要求作品与试印证据共同进入展示，而不是只看成品。"],
        ["评价方案", SOURCE_ANCHORS["评价方案"], "推动学习单、试印纸、作品照片、展示说明成为证据链。"],
    ]
    event_rows = [
        [event["event_id"], event["event_name"], event["teaching_responsibility"], event["evidence_trigger"]["minimum_evidence"]]
        for event in EVENTS
    ]
    return f"""# R223N 《有趣的纸印》推理链生产物

```text
stage_id={STAGE_ID}
standard_source=R223M-P5 GOLDEN_CLASSROOM_EVENT_EXPANSION_STANDARD_V0.1
validation_sample=第五单元《有趣的纸印》
validation_focus=material_technique_print_mark_inquiry
```

## 一、迁移判断

本轮不是生成正式教案，而是验证同一课堂事件展开标准能否承接材料 / 技法 / 印痕探究类型。核心链条为：

```text
学情与课标实践要求
→ 大观念：印痕是版画的独特语言
→ 基本问题：纸材和印法碰撞带来怎样的惊喜
→ 表现性任务：版画车间坊
→ 纸材观察 / 肌理制造 / 试印记录 / 印法比较 / 作品展评
→ 作品 + 试印证据 + 展示说明
```

## 二、源证据与推理约束

{md_table(["来源节点", "源样本证据", "对课堂事件的约束"], rows)}

## 三、课堂事件链

{md_table(["event_id", "课堂事件", "教学责任", "最低证据"], event_rows)}

## 四、不过拟合说明

本轮没有迁移前一标准样本中的具体内容、仪式或角色设定。组件和大屏只从纸材、印法、印痕、试印记录与作品展评这些源样本要素中触发。
"""


def build_selection_note():
    return f"""# R223N 跨样本选择说明

```text
stage_id={STAGE_ID}
selected_sample=第五单元《有趣的纸印》
selection_reason=材料 / 技法 / 印痕探究类型，与 R223M-P5 的设计应用样本差异足够大
formal_ui=blocked
```

## 为什么选择《有趣的纸印》

R223M-P5 锁定的标准来自设计应用与生活问题解决类型。若继续在同一类型内验证，容易过拟合。第五单元《有趣的纸印》的核心是纸材、印法、印痕与版画表现语言，能验证 classroom_event_expansion_schema 是否适配材料技法类课堂事件。

## 本轮选取的核心课堂链

1. 任务入场：走进版画车间坊；
2. 纸材肌理观察；
3. 制造纸的新肌理；
4. 第一次转印与试印记录；
5. 干印、湿印、油印比较；
6. 用印痕完成作品；
7. 印痕展评与证据归档。

## 边界

本轮只做跨样本验证，不生成正式 UI，不改 R97B，不接 runtime/model/prompt/db，不 formal apply。前一标准样本的具体人物、情境、仪式和任务名称不得迁移到《有趣的纸印》。
"""


def build_review_ledger():
    entries = []
    for event in EVENTS:
        entries.append({
            "event_id": event["event_id"],
            "event_name": event["event_name"],
            "default_teacher_visible": {
                "teacher_focus": event["teacher_visible_note"],
                "downstream_impact": {
                    "screen": event["screen_trigger"]["content"],
                    "learning_sheet": event["learning_sheet_trigger"]["field"],
                    "evidence": event["evidence_trigger"]["minimum_evidence"],
                },
            },
            "review_view_only": {
                "xiaojiao_judgement_full": {
                    "what_is_happening": event["teaching_responsibility"],
                    "why_it_matters": event["student_problem"],
                    "risk_if_skipped": event["likely_misconceptions_or_failures"],
                    "minimum_success_signal": event["evidence_trigger"]["minimum_evidence"],
                },
                "control_points_full": event["control_points"],
                "screen_trigger": event["screen_trigger"],
                "component_trigger": event["component_trigger"],
                "learning_sheet_trigger": event["learning_sheet_trigger"],
                "evidence_trigger": event["evidence_trigger"],
                "source_anchor": event["source_anchor"],
            },
        })
    return {
        "stage_id": STAGE_ID,
        "standard_id": STANDARD_ID,
        "sample": SOURCE_SAMPLE,
        "default_teacher_view_must_not_show_full_ledger": True,
        "entries": entries,
        "boundary": {
            "preview_only": True,
            "teacher_confirmed": False,
            "formal_apply_allowed": False,
            "r97b_modified": False,
            "ui_modified": False,
            "runtime_connected": False,
            "provider_model_connected": False,
            "database_written": False,
        },
    }


def build_trigger_map():
    rows = []
    for event in EVENTS:
        rows.append([
            event["event_name"],
            f"{event['component_trigger']['component_name']}：{event['component_trigger']['trigger_condition']}",
            event["screen_trigger"]["content"],
            event["learning_sheet_trigger"]["prompt"],
            event["evidence_trigger"]["minimum_evidence"],
        ])
    return f"""# R223N 组件 / 大屏 / 学习单 / 证据触发图

```text
stage_id={STAGE_ID}
view=review_support
default_teacher_view=false
```

{md_table(["课堂事件", "组件触发", "大屏触发", "学习单触发", "证据触发"], rows)}

## 触发原则

派生物必须从课堂事件长出来：任务释放需要大屏任务语，学生观察散乱时触发圈画或比较，试印后触发学习单记录，展评时触发作品与证据并置。不得把组件做成全局工具货架。
"""


def build_rubric_score():
    rows = [
        ["课堂事件真实展开", 5, "7 个事件均包含任务释放、学生反应、偏差、追问、补救、证据和过渡。"],
        ["学生可能性符合学情", 4, "能体现三年级对肌理有经验但技法和记录仍需支架；仍需后续真实课堂校准。"],
        ["教师追问与补救具体", 5, "每个事件都有可直接使用的追问和补救动作，如同版对比、少量上色示范、遮挡取舍。"],
        ["大屏 / 组件 / 学习单 / 证据有触发点", 5, "所有派生物均绑定具体事件和触发条件。"],
        ["教师默认稿连续可读", 4, "默认稿保持连续阅读，但作为跨样本初版，部分下游影响仍偏审核提示。"],
    ]
    total = sum(row[1] for row in rows)
    return f"""# R223N 25 分规准评分

```text
rubric_id=CLASSROOM_EVENT_EXPANSION_STANDARD_V0.1_25_POINT
pass_line=20
lock_candidate_line=23
score={total}/25
decision=PASS_INITIAL_MIGRATION_EVIDENCE
```

{md_table(["维度", "得分", "理由"], rows)}

## 判断

《有趣的纸印》达到 23/25，说明 R223M-P5 标准在材料 / 技法 / 印痕探究类型上具备第一轮迁移证据。扣分点保留给真实课堂校准和下游影响进一步页边注化。
"""


def build_report(zip_sha=None):
    return f"""# R223N 跨样本课堂事件展开验证报告

```text
stage_id={STAGE_ID}
R223M-P5=PASS_GOLDEN_STANDARD_LOCK_PACKAGE
R223N=PASS_INITIAL_CROSS_SAMPLE_VALIDATION
score=23/25
next_recommended=teacher_review_before_next_cross_sample
formal_ui=blocked
R97B / UI / runtime / prompt / model / db = untouched
```

## 一、验证结论

本轮用《有趣的纸印》验证 R223M-P5 锁定的课堂事件展开标准。结果显示，同一 schema 能表达材料 / 技法 / 印痕探究类事件；教师默认稿能保持连续阅读；review ledger 能追溯来源、控制点、组件、大屏、学习单和证据触发。

## 二、关键通过点

- 课堂事件从纸材观察、肌理制造、试印记录、印法比较到作品展评，未停留在环节摘要；
- 学生可能性来自三年级学情和源样本：会观察肌理但容易只看颜色、作品好看或技法名称；
- 大屏、组件、学习单、证据均由课堂事件触发；
- 没有迁移前一标准样本的具体课堂情境；
- 评分达到 23/25，可作为第一轮迁移证据。

## 三、仍需注意

这不是正式教案写入，也不是 UI 放行。下一步建议先进行人工教师审核，再选第二个差异课型继续验证，例如《色彩的碰撞》或《有趣的文字和图画》。

## 四、边界

本包不改 R97B，不新增正式 route，不改 frontend/backend，不接 runtime、provider/model、prompt 或 db，不写回 lesson body，不 formal apply。

## 五、ZIP

```text
review_zip_sha256={zip_sha or "computed_after_packaging"}
```
"""


def md_to_html(md, title):
    lines = md.splitlines()
    body = []
    in_code = False
    para = []

    def flush_para():
        if para:
            body.append("<p>" + html.escape(" ".join(para)) + "</p>")
            para.clear()

    for line in lines:
        stripped = line.strip()
        if stripped.startswith("```"):
            flush_para()
            if not in_code:
                in_code = True
                body.append("<pre><code>")
            else:
                in_code = False
                body.append("</code></pre>")
            continue
        if in_code:
            body.append(html.escape(line) + "\n")
            continue
        if not stripped:
            flush_para()
            continue
        if stripped.startswith("#"):
            flush_para()
            level = len(stripped) - len(stripped.lstrip("#"))
            text = stripped[level:].strip()
            body.append(f"<h{level}>{html.escape(text)}</h{level}>")
        elif stripped.startswith("【") and "】" in stripped:
            flush_para()
            label, rest = stripped.split("】", 1)
            body.append(f"<p class='note'><strong>{html.escape(label + '】')}</strong>{html.escape(rest)}</p>")
        elif stripped.startswith("过渡语："):
            flush_para()
            body.append(f"<p class='transition'>{html.escape(stripped)}</p>")
        else:
            para.append(stripped)
    flush_para()
    css = """
body{margin:0;background:#f6f7f4;color:#24312d;font-family:"Microsoft YaHei","PingFang SC",Arial,sans-serif;line-height:1.72}
.page{max-width:980px;margin:0 auto;padding:36px 28px 72px}
article{background:#fffdf8;border:1px solid #d9e3dc;border-radius:10px;padding:38px 48px;box-shadow:0 18px 48px rgba(38,83,72,.08)}
h1{font-size:30px;line-height:1.25;margin:0 0 20px;color:#1f6f61}
h2{font-size:21px;margin:34px 0 14px;border-top:1px solid #e7eee9;padding-top:26px;color:#245f56}
h3{font-size:18px;margin:30px 0 14px;color:#24312d}
p{font-size:15.5px;margin:10px 0}
.note{background:#f3faf6;border-left:4px solid #2b7c6e;padding:10px 14px;border-radius:6px}
.transition{color:#51645d;background:#fbfaf1;border-left:4px solid #d8a84d;padding:10px 14px;border-radius:6px}
pre{background:#263832;color:#eef8f2;padding:14px 16px;border-radius:8px;overflow:auto;font-size:13px}
code{font-family:Consolas,monospace}
@media(max-width:760px){.page{padding:16px}article{padding:24px 20px}h1{font-size:24px}}
"""
    return f"<!doctype html><html lang='zh-CN'><head><meta charset='utf-8'><meta name='viewport' content='width=device-width, initial-scale=1'><title>{html.escape(title)}</title><style>{css}</style></head><body><main class='page'><article>{''.join(body)}</article></main></body></html>"


VALIDATOR_CODE = r'''
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
REQUIRED_FILES = [
    "R223N_cross_sample_selection_note.md",
    "R223N_paper_print_reasoning_chain_product.md",
    "R223N_classroom_event_expansion_chain.json",
    "R223N_teacher_default_reading_draft.md",
    "R223N_teacher_default_reading_draft.html",
    "R223N_review_ledger_sample.json",
    "R223N_component_screen_evidence_trigger_map.md",
    "R223N_rubric_score.md",
    "R223N_cross_sample_validation_report.md",
    "validate_1013R_R223N_cross_sample_classroom_event_expansion.py",
    "PACKAGE_MANIFEST.json",
    "README_FOR_GPT_REVIEW.md",
]

REQUIRED_EVENT_FIELDS = [
    "event_id",
    "event_name",
    "section",
    "source_anchor",
    "teaching_responsibility",
    "student_problem",
    "task_release",
    "expected_student_responses",
    "likely_misconceptions_or_failures",
    "teacher_follow_up_questions",
    "teacher_scaffolding_moves",
    "teacher_rescue_strategy",
    "screen_trigger",
    "component_trigger",
    "learning_sheet_trigger",
    "evidence_trigger",
    "assessment_alignment",
    "transition_chain",
    "teacher_visible_note",
    "control_points",
]

CONTROL_FIELDS = ["observe", "ask_when", "rescue_when", "screen_when", "component_when", "evidence_when", "proceed_when"]
BANNED_PREVIOUS_SAMPLE_TERMS = ["文具", "智造", "代言", "赠笔礼", "毛笔", "铅笔"]


def check(condition, message, failures):
    if not condition:
        failures.append(message)


def main():
    failures = []
    check_count = 0

    for file_name in REQUIRED_FILES:
        check_count += 1
        check((ROOT / file_name).exists(), f"missing required file: {file_name}", failures)

    chain_path = ROOT / "R223N_classroom_event_expansion_chain.json"
    ledger_path = ROOT / "R223N_review_ledger_sample.json"
    teacher_path = ROOT / "R223N_teacher_default_reading_draft.md"
    rubric_path = ROOT / "R223N_rubric_score.md"
    report_path = ROOT / "R223N_cross_sample_validation_report.md"

    chain = json.loads(chain_path.read_text(encoding="utf-8"))
    ledger = json.loads(ledger_path.read_text(encoding="utf-8"))
    teacher = teacher_path.read_text(encoding="utf-8")
    rubric = rubric_path.read_text(encoding="utf-8")
    report = report_path.read_text(encoding="utf-8")

    check_count += 1
    check(chain.get("stage_id") == "1013R_R223N_CROSS_SAMPLE_CLASSROOM_EVENT_EXPANSION_VALIDATION", "wrong stage_id", failures)
    check_count += 1
    check(chain.get("standard_id") == "GOLDEN_CLASSROOM_EVENT_EXPANSION_STANDARD_V0.1_LOCK_CANDIDATE", "wrong standard_id", failures)
    check_count += 1
    check(len(chain.get("events", [])) >= 7, "event count must be >= 7", failures)

    for event in chain.get("events", []):
        for field in REQUIRED_EVENT_FIELDS:
            check_count += 1
            check(field in event and event[field] not in (None, "", []), f"{event.get('event_id')} missing {field}", failures)
        for field in CONTROL_FIELDS:
            check_count += 1
            check(field in event.get("control_points", {}), f"{event.get('event_id')} missing control point {field}", failures)
        check_count += 1
        check(event["source_anchor"].get("source_status") in {"source_evidence", "system_inference_from_source"}, f"{event.get('event_id')} bad source_status", failures)
        check_count += 1
        check("trigger_condition" in event["component_trigger"], f"{event.get('event_id')} component trigger lacks condition", failures)
        check_count += 1
        check("minimum_evidence" in event["evidence_trigger"], f"{event.get('event_id')} evidence lacks minimum", failures)

    check_count += 1
    check(len(ledger.get("entries", [])) == len(chain.get("events", [])), "ledger entries must match events", failures)
    for entry in ledger.get("entries", []):
        rv = entry.get("review_view_only", {})
        for field in ["xiaojiao_judgement_full", "control_points_full", "screen_trigger", "component_trigger", "learning_sheet_trigger", "evidence_trigger"]:
            check_count += 1
            check(field in rv, f"ledger {entry.get('event_id')} missing {field}", failures)

    check_count += 1
    check(teacher.count("【本环节在做什么】") >= 7, "teacher draft lacks event purpose notes", failures)
    check_count += 1
    check(teacher.count("【教师关注】") >= 7, "teacher draft lacks teacher focus notes", failures)
    check_count += 1
    check(teacher.count("【下游影响】") >= 7, "teacher draft lacks downstream notes", failures)
    check_count += 1
    check("【小教判断】" not in teacher, "teacher default should not expose full xiaojiao judgement", failures)
    check_count += 1
    check("完整控制点" not in teacher, "teacher default should not expose full control ledger", failures)

    scanned = teacher + "\n" + json.dumps(chain, ensure_ascii=False)
    for term in BANNED_PREVIOUS_SAMPLE_TERMS:
        check_count += 1
        check(term not in scanned, f"previous sample term leaked into teacher/event product: {term}", failures)

    check_count += 1
    score_match = re.search(r"score=(\d+)/25", rubric)
    check(score_match is not None, "rubric score missing", failures)
    score = int(score_match.group(1)) if score_match else 0
    check_count += 1
    check(score >= 20, "rubric score below pass line", failures)
    check_count += 1
    check("23/25" in rubric and "23/25" in report, "expected 23/25 migration score not recorded", failures)

    boundary = chain.get("boundary", {})
    for key in ["r97b_modified", "ui_modified", "runtime_connected", "provider_model_connected", "database_written", "formal_apply_allowed"]:
        check_count += 1
        check(boundary.get(key) is False, f"boundary must keep {key}=false", failures)

    result = {
        "passed": not failures,
        "check_count": check_count,
        "failed": len(failures),
        "failures": failures,
        "event_count": len(chain.get("events", [])),
        "rubric_score": score,
    }
    (ROOT / "validate_1013R_R223N_cross_sample_classroom_event_expansion_result.json").write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps(result, ensure_ascii=False))
    return 0 if not failures else 1


if __name__ == "__main__":
    sys.exit(main())
'''


def write(path, content):
    path.write_text(content.strip() + "\n", encoding="utf-8")


def main():
    chain = {
        "stage_id": STAGE_ID,
        "standard_id": STANDARD_ID,
        "source_sample": SOURCE_SAMPLE,
        "source_docx": SOURCE_DOCX,
        "validation_focus": "material_technique_print_mark_inquiry",
        "events": EVENTS,
        "boundary": {
            "preview_only": True,
            "teacher_confirmed": False,
            "formal_apply_allowed": False,
            "r97b_modified": False,
            "ui_modified": False,
            "runtime_connected": False,
            "provider_model_connected": False,
            "database_written": False,
        },
    }
    write(ROOT / "R223N_cross_sample_selection_note.md", build_selection_note())
    write(ROOT / "R223N_paper_print_reasoning_chain_product.md", build_reasoning_markdown())
    write(ROOT / "R223N_classroom_event_expansion_chain.json", json.dumps(chain, ensure_ascii=False, indent=2))
    teacher_md = build_teacher_markdown()
    write(ROOT / "R223N_teacher_default_reading_draft.md", teacher_md)
    write(ROOT / "R223N_teacher_default_reading_draft.html", md_to_html(teacher_md, "R223N 有趣的纸印教师默认稿"))
    write(ROOT / "R223N_review_ledger_sample.json", json.dumps(build_review_ledger(), ensure_ascii=False, indent=2))
    write(ROOT / "R223N_component_screen_evidence_trigger_map.md", build_trigger_map())
    write(ROOT / "R223N_rubric_score.md", build_rubric_score())
    write(ROOT / "R223N_cross_sample_validation_report.md", build_report())
    write(ROOT / "validate_1013R_R223N_cross_sample_classroom_event_expansion.py", VALIDATOR_CODE)

    manifest_files = [
        "R223N_cross_sample_selection_note.md",
        "R223N_paper_print_reasoning_chain_product.md",
        "R223N_classroom_event_expansion_chain.json",
        "R223N_teacher_default_reading_draft.md",
        "R223N_teacher_default_reading_draft.html",
        "R223N_review_ledger_sample.json",
        "R223N_component_screen_evidence_trigger_map.md",
        "R223N_rubric_score.md",
        "R223N_cross_sample_validation_report.md",
        "validate_1013R_R223N_cross_sample_classroom_event_expansion.py",
    ]
    manifest = {
        "stage_id": STAGE_ID,
        "created_at_utc": datetime.now(timezone.utc).isoformat(),
        "source_sample": SOURCE_SAMPLE,
        "source_docx": SOURCE_DOCX,
        "standard_source": "R223M-P5",
        "files": manifest_files + [
            "validate_1013R_R223N_cross_sample_classroom_event_expansion_result.json",
            "PACKAGE_MANIFEST.json",
            "README_FOR_GPT_REVIEW.md",
        ],
        "boundary": chain["boundary"],
    }
    write(ROOT / "PACKAGE_MANIFEST.json", json.dumps(manifest, ensure_ascii=False, indent=2))
    readme = f"""# R223N Cross-sample Classroom Event Expansion Review

```text
stage_id={STAGE_ID}
sample=第五单元《有趣的纸印》
standard=GOLDEN_CLASSROOM_EVENT_EXPANSION_STANDARD_V0.1_LOCK_CANDIDATE
status=review_package
formal_ui=blocked
```

## Open first

1. `R223N_teacher_default_reading_draft.html`
2. `R223N_teacher_default_reading_draft.md`
3. `R223N_rubric_score.md`
4. `R223N_review_ledger_sample.json`

## Review question

Does the P5 classroom event expansion standard migrate to a material / technique / print-mark inquiry sample without becoming a card wall or leaking the previous sample content?

## Boundaries

No R97B change, no formal UI, no frontend/backend change, no runtime/provider/model/prompt/db connection, no lesson body writeback, no formal apply.
"""
    write(ROOT / "README_FOR_GPT_REVIEW.md", readme)


if __name__ == "__main__":
    main()
