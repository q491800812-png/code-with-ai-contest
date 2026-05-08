"""
单元测试：5G 信号可视化看板

本文件包含对 5G 信号看板核心功能的单元测试，包括：
- 数据加载和验证
- 信号强度着色逻辑
- 数据筛选功能
"""

import pytest
import pandas as pd
import numpy as np
from pathlib import Path


class TestDataLoading:
    """测试数据加载功能"""
    
    @pytest.fixture
    def sample_data(self):
        """加载示例数据"""
        df = pd.read_csv('data/signal_samples.csv')
        return df
    
    def test_data_file_exists(self):
        """验证数据文件存在"""
        assert Path('data/signal_samples.csv').exists(), "数据文件不存在"
    
    def test_data_loaded_successfully(self, sample_data):
        """验证数据成功加载"""
        assert isinstance(sample_data, pd.DataFrame), "数据不是 DataFrame"
        assert len(sample_data) > 0, "数据为空"
    
    def test_data_columns(self, sample_data):
        """验证必需的数据列"""
        required_columns = [
            'Latitude', 'Longitude', 'CellID', 'Band',
            'RSRP_dBm', 'SINR_dB', 'TerminalType', 'Download_Mbps'
        ]
        for col in required_columns:
            assert col in sample_data.columns, f"缺少列: {col}"
    
    def test_data_types(self, sample_data):
        """验证数据类型正确"""
        assert sample_data['Latitude'].dtype in [np.float64, np.float32], "Latitude 应为浮点数"
        assert sample_data['Longitude'].dtype in [np.float64, np.float32], "Longitude 应为浮点数"
        assert sample_data['CellID'].dtype in [np.int64, np.int32], "CellID 应为整数"
        assert sample_data['RSRP_dBm'].dtype in [np.float64, np.float32], "RSRP_dBm 应为浮点数"


class TestSignalColorLogic:
    """测试信号强度着色逻辑"""
    
    @staticmethod
    def get_color(rsrp):
        """获取信号强度对应的颜色 (从 app.py 复制的逻辑)"""
        if rsrp > -90:
            return [0, 255, 0]      # 绿色
        elif rsrp > -100:
            return [255, 255, 0]    # 黄色
        elif rsrp > -110:
            return [255, 165, 0]    # 橙色
        else:
            return [255, 0, 0]      # 红色
    
    def test_strong_signal_color(self):
        """测试信号强时返回绿色"""
        assert self.get_color(-85) == [0, 255, 0], "强信号应为绿色"
        assert self.get_color(-89.9) == [0, 255, 0], "≥-90dBm 应为绿色"
    
    def test_medium_signal_color(self):
        """测试信号中等时返回黄色"""
        assert self.get_color(-95) == [255, 255, 0], "中等信号应为黄色"
        assert self.get_color(-99) == [255, 255, 0], "-99dBm 应为黄色"
    
    def test_weak_signal_color(self):
        """测试信号较弱时返回橙色"""
        assert self.get_color(-105) == [255, 165, 0], "较弱信号应为橙色"
    
    def test_very_weak_signal_color(self):
        """测试信号很弱时返回红色"""
        assert self.get_color(-115) == [255, 0, 0], "很弱信号应为红色"
        assert self.get_color(-120) == [255, 0, 0], "≤-110dBm 应为红色"


class TestDataFiltering:
    """测试数据筛选功能"""
    
    @pytest.fixture
    def sample_data(self):
        """加载示例数据"""
        df = pd.read_csv('data/signal_samples.csv')
        return df
    
    def test_band_filtering(self, sample_data):
        """测试频段筛选"""
        bands = ['n28']
        filtered = sample_data[sample_data['Band'].isin(bands)]
        assert len(filtered) > 0, "筛选结果为空"
        assert filtered['Band'].unique().tolist() == bands, "筛选失败"
    
    def test_rsrp_range_filtering(self, sample_data):
        """测试 RSRP 范围筛选"""
        rsrp_min, rsrp_max = -100, -80
        filtered = sample_data[
            (sample_data['RSRP_dBm'] >= rsrp_min) &
            (sample_data['RSRP_dBm'] <= rsrp_max)
        ]
        assert len(filtered) > 0, "RSRP 筛选结果为空"
        assert filtered['RSRP_dBm'].min() >= rsrp_min, "最小 RSRP 不符合"
        assert filtered['RSRP_dBm'].max() <= rsrp_max, "最大 RSRP 不符合"
    
    def test_terminal_type_filtering(self, sample_data):
        """测试终端类型筛选"""
        terminals = ['Smartphone']
        filtered = sample_data[sample_data['TerminalType'].isin(terminals)]
        assert len(filtered) > 0, "终端类型筛选结果为空"
        assert filtered['TerminalType'].unique().tolist() == terminals, "筛选失败"
    
    def test_combined_filtering(self, sample_data):
        """测试联合筛选"""
        bands = ['n28', 'n78']
        rsrp_range = (-100, -85)
        terminals = ['Smartphone', 'CPE']
        
        filtered = sample_data[
            (sample_data['Band'].isin(bands)) &
            (sample_data['RSRP_dBm'] >= rsrp_range[0]) &
            (sample_data['RSRP_dBm'] <= rsrp_range[1]) &
            (sample_data['TerminalType'].isin(terminals))
        ]
        
        # 验证筛选结果符合所有条件
        if len(filtered) > 0:
            assert filtered['Band'].isin(bands).all(), "频段筛选失败"
            assert (filtered['RSRP_dBm'] >= rsrp_range[0]).all(), "RSRP 最小值检查失败"
            assert (filtered['RSRP_dBm'] <= rsrp_range[1]).all(), "RSRP 最大值检查失败"
            assert filtered['TerminalType'].isin(terminals).all(), "终端类型筛选失败"


class TestDataStatistics:
    """测试数据统计功能"""
    
    @pytest.fixture
    def sample_data(self):
        """加载示例数据"""
        df = pd.read_csv('data/signal_samples.csv')
        return df
    
    def test_average_rsrp_calculation(self, sample_data):
        """测试平均 RSRP 计算"""
        avg_rsrp = sample_data['RSRP_dBm'].mean()
        assert isinstance(avg_rsrp, float), "平均值应为浮点数"
        assert -120 <= avg_rsrp <= -70, "平均 RSRP 超出预期范围"
    
    def test_average_sinr_calculation(self, sample_data):
        """测试平均 SINR 计算"""
        avg_sinr = sample_data['SINR_dB'].mean()
        assert isinstance(avg_sinr, float), "平均值应为浮点数"
        assert 0 <= avg_sinr <= 50, "平均 SINR 超出预期范围"
    
    def test_average_download_speed(self, sample_data):
        """测试平均下载速率计算"""
        avg_speed = sample_data['Download_Mbps'].mean()
        assert isinstance(avg_speed, float), "平均值应为浮点数"
        assert avg_speed > 0, "下载速率应大于 0"
    
    def test_unique_bands(self, sample_data):
        """测试频段统计"""
        unique_bands = sample_data['Band'].unique()
        assert len(unique_bands) > 0, "应有至少一个频段"
    
    def test_unique_terminal_types(self, sample_data):
        """测试终端类型统计"""
        unique_terminals = sample_data['TerminalType'].unique()
        assert len(unique_terminals) > 0, "应有至少一个终端类型"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
