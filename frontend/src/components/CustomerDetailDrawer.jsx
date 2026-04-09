import React from 'react';
import { Drawer, Descriptions, Tag, Divider, Card, Space, Button } from 'antd';
import { ShareAltOutlined } from '@ant-design/icons';

const gradeColorMap = {
  'S': '#722ed1',
  'A': '#52c41a',
  'B': '#1890ff',
  'C': '#faad14',
  'D': '#ff4d4f',
};

const CustomerDetailDrawer = ({ 
  visible, 
  onClose, 
  customer, 
  onSyncToFeishu,
  syncing 
}) => {
  if (!customer) return null;

  return (
    <Drawer
      title={
        <div style={{ display: 'flex', alignItems: 'center', gap: 12 }}>
          <span>客户详情</span>
          {customer.grade && (
            <Tag 
              color={gradeColorMap[customer.grade]}
              style={{ 
                fontSize: '18px', 
                fontWeight: 'bold',
                padding: '4px 16px'
              }}
            >
              {customer.grade}级
            </Tag>
          )}
        </div>
      }
      width={700}
      open={visible}
      onClose={onClose}
      footer={
        <div style={{ textAlign: 'right' }}>
          <Space>
            <Button onClick={onClose}>关闭</Button>
            <Button 
              type="primary" 
              icon={<ShareAltOutlined />}
              onClick={onSyncToFeishu}
              loading={syncing}
              disabled={customer.feishu_synced}
            >
              {customer.feishu_synced ? '已同步' : '同步到飞书'}
            </Button>
          </Space>
        </div>
      }
    >
      <Descriptions title="基本信息" column={1} bordered style={{ marginBottom: 24 }}>
        <Descriptions.Item label="公司名称">
          <strong>{customer.company_name}</strong>
        </Descriptions.Item>
        <Descriptions.Item label="国家/地区">
          {customer.country}
        </Descriptions.Item>
        <Descriptions.Item label="官方网站">
          {customer.website ? (
            <a href={customer.website} target="_blank" rel="noopener noreferrer">
              {customer.website}
            </a>
          ) : (
            '待核实'
          )}
        </Descriptions.Item>
        <Descriptions.Item label="客户类型">
          <Tag color="blue">{customer.customer_type || '待分类'}</Tag>
        </Descriptions.Item>
        <Descriptions.Item label="联系方式">
          {customer.contact_info || '待核实'}
        </Descriptions.Item>
        <Descriptions.Item label="来源链接">
          {customer.source_url ? (
            <a href={customer.source_url} target="_blank" rel="noopener noreferrer">
              查看来源
            </a>
          ) : (
            '无'
          )}
        </Descriptions.Item>
      </Descriptions>

      <Divider />

      <Card title="客户评级" style={{ marginBottom: 24 }}>
        <Descriptions column={2} bordered>
          <Descriptions.Item label="客户等级" span={2}>
            <Tag 
              color={gradeColorMap[customer.grade]}
              style={{ 
                fontSize: '20px', 
                fontWeight: 'bold',
                padding: '8px 24px'
              }}
            >
              {customer.grade}
            </Tag>
          </Descriptions.Item>
          <Descriptions.Item label="总分">
            <strong style={{ fontSize: '18px' }}>{customer.total_score}</strong>
          </Descriptions.Item>
          <Descriptions.Item label="分项评分">
            {customer.score_details ? (
              <div>
                {Object.entries(customer.score_details).map(([key, value]) => (
                  <div key={key} style={{ marginBottom: 4 }}>
                    {key}: {value}分
                  </div>
                ))}
              </div>
            ) : (
              '暂无'
            )}
          </Descriptions.Item>
        </Descriptions>
        
        <div style={{ marginTop: 16 }}>
          <h4 style={{ marginBottom: 8 }}>分级原因：</h4>
          <p style={{ margin: 0, color: '#666' }}>
            {customer.grading_reason || '暂无'}
          </p>
        </div>
        
        <div style={{ marginTop: 12 }}>
          <h4 style={{ marginBottom: 8 }}>关键依据：</h4>
          <p style={{ margin: 0, color: '#666' }}>
            {customer.key_evidence || '暂无'}
          </p>
        </div>
        
        <div style={{ marginTop: 12 }}>
          <h4 style={{ marginBottom: 8 }}>待核实项：</h4>
          <p style={{ margin: 0, color: '#faad14' }}>
            {customer.to_verify || '暂无'}
          </p>
        </div>
      </Card>

      <Divider />

      <Card title="动作建议">
        {customer.action_suggestion ? (
          <div>
            <Descriptions column={1} bordered style={{ marginBottom: 16 }}>
              <Descriptions.Item label="优先级">
                <Tag color={
                  customer.action_priority === '高' ? 'red' :
                  customer.action_priority === '中' ? 'orange' : 'default'
                }>
                  {customer.action_priority || '中'}
                </Tag>
              </Descriptions.Item>
              <Descriptions.Item label="触达渠道">
                {customer.contact_channel || '邮件'}
              </Descriptions.Item>
              <Descriptions.Item label="跟进时机">
                {customer.follow_up_timing || '尽快'}
              </Descriptions.Item>
            </Descriptions>
            
            <div style={{ marginBottom: 16 }}>
              <h4 style={{ marginBottom: 8 }}>建议动作：</h4>
              <p style={{ margin: 0, color: '#666' }}>
                {customer.action_suggestion}
              </p>
            </div>
            
            <div>
              <h4 style={{ marginBottom: 8 }}>开场话术：</h4>
              <Card size="small" style={{ background: '#f5f5f5' }}>
                <p style={{ margin: 0, fontStyle: 'italic', color: '#333' }}>
                  {customer.opening_line || '暂无'}
                </p>
              </Card>
            </div>
          </div>
        ) : (
          <p style={{ color: '#999', textAlign: 'center', padding: '20px' }}>
            暂无动作建议
          </p>
        )}
      </Card>
    </Drawer>
  );
};

export default CustomerDetailDrawer;
