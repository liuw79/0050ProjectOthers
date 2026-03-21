import requests
import json
import logging
from datetime import datetime
from django.conf import settings
from .models import InterviewTranscript, InsightAnalysis, AnalysisTemplate, AnalysisLog

logger = logging.getLogger('ascend_plan')


class FastGPTService:
    """FastGPT API 服务类"""
    
    def __init__(self):
        self.api_url = settings.FASTGPT_API_URL
        self.api_key = settings.FASTGPT_API_KEY
        self.headers = {
            'Authorization': f'Bearer {self.api_key}',
            'Content-Type': 'application/json'
        }
    
    def call_llm(self, messages, model='deepseek-chat', temperature=0.7, max_tokens=2000):
        """调用LLM API"""
        payload = {
            'model': model,
            'messages': messages,
            'temperature': temperature,
            'max_tokens': max_tokens
        }
        
        try:
            response = requests.post(
                f"{self.api_url}/chat/completions",
                headers=self.headers,
                json=payload,
                timeout=60
            )
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            logger.error(f"FastGPT API调用失败: {e}")
            raise


class InsightAnalysisService:
    """洞察分析服务类"""
    
    def __init__(self):
        self.fastgpt = FastGPTService()
    
    def analyze_transcript(self, transcript_id, template_id=None):
        """分析访谈文稿"""
        try:
            transcript = InterviewTranscript.objects.get(id=transcript_id)
            transcript.status = 'processing'
            transcript.save()
            
            # 获取分析模板
            if template_id:
                template = AnalysisTemplate.objects.get(id=template_id, is_active=True)
            else:
                template = AnalysisTemplate.objects.filter(is_active=True).first()
            
            if not template:
                raise ValueError("没有可用的分析模板")
            
            # 开始分析
            start_time = datetime.now()
            log = AnalysisLog.objects.create(
                transcript=transcript,
                template=template,
                start_time=start_time,
                status='success'  # 先设为成功，如果失败会更新
            )
            
            try:
                # 构建分析请求
                analysis_result = self._perform_analysis(transcript, template, log)
                
                # 保存分析结果
                insight, created = InsightAnalysis.objects.get_or_create(
                    transcript=transcript,
                    defaults=analysis_result
                )
                
                if not created:
                    # 更新现有分析
                    for key, value in analysis_result.items():
                        setattr(insight, key, value)
                    insight.save()
                
                transcript.status = 'completed'
                transcript.save()
                
                # 更新日志
                end_time = datetime.now()
                log.end_time = end_time
                log.duration_seconds = (end_time - start_time).total_seconds()
                log.save()
                
                return insight
                
            except Exception as e:
                # 记录错误
                log.status = 'error'
                log.error_message = str(e)
                log.end_time = datetime.now()
                log.save()
                
                transcript.status = 'failed'
                transcript.save()
                
                raise
                
        except Exception as e:
            logger.error(f"分析访谈文稿失败 (ID: {transcript_id}): {e}")
            raise
    
    def _perform_analysis(self, transcript, template, log):
        """执行具体的分析逻辑"""
        # 构建提示词
        user_prompt = template.user_prompt_template.format(
            transcript=transcript.raw_transcript,
            customer_name=transcript.customer.name,
            interview_date=transcript.interview_date or '未知',
            interview_type=transcript.interview_type or '常规访谈'
        )
        
        messages = [
            {"role": "system", "content": template.system_prompt},
            {"role": "user", "content": user_prompt}
        ]
        
        # 记录请求数据
        log.request_data = {
            'messages': messages,
            'template_id': template.id,
            'model_config': template.model_config
        }
        log.save()
        
        # 调用LLM
        model_config = template.model_config or {}
        response = self.fastgpt.call_llm(
            messages=messages,
            model=model_config.get('model', 'deepseek-chat'),
            temperature=model_config.get('temperature', 0.7),
            max_tokens=model_config.get('max_tokens', 2000)
        )
        
        # 记录响应数据
        log.response_data = response
        log.save()
        
        # 解析响应
        content = response['choices'][0]['message']['content']
        
        try:
            # 尝试解析JSON格式的响应
            analysis_data = json.loads(content)
        except json.JSONDecodeError:
            # 如果不是JSON格式，作为纯文本处理
            analysis_data = {'summary': content}
        
        # 构建分析结果
        result = {
            'key_information': analysis_data.get('key_information', {}),
            'learning_goals': analysis_data.get('learning_goals', {}),
            'current_situation': analysis_data.get('current_situation', {}),
            'challenges_obstacles': analysis_data.get('challenges_obstacles', {}),
            'strengths_resources': analysis_data.get('strengths_resources', {}),
            'summary': analysis_data.get('summary', ''),
            'recommendations': analysis_data.get('recommendations', ''),
            'next_steps': analysis_data.get('next_steps', ''),
            'analysis_model': model_config.get('model', 'deepseek-chat'),
            'analysis_version': template.version,
            'confidence_score': analysis_data.get('confidence_score')
        }
        
        # 记录Token使用量和成本
        if 'usage' in response:
            log.token_usage = response['usage']
            # 简单的成本估算（需要根据实际API定价调整）
            total_tokens = response['usage'].get('total_tokens', 0)
            log.estimated_cost = total_tokens * 0.0001  # 假设每1000 tokens 0.1元
            log.save()
        
        return result
    
    def get_default_template(self):
        """获取默认分析模板"""
        template, created = AnalysisTemplate.objects.get_or_create(
            name='默认访谈分析模板',
            defaults={
                'description': '用于分析客户访谈文稿的默认模板',
                'system_prompt': self._get_default_system_prompt(),
                'user_prompt_template': self._get_default_user_prompt(),
                'target_fields': [
                    'key_information', 'learning_goals', 'current_situation',
                    'challenges_obstacles', 'strengths_resources', 'summary',
                    'recommendations', 'next_steps'
                ],
                'model_config': {
                    'model': 'deepseek-chat',
                    'temperature': 0.7,
                    'max_tokens': 2000
                },
                'created_by_id': 1  # 假设管理员用户ID为1
            }
        )
        return template
    
    def _get_default_system_prompt(self):
        """获取默认系统提示词"""
        return """
你是一位专业的学习规划师助手，擅长分析客户访谈内容并提取关键洞察。

你的任务是分析访谈文稿，提取以下关键信息：
1. 关键信息提取：客户的基本情况、背景信息
2. 学习目标分析：客户的学习目标、期望成果
3. 现状分析：客户当前的学习状态、已有基础
4. 挑战与障碍：客户面临的困难、阻碍因素
5. 优势与资源：客户的优势、可利用资源
6. 总结概述：整体情况的简要总结
7. 初步建议：基于分析的初步建议
8. 后续行动：建议的下一步行动

请以JSON格式返回分析结果，确保结构清晰、内容准确。
"""
    
    def _get_default_user_prompt(self):
        """获取默认用户提示词模板"""
        return """
请分析以下访谈文稿：

客户姓名：{customer_name}
访谈日期：{interview_date}
访谈类型：{interview_type}

访谈内容：
{transcript}

请按照系统提示的要求，以JSON格式返回分析结果。
"""


class AnalysisReportService:
    """分析报告服务类"""
    
    def generate_customer_report(self, customer_id):
        """生成客户的综合分析报告"""
        from appointments.models import Customer
        
        customer = Customer.objects.get(id=customer_id)
        transcripts = InterviewTranscript.objects.filter(customer=customer)
        insights = InsightAnalysis.objects.filter(transcript__customer=customer)
        
        report = {
            'customer_info': {
                'name': customer.name,
                'phone': customer.phone,
                'email': customer.email,
                'age': customer.age,
                'education_background': customer.education_background
            },
            'interview_summary': {
                'total_interviews': transcripts.count(),
                'completed_analysis': insights.count(),
                'latest_interview': transcripts.first().created_at if transcripts.exists() else None
            },
            'key_insights': [],
            'recommendations': [],
            'next_steps': []
        }
        
        # 汇总所有洞察
        for insight in insights:
            if insight.summary:
                report['key_insights'].append(insight.summary)
            if insight.recommendations:
                report['recommendations'].append(insight.recommendations)
            if insight.next_steps:
                report['next_steps'].append(insight.next_steps)
        
        return report