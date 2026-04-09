import React from 'react';
import { Table, Tag, Space, Button } from 'antd';
import { EyeOutlined } from '@ant-design/icons';

const gradeColorMap = {
  'A': '#52c41a',
  'B': '#1890ff',
  'C': '#faad14',
  'D': '#ff4d4f',
};

const CustomerTable = ({ data, loading, onViewDetail }) => {
  const columns = [
    {
      title: '公司名称',
      dataIndex: 'company_name',
      key: 'company_name',
      width: 200,
      render: (text, record) => (
        <div>
          <strong>{text}</strong>
          {record.website && (
            <div>
              <a 
                href={record.website} 
                target="_blank" 
                rel="noopener noreferrer"
                style={{ fontSize: '12px', color: '#1890ff' }}
              >
                {record.website}
              </a>
            </div>
          )}
        </div>
      ),
    },
    {
      title: '国家/地区',
      dataIndex: 'country',
      key: 'country',
      width: 120,
    },
    {
      title: '客户类型',
      dataIndex: 'customer_type',
      key: 'customer_type',
      width: 120,
      render: (text) => <Tag color="blue">{text}</Tag>,
    },
    {
      title: '客户等级',
      dataIndex: 'grade',
      key: 'grade',
      width: 100,
      render: (grade) => (
        <Tag 
          color={gradeColorMap[grade] || 'default'}
          style={{ 
            fontSize: '16px', 
            fontWeight: 'bold',
            padding: '4px 12px'
          }}
        >
          {grade}
        </Tag>
      ),
    },
    {
      title: '总分',
      dataIndex: 'total_score',
      key: 'total_score',
      width: 80,
      sorter: (a, b) => (a.total_score || 0) - (b.total_score || 0),
      render: (score) => <strong>{score}</strong>,
    },
    {
      title: '分级原因',
      dataIndex: 'grading_reason',
      key: 'grading_reason',
      width: 200,
      ellipsis: true,
    },
    {
      title: '动作建议',
      dataIndex: 'action_suggestion',
      key: 'action_suggestion',
      width: 200,
      ellipsis: true,
    },
    {
      title: '飞书同步',
      dataIndex: 'feishu_synced',
      key: 'feishu_synced',
      width: 100,
      render: (synced) => (
        <Tag color={synced ? 'success' : 'default'}>
          {synced ? '已同步' : '未同步'}
        </Tag>
      ),
    },
    {
      title: '操作',
      key: 'action',
      width: 100,
      fixed: 'right',
      render: (_, record) => (
        <Space size="middle">
          <Button 
            type="link" 
            icon={<EyeOutlined />}
            onClick={() => onViewDetail(record)}
          >
            详情
          </Button>
        </Space>
      ),
    },
  ];

  return (
    <div className="customer-table">
      <Table
        columns={columns}
        dataSource={data}
        rowKey="id"
        loading={loading}
        pagination={{
          pageSize: 10,
          showSizeChanger: true,
          showQuickJumper: true,
          showTotal: (total) => `共 ${total} 条记录`,
        }}
        scroll={{ x: 1200 }}
      />
    </div>
  );
};

export default CustomerTable;
