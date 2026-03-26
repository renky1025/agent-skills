#!/usr/bin/env python3
"""
Insanely Fast Whisper Transcriber
使用 faster-whisper 进行高性能语音转文字
基于 https://github.com/Vaibhavs10/insanely-fast-whisper
"""

import torch
from faster_whisper import WhisperModel
from pathlib import Path
from typing import Dict, Optional, List
import time


class InsanelyFastTranscriber:
    """
    高性能 Whisper 转录器
    使用 faster-whisper 实现，比原始 openai-whisper 快 2-4 倍
    """
    
    # 支持的模型列表
    MODELS = {
        "tiny": "tiny",
        "base": "base", 
        "small": "small",
        "medium": "medium",
        "large-v1": "large-v1",
        "large-v2": "large-v2",
        "large-v3": "large-v3",
        "large": "large-v3"  # 默认使用 v3
    }
    
    def __init__(
        self,
        model_size: str = "base",
        device: Optional[str] = None,
        compute_type: str = "int8",
        cpu_threads: int = 4,
        num_workers: int = 1
    ):
        """
        初始化转录器
        
        Args:
            model_size: 模型大小 (tiny/base/small/medium/large-v1/large-v2/large-v3)
            device: 计算设备 (cuda/cpu)，None 则自动选择
            compute_type: 计算精度 (int8/int8_float16/float16/float32)
            cpu_threads: CPU 线程数
            num_workers: 工作线程数
        """
        self.model_size = self.MODELS.get(model_size, "base")
        self.device = device or ("cuda" if torch.cuda.is_available() else "cpu")
        self.compute_type = compute_type
        self.cpu_threads = cpu_threads
        self.num_workers = num_workers
        
        self.model = None
        self._load_model()
    
    def _load_model(self):
        """加载 Whisper 模型"""
        print(f"🤖 加载 Whisper 模型: {self.model_size}")
        print(f"   设备: {self.device}, 精度: {self.compute_type}")
        
        start_time = time.time()
        
        self.model = WhisperModel(
            self.model_size,
            device=self.device,
            compute_type=self.compute_type,
            cpu_threads=self.cpu_threads,
            num_workers=self.num_workers
        )
        
        load_time = time.time() - start_time
        print(f"   ✅ 模型加载完成 ({load_time:.2f}s)")
    
    def transcribe(
        self,
        audio_path: Path,
        language: Optional[str] = None,
        task: str = "transcribe",
        beam_size: int = 5,
        best_of: int = 5,
        patience: float = 1.0,
        length_penalty: float = 1.0,
        temperature: float = 0.0,
        compression_ratio_threshold: float = 2.4,
        log_prob_threshold: float = -1.0,
        no_speech_threshold: float = 0.6,
        condition_on_previous_text: bool = True,
        initial_prompt: Optional[str] = None,
        word_timestamps: bool = True,
        vad_filter: bool = True,
        vad_parameters: Optional[dict] = None,
        verbose: bool = False
    ) -> Dict:
        """
        转录音频文件
        
        Args:
            audio_path: 音频文件路径
            language: 语言代码 (zh/en/ja等)，None 则自动检测
            task: 任务类型 (transcribe/translate)
            beam_size: beam search 大小
            best_of: 候选数量
            patience: 耐心值
            length_penalty: 长度惩罚
            temperature: 采样温度
            compression_ratio_threshold: 压缩比阈值
            log_prob_threshold: 对数概率阈值
            no_speech_threshold: 无语音阈值
            condition_on_previous_text: 是否基于前文
            initial_prompt: 初始提示
            word_timestamps: 是否生成词级时间戳
            vad_filter: 是否使用 VAD 过滤
            vad_parameters: VAD 参数
            verbose: 是否显示详细信息
            
        Returns:
            转录结果字典
        """
        if self.model is None:
            raise RuntimeError("模型未加载")
        
        audio_path = Path(audio_path)
        if not audio_path.exists():
            raise FileNotFoundError(f"音频文件不存在: {audio_path}")
        
        print(f"🎯 开始转录: {audio_path.name}")
        start_time = time.time()
        
        # 设置 VAD 参数
        if vad_parameters is None:
            vad_parameters = {
                "threshold": 0.5,
                "min_speech_duration_ms": 250,
                "max_speech_duration_s": float("inf"),
                "min_silence_duration_ms": 500,
                "speech_pad_ms": 400
            }
        
        # 执行转录
        segments, info = self.model.transcribe(
            str(audio_path),
            language=language,
            task=task,
            beam_size=beam_size,
            best_of=best_of,
            patience=patience,
            length_penalty=length_penalty,
            temperature=temperature,
            compression_ratio_threshold=compression_ratio_threshold,
            log_prob_threshold=log_prob_threshold,
            no_speech_threshold=no_speech_threshold,
            condition_on_previous_text=condition_on_previous_text,
            initial_prompt=initial_prompt,
            word_timestamps=word_timestamps,
            vad_filter=vad_filter,
            vad_parameters=vad_parameters
        )
        
        # 处理结果
        result_segments = []
        full_text = []
        
        for segment in segments:
            seg_data = {
                "id": segment.id,
                "start": segment.start,
                "end": segment.end,
                "text": segment.text.strip(),
                "confidence": segment.avg_logprob,
                "no_speech_prob": segment.no_speech_prob
            }
            
            # 添加词级时间戳
            if word_timestamps and segment.words:
                seg_data["words"] = [
                    {
                        "start": word.start,
                        "end": word.end,
                        "word": word.word,
                        "probability": word.probability
                    }
                    for word in segment.words
                ]
            
            result_segments.append(seg_data)
            full_text.append(segment.text.strip())
        
        elapsed_time = time.time() - start_time
        audio_duration = result_segments[-1]["end"] if result_segments else 0
        
        print(f"   ✅ 转录完成")
        print(f"   📊 音频长度: {self._format_time(audio_duration)}")
        print(f"   ⏱️  处理时间: {elapsed_time:.2f}s")
        print(f"   🚀 实时率: {audio_duration/elapsed_time:.2f}x")
        
        return {
            "text": " ".join(full_text),
            "segments": result_segments,
            "language": info.language,
            "language_probability": info.language_probability,
            "duration": audio_duration,
            "processing_time": elapsed_time,
            "realtime_factor": audio_duration / elapsed_time if elapsed_time > 0 else 0
        }
    
    def transcribe_batch(
        self,
        audio_paths: List[Path],
        language: Optional[str] = None,
        **kwargs
    ) -> List[Dict]:
        """
        批量转录多个音频文件
        
        Args:
            audio_paths: 音频文件路径列表
            language: 语言代码
            **kwargs: 其他转录参数
            
        Returns:
            转录结果列表
        """
        results = []
        total = len(audio_paths)
        
        print(f"📦 批量转录 {total} 个文件")
        
        for i, audio_path in enumerate(audio_paths, 1):
            print(f"\n[{i}/{total}] 处理: {audio_path.name}")
            try:
                result = self.transcribe(audio_path, language=language, **kwargs)
                results.append(result)
            except Exception as e:
                print(f"   ❌ 错误: {e}")
                results.append({"error": str(e), "audio_path": str(audio_path)})
        
        return results
    
    def _format_time(self, seconds: float) -> str:
        """格式化时间"""
        mins, secs = divmod(int(seconds), 60)
        hours, mins = divmod(mins, 60)
        if hours > 0:
            return f"{hours}:{mins:02d}:{secs:02d}"
        return f"{mins}:{secs:02d}"
    
    def get_model_info(self) -> Dict:
        """获取模型信息"""
        return {
            "model_size": self.model_size,
            "device": self.device,
            "compute_type": self.compute_type,
            "cuda_available": torch.cuda.is_available(),
            "cuda_device_count": torch.cuda.device_count() if torch.cuda.is_available() else 0
        }


# 兼容性包装类，保持与原有 Whisper 接口一致
class WhisperTranscriber(InsanelyFastTranscriber):
    """
    兼容性包装类
    保持与原有代码的接口兼容
    """
    
    def __init__(self, model_size: str = "base", **kwargs):
        # 映射模型名称
        model_mapping = {
            "tiny": "tiny",
            "base": "base",
            "small": "small",
            "medium": "medium",
            "large": "large-v3"
        }
        mapped_size = model_mapping.get(model_size, "base")
        super().__init__(model_size=mapped_size, **kwargs)


if __name__ == "__main__":
    # 测试代码
    import sys
    
    if len(sys.argv) < 2:
        print("用法: python transcriber.py <音频文件>")
        sys.exit(1)
    
    audio_file = Path(sys.argv[1])
    
    # 创建转录器
    transcriber = InsanelyFastTranscriber(model_size="base")
    
    # 打印模型信息
    info = transcriber.get_model_info()
    print(f"\n模型信息: {info}\n")
    
    # 执行转录
    result = transcriber.transcribe(audio_file, verbose=True)
    
    # 输出结果
    print("\n" + "="*50)
    print("转录结果:")
    print("="*50)
    print(result["text"])
    
    print("\n分段详情:")
    for seg in result["segments"][:5]:  # 只显示前5段
        print(f"[{seg['start']:.2f}s -> {seg['end']:.2f}s] {seg['text']}")
