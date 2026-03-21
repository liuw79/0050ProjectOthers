#!/usr/bin/env python3
"""
语音助手 - 开车时免手操作 Claude
使用方法：
1. 安装依赖：pip install anthropic openwakeword sounddevice scipy numpy faster-whisper
2. 设置环境变量：export ANTHROPIC_API_KEY="your-key"
3. 运行：python voice_claude.py

注意：首次运行会下载 Whisper 模型（约 150MB）
"""

import os
import sys
import time

try:
    import sounddevice as sd
    import numpy as np
except ImportError:
    print("请安装音频依赖：pip install sounddevice numpy")
    sys.exit(1)

try:
    from anthropic import Anthropic
except ImportError:
    print("请安装API依赖：pip install anthropic")
    sys.exit(1)

try:
    from faster_whisper import WhisperModel
except ImportError:
    print("请安装语音识别依赖：pip install faster-whisper")
    sys.exit(1)

try:
    import openwakeword
    from openwakeword.model import Model
except ImportError:
    print("请安装唤醒词依赖：pip install openwakeword")
    sys.exit(1)


class VoiceAssistant:
    def __init__(self):
        # 配置
        self.anthropic_key = os.environ.get("ANTHROPIC_API_KEY")
        self.anthropic_base_url = os.environ.get("ANTHROPIC_BASE_URL")

        if not self.anthropic_key:
            print("错误：请设置 ANTHROPIC_API_KEY 环境变量")
            sys.exit(1)

        # 初始化 Claude 客户端
        claude_params = {"api_key": self.anthropic_key}
        if self.anthropic_base_url:
            claude_params["base_url"] = self.anthropic_base_url
            print(f"使用自定义 Anthropic API: {self.anthropic_base_url}")
        self.claude_client = Anthropic(**claude_params)

        # 音频配置
        self.sample_rate = 16000
        self.channels = 1

        # 对话历史
        self.conversation_history = []

        # 加载本地 Whisper 模型
        print("加载语音识别模型...")
        self.whisper_model = WhisperModel(
            "small",  # 可选: tiny, base, small, medium, large
            device="cpu",  # Mac 用 CPU，有 GPU 可改为 "cuda"
            compute_type="int8"  # 量化，减少内存
        )
        print("语音识别模型加载完成")

        # 唤醒词模型
        print("加载唤醒词模型...")
        self.oww_model = Model(
            wakeword_models=["hey_mycroft", "alexa", "jarvis"],
            enable_speex_noise_suppression=True
        )
        print("唤醒词模型加载完成")

    def record_audio(self, duration=5):
        """录音指定时长"""
        print(f"🎤 录音中... ({duration}秒)")
        recording = sd.rec(
            int(duration * self.sample_rate),
            samplerate=self.sample_rate,
            channels=self.channels,
            dtype='float32'
        )
        sd.wait()
        return recording.flatten()

    def listen_for_wakeword(self):
        """持续监听唤醒词"""
        print("\n🎧 监听中... 说 'Hey Mycroft' 或 'Jarvis' 唤醒")

        buffer_size = 1280  # 80ms @ 16kHz

        with sd.InputStream(
            samplerate=self.sample_rate,
            channels=self.channels,
            dtype='float32',
            blocksize=buffer_size
        ) as stream:
            while True:
                data, _ = stream.read(buffer_size)
                audio_chunk = data.flatten()

                # 检测唤醒词
                prediction = self.oww_model.predict(audio_chunk)

                for wakeword, score in prediction.items():
                    if score > 0.5:
                        print(f"\n✅ 检测到唤醒词: {wakeword} (置信度: {score:.2f})")
                        return True

    def transcribe(self, audio_data):
        """使用本地 Whisper 转录语音"""
        print("📝 正在转录...")

        try:
            # faster-whisper 直接接受 numpy 数组
            segments, info = self.whisper_model.transcribe(
                audio_data,
                language="zh",
                beam_size=5
            )

            # 合并所有片段
            text = "".join([segment.text for segment in segments])
            return text.strip() if text else None

        except Exception as e:
            print(f"转录错误: {e}")
            return None

    def ask_claude(self, user_message):
        """发送消息给 Claude"""
        self.conversation_history.append({
            "role": "user",
            "content": user_message
        })

        try:
            message = self.claude_client.messages.create(
                model="claude-sonnet-4-20250514",
                max_tokens=1024,
                messages=self.conversation_history
            )

            response = message.content[0].text
            self.conversation_history.append({
                "role": "assistant",
                "content": response
            })

            return response
        except Exception as e:
            print(f"Claude API 错误: {e}")
            return "抱歉，连接 Claude 时出错。"

    def speak(self, text):
        """使用 macOS TTS 播放语音"""
        print(f"🔊 Claude: {text}")

        # 截断过长的文本
        if len(text) > 500:
            text = text[:500] + "..."

        # 转义特殊字符
        text = text.replace('"', '\\"').replace("'", "\\'")

        # 使用 macOS say 命令
        os.system(f'say -v "Ting-Ting" "{text}"')

    def run(self):
        """主循环"""
        print("=" * 50)
        print("🚗 Claude 语音助手 - 开车模式")
        print("=" * 50)
        print("使用方法：")
        print("1. 说 'Hey Mycroft' 或 'Jarvis' 唤醒")
        print("2. 听到提示音后说出你的问题")
        print("3. Claude 会语音回答")
        print("4. 说 '退出' 或 '停止' 结束")
        print("=" * 50)

        # 播放启动提示
        os.system('say "语音助手已启动，请说唤醒词"')

        while True:
            try:
                # 等待唤醒词
                if self.listen_for_wakeword():
                    # 播放提示音
                    os.system('say "请说"')

                    # 录音 5 秒
                    audio = self.record_audio(duration=5)

                    # 转录
                    user_text = self.transcribe(audio)

                    if user_text:
                        print(f"👤 你: {user_text}")

                        # 检查退出命令
                        if "退出" in user_text or "停止" in user_text:
                            self.speak("好的，再见！")
                            break

                        # 发送给 Claude
                        response = self.ask_claude(user_text)

                        # 语音播放回复
                        self.speak(response)
                    else:
                        self.speak("没听清，请再说一次")

            except KeyboardInterrupt:
                print("\n退出语音助手")
                break
            except Exception as e:
                print(f"错误: {e}")
                time.sleep(1)


def main():
    assistant = VoiceAssistant()
    assistant.run()


if __name__ == "__main__":
    main()
