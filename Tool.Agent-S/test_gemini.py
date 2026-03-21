#!/usr/bin/env python3

import os
from gui_agents.s3.core.engine import LMMEngineGemini

def test_gemini_api():
    """测试 Gemini API 连接"""
    try:
        # 尝试不同的模型名称 (基于 OpenAI 兼容格式)
        model_names = [
            'gemini-1.5-flash',
            'gemini-1.5-pro',
            'gemini-pro',
            'gemini-pro-vision'
        ]
        
        for model_name in model_names:
            try:
                print(f"🔄 测试模型: {model_name}")
                engine = LMMEngineGemini(
                    api_key=os.getenv('GEMINI_API_KEY'),
                    model=model_name
                )
                
                # 简单测试消息
                messages = [{'role': 'user', 'content': 'Hello, this is a test message. Please respond with "Gemini API is working!"'}]
                
                response = engine.generate(messages, temperature=0.0)
                print(f'✅ Gemini API 测试成功! 使用模型: {model_name}')
                print(f'响应: {response}')
                return True
                
            except Exception as e:
                print(f'❌ 模型 {model_name} 测试失败: {str(e)}')
                continue
        
        print("❌ 所有模型测试都失败了")
        return False
        
    except Exception as e:
        print(f'❌ Gemini API 测试失败: {str(e)}')
        return False

def test_direct_openai_client():
    """直接使用 OpenAI 客户端测试 Gemini API"""
    try:
        from openai import OpenAI
        
        api_key = os.getenv('GEMINI_API_KEY')
        base_url = os.getenv('GEMINI_ENDPOINT_URL')
        
        print(f"🔄 使用 API Key: {api_key[:10]}...")
        print(f"🔄 使用 Base URL: {base_url}")
        
        client = OpenAI(
            api_key=api_key,
            base_url=base_url
        )
        
        # 尝试不同的模型名称
        model_names = [
            'gemini-1.5-flash',
            'gemini-1.5-pro',
            'gemini-pro'
        ]
        
        for model_name in model_names:
            try:
                print(f"🔄 直接测试模型: {model_name}")
                
                response = client.chat.completions.create(
                    model=model_name,
                    messages=[{'role': 'user', 'content': 'Hello, please respond with "Direct Gemini API test successful!"'}],
                    temperature=0.0,
                    max_tokens=100
                )
                
                print(f'✅ 直接 Gemini API 测试成功! 使用模型: {model_name}')
                print(f'响应: {response.choices[0].message.content}')
                return True
                
            except Exception as e:
                print(f'❌ 直接测试模型 {model_name} 失败: {str(e)}')
                continue
        
        return False
        
    except Exception as e:
        print(f'❌ 直接 Gemini API 测试失败: {str(e)}')
        return False

if __name__ == "__main__":
    print("🧪 开始测试 Gemini API...")
    print("="*50)
    
    # 检查环境变量
    api_key = os.getenv('GEMINI_API_KEY')
    base_url = os.getenv('GEMINI_ENDPOINT_URL')
    
    if not api_key:
        print("❌ GEMINI_API_KEY 环境变量未设置")
        exit(1)
    
    if not base_url:
        print("❌ GEMINI_ENDPOINT_URL 环境变量未设置")
        exit(1)
    
    print(f"✅ API Key: {api_key[:10]}...")
    print(f"✅ Base URL: {base_url}")
    print()
    
    # 测试直接 OpenAI 客户端
    print("📋 测试 1: 直接使用 OpenAI 客户端")
    success1 = test_direct_openai_client()
    print()
    
    # 测试 Agent-S 的 Gemini 引擎
    print("📋 测试 2: 使用 Agent-S 的 LMMEngineGemini")
    success2 = test_gemini_api()
    
    if success1 or success2:
        print("\n🎉 Gemini API 配置成功!")
    else:
        print("\n❌ Gemini API 配置失败")