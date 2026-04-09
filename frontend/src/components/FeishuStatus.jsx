import React from 'react';
import { Card, Tag, Button, Progress, List, Statistic, Row, Col } from 'antd';
import { 
  ShareAltOutlined, 
  CheckCircleOutlined, 
  CloseCircleOutlined,
  SyncOutlined
} from '@ant-design/icons';

const FeishuStatus = ({ 
  status, 
  totalCount, 
  syncedCount, 
  failedCount,
  lastSyncTime,
  syncing,
  onTestConnection,
  onSyncAll,
  connectionStatus,
  errors 
}) => {
  const getStatusIcon = () => {
    switch (connectionStatus) {
      case 'connected':
        return <CheckCircleOutlined style={{ color: '#52c41a', fontSize: 20 }} />;
      case 'disconnected':
        return <CloseCircleOutlined style={{ color: '#ff4d4f', fontSize: 20 }} />;
      case 'testing':
        return <SyncOutlined spin style={{ fontSize: 20 }} />;
      default:
        return <ShareAltOutlined style={{ fontSize: 20 }} />;
    }
  };

  const getStatusText = () => {
    switch (connectionStatus) {
      case 'connected':
        return '已连接';
      case 'disconnected':
        return '未连接';
      case 'testing':
        return '测试中...';
      default:
        return '未知状态';
    }
  };

  const syncProgress = totalCount > 0 ? Math.round((syncedCount / totalCount) * 100) : 0;

  return (
    <Card 
      className="feishu-status-card"
      title={
        <div style={{ display: 'flex', alignItems: 'center', gap: 12 }}>
          {getStatusIcon()}
          <span>飞书多维表同步状态</span>
        </div>
      }
      extra={
        <div style={{ display: 'flex', gap: 8 }}>
          <Button 
            size="small" 
            onClick={onTestConnection}
            loading={connectionStatus === 'testing'}
          >
            测试连接
          </Button>
          <Button 
            type="primary" 
            size="small"
            icon={<ShareAltOutlined />}
            onClick={onSyncAll}
            loading={syncing}
            disabled={totalCount === 0 || connectionStatus !== 'connected'}
          >
            同步全部
          </Button>
        </div>
      }
    >
      <Row gutter={16} style={{ marginBottom: 24 }}>
        <Col span={6}>
          <Statistic 
            title="连接状态" 
            value={getStatusText()}
            valueStyle={{ 
              color: connectionStatus === 'connected' ? '#52c41a' : '#ff4d4f',
              fontSize: '16px'
            }}
          />
        </Col>
        <Col span={6}>
          <Statistic 
            title="总记录数" 
            value={totalCount}
            valueStyle={{ fontSize: '16px' }}
          />
        </Col>
        <Col span={6}>
          <Statistic 
            title="已同步" 
            value={syncedCount}
            valueStyle={{ color: '#52c41a', fontSize: '16px' }}
          />
        </Col>
        <Col span={6}>
          <Statistic 
            title="失败" 
            value={failedCount}
            valueStyle={{ color: '#ff4d4f', fontSize: '16px' }}
          />
        </Col>
      </Row>

      {totalCount > 0 && (
        <div style={{ marginBottom: 24 }}>
          <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: 8 }}>
            <span>同步进度</span>
            <span>{syncProgress}%</span>
          </div>
          <Progress 
            percent={syncProgress} 
            status={syncProgress === 100 ? 'success' : 'active'}
            strokeColor={{
              '0%': '#108ee9',
              '100%': '#87d068',
            }}
          />
        </div>
      )}

      {lastSyncTime && (
        <div style={{ marginBottom: 16, color: '#666', fontSize: '13px' }}>
          最后同步时间：{lastSyncTime}
        </div>
      )}

      {errors && errors.length > 0 && (
        <div style={{ marginTop: 16 }}>
          <h4 style={{ marginBottom: 8, color: '#ff4d4f' }}>同步失败记录：</h4>
          <List
            size="small"
            dataSource={errors}
            renderItem={(item) => (
              <List.Item>
                <Tag color="error">{item.company_name}</Tag>
                <span style={{ color: '#666', marginLeft: 8 }}>{item.error}</span>
              </List.Item>
            )}
            style={{ maxHeight: 150, overflow: 'auto' }}
          />
        </div>
      )}
    </Card>
  );
};

export default FeishuStatus;
