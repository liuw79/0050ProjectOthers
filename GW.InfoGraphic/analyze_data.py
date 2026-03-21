import csv
from datetime import datetime
from collections import defaultdict

file_path = '/Users/comdir/SynologyDrive/0050Project/GW.InfoGraphic/班主任经历信息图/伍悦开课数据 - 汇总.csv'

def parse_date(date_str):
    try:
        return datetime.strptime(date_str, '%Y/%m/%d')
    except ValueError:
        return None

import json
import os

def analyze_data(file_path):
    data = []
    with open(file_path, 'r', encoding='utf-8-sig') as f:
        reader = csv.DictReader(f)
        for row in reader:
            data.append(row)

    if not data:
        print("No data found.")
        return

    # Basic Metrics
    dates = [parse_date(row['开课日期']) for row in data if parse_date(row['开课日期'])]
    dates.sort()
    
    start_date = dates[0]
    end_date = dates[-1]
    duration = end_date - start_date
    
    total_sessions = len(data)
    total_students = sum(int(row['上课人数']) for row in data if row['上课人数'].isdigit())
    total_companies = sum(int(row['上课企业数']) for row in data if row['上课企业数'].isdigit())
    
    unique_courses = set(row['课程'] for row in data)
    unique_teachers = set(row['导师'] for row in data)
    
    # Advanced Metrics / "Emotional" Milestones
    teacher_first_met = {}
    new_course_milestones = [] # 见证新课 (第1期)
    term_milestones = [] # 见证整数期 (10, 50, 100等)
    
    # Yearly summary
    yearly_stats = defaultdict(lambda: {"sessions": 0, "students": 0, "cities": set(), "courses": set()})

    # Process chronologically
    sorted_data = sorted(data, key=lambda x: parse_date(x['开课日期']) if parse_date(x['开课日期']) else datetime.min)
    
    teacher_first_met_list = []
    
    # Interesting milestones terms
    milestone_terms = {'10', '20', '30', '50', '80', '100', '200'}

    cumulative_sessions = 0

    timeline_events = []
    
    # Add manual special events (COVID-19)
    timeline_events.append({
        "year": 2020,
        "date": "2020/02/01",
        "type": "covid",
        "content": "共克 · 时艰",
        "desc": "疫情爆发，线下暂停。戴上口罩，心依然相连。"
    })
    
    timeline_events.append({
        "year": 2022,
        "date": "2022/04/01",
        "type": "covid",
        "content": "守望 · 上海",
        "desc": "一段艰难的静默时光。暂时的分别，是为了更好的重逢。"
    })

    for row in sorted_data:
        date_obj = parse_date(row['开课日期'])
        if not date_obj:
            continue
            
        date = row['开课日期']
        teacher = row['导师']
        course = row['课程']
        term = row['期号']
        city = row['城市']
        
        cumulative_sessions += 1
        year = date_obj.year
        
        # Yearly Stats
        yearly_stats[year]["sessions"] += 1
        if row['上课人数'].isdigit():
            yearly_stats[year]["students"] += int(row['上课人数'])
        yearly_stats[year]["cities"].add(city)
        yearly_stats[year]["courses"].add(course)

        # Teacher First Met
        if teacher not in teacher_first_met:
            teacher_first_met[teacher] = date
            teacher_first_met_list.append({
                "type": "teacher",
                "year": year,
                "date": date,
                "teacher": teacher,
                "text": f"第一次与 {teacher} 老师并肩作战"
            })
            # Add to timeline if it's a significant teacher (optional logic, here we add all to list but filter later)
            timeline_events.append({
                "year": year,
                "date": date,
                "type": "teacher",
                "content": f"与 {teacher} 老师开启合作"
            })
            
        # Course Milestones (Term 1)
        if term == '1':
            new_course_milestones.append({
                "year": year,
                "course": course,
                "date": date
            })
            timeline_events.append({
                "year": year,
                "date": date,
                "type": "new_course",
                "content": f"见证《{course}》诞生"
            })

        # Course Integer Milestones
        if term in milestone_terms:
            term_milestones.append({
                "year": year,
                "date": date,
                "course": course,
                "term": term,
                "text": f"见证《{course}》第{term}期"
            })
            timeline_events.append({
                "year": year,
                "date": date,
                "type": "milestone",
                "content": f"《{course}》第{term}期达成"
            })
            
        # Personal Milestones (Cumulative Sessions)
        if cumulative_sessions in [1, 100, 200, 300, 400]:
            timeline_events.append({
                "year": year,
                "date": date,
                "type": "personal",
                "content": f"第 {cumulative_sessions} 次带班达成"
            })

    # Group new courses by year for the artistic view
    new_courses_by_year = defaultdict(list)
    for item in new_course_milestones:
        new_courses_by_year[item['year']].append(item['course'])
        
    # Format timeline: Group by year, pick highlights
    final_timeline = []
    
    # 1. Start
    final_timeline.append({
        "year": sorted_data[0]['开课日期'].split('/')[0],
        "date": sorted_data[0]['开课日期'],
        "title": "初次相遇",
        "desc": f"在上海，开启了第一场《{sorted_data[0]['课程']}》"
    })

    # 2. Iterate years
    for year in sorted(yearly_stats.keys()):
        stats = yearly_stats[year]
        # Annual Summary
        final_timeline.append({
            "year": year,
            "type": "summary",
            "title": f"{year}年 · 耕耘",
            "desc": f"全年带班 {stats['sessions']} 场，服务 {stats['students']} 位学员，足迹遍布 {len(stats['cities'])} 个城市"
        })
        
        # Pick 1-2 highlight events for this year (Priority: COVID > Personal Milestone > Term Milestone > New Course > Teacher)
        year_events = [e for e in timeline_events if e['year'] == year]
        
        # Filter priorities
        highlights = []
        
        # Add COVID events first
        highlights.extend([e for e in year_events if e['type'] == 'covid'])
        
        # Add big term milestones (100, 50)
        highlights.extend([e for e in year_events if e['type'] == 'milestone' and e['content'].split('第')[1].startswith(('50', '100'))])
        # Add personal milestones (100th session etc)
        highlights.extend([e for e in year_events if e['type'] == 'personal'])
        
        # If not enough, add new courses (limit to 2)
        if len(highlights) < 3: # Increased limit slightly to accommodate COVID
            new_course_events = [e for e in year_events if e['type'] == 'new_course']
            highlights.extend(new_course_events[:2])
            
        # If still not enough, add first teacher collab (limit to 1)
        if len(highlights) < 3:
             teacher_events = [e for e in year_events if e['type'] == 'teacher']
             highlights.extend(teacher_events[:1])

        # Deduplicate and add to final timeline
        seen_content = set()
        # Sort highlights by date to ensure correct order
        highlights.sort(key=lambda x: x['date'])
        
        for h in highlights:
            if h['content'] not in seen_content:
                final_timeline.append({
                    "year": h['year'],
                    "date": h['date'],
                    "title": h['content'], # Simplified
                    "desc": h.get('desc', ''), # Get desc if exists
                    "type": h['type']
                })
                seen_content.add(h['content'])

    # 3. End
    final_timeline.append({
        "year": sorted_data[-1]['开课日期'].split('/')[0],
        "date": sorted_data[-1]['开课日期'],
        "title": "最近一次",
        "desc": f"在上海，圆满完成《{sorted_data[-1]['课程']}》"
    })

    output_data = {
        "summary": {
            "start_date": start_date.strftime('%Y/%m/%d'),
            "end_date": end_date.strftime('%Y/%m/%d'),
            "duration_days": duration.days,
            "total_sessions": total_sessions,
            "total_students": total_students,
            "total_companies": total_companies,
            "teacher_count": len(unique_teachers),
            "course_count": len(unique_courses),
            "new_course_count": len(new_course_milestones)
        },
        "new_courses_by_year": [{"year": k, "courses": v} for k, v in new_courses_by_year.items()],
        "term_milestones": term_milestones,
        "timeline": final_timeline,
        "teacher_first_met": teacher_first_met_list
    }

    # Ensure web directory exists
    output_path = '班主任经历信息图/wyweb/data.json'
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(output_data, f, ensure_ascii=False, indent=2)
    
    print(f"Data exported to {output_path}")

    print(f"--- 基础数据统计 ---")
    print(f"服务开始日期: {start_date.strftime('%Y年%m月%d日')}")
    print(f"服务结束日期: {end_date.strftime('%Y年%m月%d日')}")
    print(f"总服务天数: {duration.days} 天")
    print(f"总开课期数: {total_sessions} 期")
    print(f"总服务学员数: {total_students} 人")
    print(f"总服务企业数: {total_companies} 家")
    print(f"合作导师数: {len(unique_teachers)} 位")
    print(f"涉及课程门数: {len(unique_courses)} 门")
    
    print(f"\n--- 情感化/里程碑数据 ---")
    print(f"第一次开课: {sorted_data[0]['开课日期']} - {sorted_data[0]['课程']}")
    print(f"最后一次开课: {sorted_data[-1]['开课日期']} - {sorted_data[-1]['课程']}")
    
    print(f"\n--- 导师初次见面 (部分) ---")
    for teacher, date in list(teacher_first_met.items())[:10]: # Show first 10
        print(f"第一次与 {teacher} 老师合作: {date}")
        
    print(f"\n--- 课程里程碑 (第1期) ---")
    for milestone in new_course_milestones:
        print(milestone)

if __name__ == "__main__":
    analyze_data(file_path)
