import React from 'react';
import { Card, Spin, Tag, Progress, Steps } from 'antd';
import { 
  UserOutlined, 
  SearchOutlined, 
  TrophyOutlined, 
  ThunderboltOutlined, 
  ShareAltOutlined,
  CheckCircleOutlined,
  ClockCircleOutlined,
  LoadingOutlined
} from '@ant-design/icons';

const { Step } = Steps;

const agentConfig = {
  company: {
    title: '公司识别 Agent',
    icon: <UserOutlined style={{ fontSize: '24px' }} />,
    color: '#1890ff',
    description: '从 PDF 中提取公司画像',
  },
  search: {
    title: '客户搜索 Agent',
    icon: <SearchOutlined style={{ fontSize: '24px' }} />,
    color: '#52c41a',
    description: '根据画像搜索候选客户',
  },
  grading: {
    title: '分级 Agent',
    icon: <TrophyOutlined style={{ fontSize: '24px' }} />,
    color: '#faad14',
    description: '对客户进行 A/B/C/D 分级',
  },
  action: {
    title: '动作建议 Agent',
    icon: <ThunderboltOutlined style={{ fontSize: '24px' }} />,
    color: '#eb2f96',
    description: '生成下一步动作建议',
  },
  feishu: {
    title: '飞书联动 Agent',
    icon: <ShareAltOutlined style={{ fontSize: '24px' }} />,
    color: '#722ed1',
    description: '同步结果到飞书多维表',
  },
};

const AgentCard = ({ type, status, progress, data, onStart }) => {
  const config = agentConfig[type];
  if (!config) return null;

  const getStatusIcon = () => {
    switch (status) {
      case 'idle':
        return <ClockCircleOutlined />;
      case 'running':
        return <Spin indicator={<LoadingOutlined style={{ fontSize: 24 }} spin />} />;
      case 'completed':
        return <CheckCircleOutlined />;
      case 'error':
        return <span style={{ color: '#ff4d4f' }}>✕</span>;
      default:
        return <ClockCircleOutlined />;
    }
  };

  const getStatusTag = () => {
    const colors = {
      idle: 'default',
      running: 'processing',
      completed: 'success',
      error: 'error',
    };
    const texts = {
      idle: '等待中',
      running: '运行中',
      completed: '已完成',
      error: '失败',
    };
    return <Tag color={colors[status]}>{texts[status]}</Tag>;
  };

  return (
    <Card
      className="agent-card"
      hoverable
      style={{ 
        borderLeft: `4px solid ${config.color}`,
        opacity: status === 'idle' ? 0.8 : 1,
      }}
      onClick={() => status === 'idle' && onStart && onStart(type)}
    >
      <div style={{ display: 'flex', alignItems: 'flex-start', gap: 16 }}>
        <div style={{ color: config.color, marginTop: 4 }}>
          {config.icon}
        </div>
        <div style={{ flex: 1 }}>
          <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: 8 }}>
            <h3 style={{ margin: 0, fontSize: '16px' }}>{config.title}</h3>
            {getStatusTag()}
          </div>
          <p style={{ margin: '0 0 12px 0', color: '#666', fontSize: '13px' }}>
            {config.description}
          </p>
          
          {status === 'running' && (
            <Progress 
              percent={progress || 0} 
              size="small" 
              status="active"
              style={{ marginBottom: 8 }}
            />
          )}
          
          {status === 'completed' && data && (
            <div style={{ fontSize: '12px', color: '#52c41a', marginTop: 8 }}>
              ✓ 处理完成
            </div>
          )}
        </div>
      </div>
    </Card>
  );
};

export default AgentCard;
