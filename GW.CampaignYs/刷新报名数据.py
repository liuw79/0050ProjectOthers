#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Q2 AI化课程 · 报名数据刷新工具

用法：
    python3 刷新报名数据.py          # 刷新数据并生成报告
    python3 刷新报名数据.py --dry-run  # 只预览，不写文件

数据保护机制：
    - DB字段（姓名、公司、职务等）每次从数据库拉取，自动更新
    - 手动列（创始人_手动、备注）按「学友ID+班级ID」匹配保留，永不覆盖
    - 新增学友：手动列为空，等你填
    - 退课学友：保留在CSV底部，标记「已退课」
"""

import pymssql
import csv
import os
import sys
from datetime import datetime
from collections import defaultdict, Counter
from pathlib import Path

# ========== 配置 ==========

DB_CONFIG = {
    'server': '47.115.38.118',
    'port': 9024,
    'user': 'gw_reader',
    'password': 'cZ1cM5nX5eX7',
    'database': 'GW_Course',
    'login_timeout': 30,
    'charset': 'utf8',
}

# Q2 AI化课程 → 对应的排期ActivityID
# 如需增减课程，在这里改
TARGET_COURSES = {
    '品牌增长与全域营销': {
        'activity_id': 'd24cb69b-020f-412c-b863-6b45f5b6ab2a',
        'date': '4/18-19', 'city': '深圳', 'type': '操作型',
    },
    'GTM产品市场协同作战': {
        'activity_id': '4a8e8a95-a65f-4167-ab3b-2af7fdb8fe44',
        'date': '5/9-10', 'city': '深圳', 'type': '操作型',
    },
    '超级转化率': {
        'activity_id': '07ab2b5c-4a85-4342-927c-31eaae54492d',
        'date': '5/16-17', 'city': '深圳', 'type': '操作型',
    },
    '流程型组织': {
        'activity_id': 'e2a24789-46aa-4f62-9a66-32233d0ce80e',
        'date': '5/16-17', 'city': '广州', 'type': '理论型',
    },
    '人人都是自己的CEO': {
        'activity_id': '5b068565-3aaa-44eb-a889-34a958ef5be9',
        'date': '5/16-17', 'city': '深圳', 'type': '通用型',
    },
    '科学分钱': {
        'activity_id': 'd2c80401-7751-458b-b651-0c9e21b60250',
        'date': '5/23-24', 'city': '广州', 'type': '混合型',
    },
    '战略设计总纲课': {
        'activity_id': '7851c6e1-90b6-43ff-b70a-9e899c945ebd',
        'date': '5/23-24', 'city': '深圳', 'type': '理论型',
    },
    '业务领先战略': {
        'activity_id': '3f164116-6f88-4944-9022-be345fdd4bbd',
        'date': '6/6-7', 'city': '上海', 'type': '理论型',
    },
}

# 文件路径
SCRIPT_DIR = Path(__file__).parent
CSV_FILE = SCRIPT_DIR / '报名数据.csv'
REPORT_FILE = SCRIPT_DIR / 'Q2课程报名学友分析.md'

# CSV 列定义
# DB列：每次刷新自动覆盖
DB_COLUMNS = ['课程简称', '日期', '城市', '开课地址', '班主任', '课程类型', '姓名', '公司', '职务', '是否创始人_系统', '年级', '下单时间', '渠道']
# 键列：用于匹配新旧数据
KEY_COLUMNS = ['学友ID', '班级ID']
# 手动列：永不覆盖（你可以自行增加列，脚本会自动保留）
MANUAL_COLUMNS = ['创始人_手动', '备注']
# 状态列
STATUS_COLUMN = '状态'

ALL_COLUMNS = KEY_COLUMNS + DB_COLUMNS + [STATUS_COLUMN] + MANUAL_COLUMNS


# ========== 数据库查询 ==========

def fetch_from_db():
    """从数据库拉取最新报名数据 + 班主任 + 开课地址"""
    conn = pymssql.connect(**DB_CONFIG)
    cursor = conn.cursor(as_dict=True)

    activity_ids = [v['activity_id'] for v in TARGET_COURSES.values()]
    placeholders = ','.join([f"'{aid}'" for aid in activity_ids])

    # 1. 报名学友
    sql = f"""
    SELECT
        CONVERT(varchar(36), v.LearnerID) as LearnerID,
        CONVERT(varchar(36), v.activityid) as ActivityID,
        v.课程,
        v.排期,
        v.开课日期,
        v.城市,
        v.上课人,
        v.上课人公司,
        v.上课人职务,
        v.是否创始人,
        v.年级,
        v.下单时间,
        v.渠道
    FROM view_orders_cache v
    WHERE v.activityid IN ({placeholders})
    ORDER BY v.开课日期, v.课程, v.下单时间
    """
    cursor.execute(sql)
    rows = cursor.fetchall()

    # 2. 班主任（ClassTeacher表）
    sql_teacher = f"""
    SELECT CONVERT(varchar(36), ct.ActivityID) as ActivityID, ct.Name as 班主任
    FROM ClassTeacher ct
    WHERE ct.ActivityID IN ({placeholders})
    """
    cursor.execute(sql_teacher)
    teacher_map = {}
    for t in cursor.fetchall():
        aid = t['ActivityID'].lower() if t['ActivityID'] else ''
        teacher_map[aid] = t['班主任'] or ''

    # 3. 开课地址（TranActivity表）
    sql_addr = f"""
    SELECT CONVERT(varchar(36), ta.ID) as ActivityID,
           ta.Info_Address as 城市,
           ta.FullAddress as 详细地址
    FROM TranActivity ta
    WHERE ta.ID IN ({placeholders})
    """
    cursor.execute(sql_addr)
    addr_map = {}
    for a in cursor.fetchall():
        aid = a['ActivityID'].lower() if a['ActivityID'] else ''
        addr_map[aid] = a['详细地址'] or a['城市'] or ''

    conn.close()
    return rows, teacher_map, addr_map


def normalize_course_name(full_name):
    """将数据库中的完整课程名映射为简称"""
    for short_name in TARGET_COURSES:
        if short_name in full_name:
            return short_name
    return full_name


# ========== CSV 读写（保护手动列） ==========

def load_existing_csv():
    """读取现有CSV，返回 {(学友ID, 班级ID): {列名: 值}} 的字典"""
    if not CSV_FILE.exists():
        return {}, []

    existing = {}
    extra_manual_cols = []  # 用户可能自己加的列
    with open(CSV_FILE, 'r', encoding='utf-8-sig') as f:
        reader = csv.DictReader(f)
        if reader.fieldnames:
            # 发现用户新增的列（不在预定义列中的），也要保留
            extra_manual_cols = [c for c in reader.fieldnames if c not in ALL_COLUMNS]
        for row in reader:
            key = (row.get('学友ID', ''), row.get('班级ID', ''))
            if key[0] and key[1]:
                existing[key] = row
    return existing, extra_manual_cols


def save_csv(rows, extra_manual_cols=None):
    """保存CSV"""
    columns = ALL_COLUMNS + (extra_manual_cols or [])
    with open(CSV_FILE, 'w', encoding='utf-8-sig', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=columns, extrasaction='ignore')
        writer.writeheader()
        for row in rows:
            writer.writerow(row)


def merge_data(db_rows, existing_data, extra_manual_cols, teacher_map=None, addr_map=None):
    """
    合并数据库新数据和CSV中的手动标注
    返回合并后的行列表
    """
    teacher_map = teacher_map or {}
    addr_map = addr_map or {}
    merged = []
    seen_keys = set()
    manual_cols_to_preserve = MANUAL_COLUMNS + extra_manual_cols

    for db_row in db_rows:
        course_short = normalize_course_name(db_row['课程'] or '')
        course_info = TARGET_COURSES.get(course_short, {})
        activity_id = db_row['ActivityID'].lower() if db_row['ActivityID'] else ''

        key = (db_row['LearnerID'] or '', activity_id)
        seen_keys.add(key)

        # DB字段（每次刷新）
        row = {
            '学友ID': db_row['LearnerID'] or '',
            '班级ID': activity_id,
            '课程简称': course_short,
            '日期': course_info.get('date', ''),
            '城市': db_row['城市'] or course_info.get('city', ''),
            '开课地址': addr_map.get(activity_id, ''),
            '班主任': teacher_map.get(activity_id, ''),
            '课程类型': course_info.get('type', ''),
            '姓名': db_row['上课人'] or '',
            '公司': db_row['上课人公司'] or '',
            '职务': db_row['上课人职务'] or '',
            '是否创始人_系统': '是' if db_row['是否创始人'] == 1 else '',
            '年级': db_row['年级'] or '',
            '下单时间': db_row['下单时间'].strftime('%Y-%m-%d') if db_row['下单时间'] else '',
            '渠道': db_row['渠道'] or '',
            '状态': '正常',
        }

        # 手动列：从旧数据保留
        old = existing_data.get(key, {})
        for col in manual_cols_to_preserve:
            row[col] = old.get(col, '')

        merged.append(row)

    # 处理退课学友（旧数据中有、新数据中没有的）
    for key, old_row in existing_data.items():
        if key not in seen_keys and old_row.get('状态') != '已退课':
            old_row['状态'] = '已退课'
            merged.append(old_row)

    return merged


# ========== Markdown 报告生成 ==========

def generate_report(rows):
    """从合并后的数据生成Markdown分析报告"""
    active_rows = [r for r in rows if r.get('状态') != '已退课']

    # 按课程分组
    by_course = defaultdict(list)
    for r in active_rows:
        by_course[r['课程简称']].append(r)

    lines = []
    lines.append('# Q2 AI化课程 · 报名学友分析')
    lines.append('')
    lines.append(f'> 数据更新时间：{datetime.now().strftime("%Y-%m-%d %H:%M")}')
    lines.append('> 数据来源：GW_Course数据库 · 由`刷新报名数据.py`自动生成')
    lines.append('> ⚠️ 本文件每次刷新会覆盖，手动标注请改`报名数据.csv`')
    lines.append('')

    # 从数据中提取班主任和地址（取每门课第一条记录的值）
    course_meta = {}
    for r in active_rows:
        cn = r['课程简称']
        if cn not in course_meta:
            course_meta[cn] = {'班主任': r.get('班主任', ''), '开课地址': r.get('开课地址', '')}

    # 总览表
    lines.append('## 总览')
    lines.append('')
    lines.append('| 课程 | 日期 | 城市 | 班主任 | 类型 | 报名 | 创始人 | 企业数 | 团报 |')
    lines.append('|------|------|------|--------|------|------|--------|--------|------|')

    total_count = 0
    total_founders = 0
    for course_name, info in TARGET_COURSES.items():
        students = by_course.get(course_name, [])
        count = len(students)
        total_count += count
        # 创始人：手动标注优先，其次看系统
        founders = sum(1 for s in students if s.get('创始人_手动') == '是' or (not s.get('创始人_手动') and s.get('是否创始人_系统') == '是'))
        total_founders += founders
        companies = set(s['公司'] for s in students if s['公司'])
        company_counter = Counter(s['公司'] for s in students if s['公司'])
        team_buy = sum(1 for c, n in company_counter.items() if n >= 2)
        founder_pct = f"{founders*100//count}%" if count > 0 else '-'
        teacher = course_meta.get(course_name, {}).get('班主任', '')
        lines.append(f'| {course_name} | {info["date"]} | {info["city"]} | {teacher} | {info["type"]} | {count} | {founders}({founder_pct}) | {len(companies)} | {team_buy} |')

    lines.append(f'| **合计** | | | | | **{total_count}** | **{total_founders}** | | |')
    lines.append('')

    # 每门课详情
    for course_name, info in TARGET_COURSES.items():
        students = by_course.get(course_name, [])
        lines.append('---')
        lines.append('')
        meta = course_meta.get(course_name, {})
        teacher = meta.get('班主任', '')
        address = meta.get('开课地址', '')
        lines.append(f'## {course_name}（{info["date"]} {info["city"]}）')
        lines.append('')
        meta_parts = []
        if teacher:
            meta_parts.append(f'班主任：{teacher}')
        if address and address != info['city']:
            meta_parts.append(f'地址：{address}')
        if meta_parts:
            lines.append(' | '.join(meta_parts))
            lines.append('')

        if not students:
            lines.append('暂无报名。')
            lines.append('')
            continue

        count = len(students)
        founders = sum(1 for s in students if s.get('创始人_手动') == '是' or (not s.get('创始人_手动') and s.get('是否创始人_系统') == '是'))
        companies = set(s['公司'] for s in students if s['公司'])
        company_counter = Counter(s['公司'] for s in students if s['公司'])
        team_buy = {k: v for k, v in company_counter.items() if v >= 2}

        lines.append(f'**{count}人 | {len(companies)}家企业 | 创始人{founders}人({founders*100//count}%)**')
        lines.append('')

        if team_buy:
            lines.append('团报企业：' + '、'.join(f'{c}({n}人)' for c, n in sorted(team_buy.items(), key=lambda x: -x[1])))
            lines.append('')

        # 职务分布
        duties = [s['职务'] for s in students if s['职务']]
        if duties:
            duty_counter = Counter(duties)
            top5 = duty_counter.most_common(5)
            lines.append('职务TOP5：' + '、'.join(f'{d}({n})' for d, n in top5))
            lines.append('')

        # 名单
        lines.append('| 姓名 | 公司 | 职务 | 创始人 | 备注 |')
        lines.append('|------|------|------|--------|------|')
        for s in students:
            is_founder = s.get('创始人_手动') or ('✓' if s.get('是否创始人_系统') == '是' else '')
            remark = s.get('备注', '')
            lines.append(f'| {s["姓名"]} | {s["公司"]} | {s["职务"]} | {is_founder} | {remark} |')
        lines.append('')

    # 跨课程企业
    lines.append('---')
    lines.append('')
    lines.append('## 跨课程报名企业')
    lines.append('')

    company_courses = defaultdict(lambda: defaultdict(int))
    for r in active_rows:
        if r['公司']:
            company_courses[r['公司']][r['课程简称']] += 1

    multi_course = {c: courses for c, courses in company_courses.items() if len(courses) >= 2}
    if multi_course:
        lines.append('| 企业 | 跨课详情 | 总人次 |')
        lines.append('|------|----------|--------|')
        for company, courses in sorted(multi_course.items(), key=lambda x: -sum(x[1].values())):
            total = sum(courses.values())
            detail = ' + '.join(f'{c}({n})' for c, n in courses.items())
            lines.append(f'| {company} | {detail} | {total} |')
    lines.append('')

    return '\n'.join(lines)


# ========== 主流程 ==========

def main():
    dry_run = '--dry-run' in sys.argv

    print('📡 连接数据库...')
    db_rows, teacher_map, addr_map = fetch_from_db()
    print(f'   拉取到 {len(db_rows)} 条报名记录')
    for cname, cinfo in TARGET_COURSES.items():
        aid = cinfo['activity_id']
        t = teacher_map.get(aid, '未知')
        a = addr_map.get(aid, '未知')
        print(f'   {cname}: 班主任={t}, 地址={a}')

    print('📂 读取现有CSV...')
    existing_data, extra_cols = load_existing_csv()
    old_count = len(existing_data)
    print(f'   现有 {old_count} 条记录，用户自定义列：{extra_cols or "无"}')

    print('🔀 合并数据（保护手动标注）...')
    merged = merge_data(db_rows, existing_data, extra_cols, teacher_map, addr_map)
    active = [r for r in merged if r.get('状态') != '已退课']
    retired = [r for r in merged if r.get('状态') == '已退课']

    # 统计变化
    new_keys = set((r['学友ID'], r['班级ID']) for r in merged if r['状态'] == '正常')
    old_keys = set(existing_data.keys())
    added = new_keys - old_keys
    removed = old_keys - new_keys

    print(f'   活跃: {len(active)} | 新增: {len(added)} | 退课: {len(retired)}')

    if added:
        print(f'   ➕ 新增学友:')
        for r in merged:
            if (r['学友ID'], r['班级ID']) in added:
                print(f'      {r["课程简称"]} | {r["姓名"]} | {r["公司"]}')

    if removed:
        print(f'   ➖ 退课学友:')
        for r in merged:
            if r['状态'] == '已退课':
                print(f'      {r["课程简称"]} | {r["姓名"]} | {r["公司"]}')

    if dry_run:
        print('\n🏁 dry-run 模式，未写入文件。')
        return

    print('💾 写入CSV...')
    save_csv(merged, extra_cols)
    print(f'   → {CSV_FILE}')

    print('📝 生成分析报告...')
    report = generate_report(merged)
    with open(REPORT_FILE, 'w', encoding='utf-8') as f:
        f.write(report)
    print(f'   → {REPORT_FILE}')

    print(f'\n✅ 完成！共 {len(active)} 条活跃报名。')
    print(f'   编辑手动列请打开: {CSV_FILE.name}')
    print(f'   可编辑的列: {", ".join(MANUAL_COLUMNS + extra_cols)}')
    print(f'   你也可以直接在CSV里新增列，下次刷新会自动保留。')


if __name__ == '__main__':
    main()
