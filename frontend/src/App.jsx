import React, { useState, useEffect } from 'react';
import { 
  Layout, 
  Typography, 
  Button, 
  Upload, 
  message, 
  Space, 
  Row, 
  Col, 
  Divider,
  Modal,
  Steps,
  Card
} from 'antd';
import { 
  InboxOutlined, 
  PlayCircleOutlined, 
  ReloadOutlined 
} from '@ant-design/icons';
import AgentCard from './components/AgentCard';
import CustomerTable from './components/CustomerTable';
import CustomerDetailDrawer from './components/CustomerDetailDrawer';
import FeishuStatus from './components/FeishuStatus';
import './App.css';

const { Header, Content } = Layout;
const { Title, Text } = Typography;
const { Dragger } = Upload;
const { Step } = Steps;

const API_BASE = 'http://localhost:8000';

function App() {
  const [file, setFile] = useState(null);
  const [fileId, setFileId] = useState(null);
  const [isProcessing, setIsProcessing] = useState(false);
  const [currentStep, setCurrentStep] = useState(0);
  
  const [agentStatuses, setAgentStatuses] = useState({
    company: 'idle',
    search: 'idle',
    grading: 'idle',
    action: 'idle',
    feishu: 'idle',
  });
  
  const [agentProgress, setAgentProgress] = useState({
    company: 0,
    search: 0,
    grading: 0,
    action: 0,
    feishu: 0,
  });
  
  const [agentData, setAgentData] = useState({
    company: null,
    search: null,
    grading: null,
    action: null,
    feishu: null,
  });
  
  const [companyProfile, setCompanyProfile] = useState(null);
  const [customerStrategy, setCustomerStrategy] = useState(null);
  const [customers, setCustomers] = useState([]);
  const [selectedCustomer, setSelectedCustomer] = useState(null);
  const [drawerVisible, setDrawerVisible] = useState(false);
  
  const [feishuConnectionStatus, setFeishuConnectionStatus] = useState('unknown');
  const [feishuSyncing, setFeishuSyncing] = useState(false);
  const [feishuErrors, setFeishuErrors] = useState([]);
  const [lastSyncTime, setLastSyncTime] = useState(null);

  useEffect(() => {
    testFeishuConnection();
  }, []);

  const uploadProps = {
    name: 'file',
    multiple: false,
    accept: '.pdf',
    beforeUpload: (file) => {
      if (file.type !== 'application/pdf') {
        message.error('请上传 PDF 文件');
        return false;
      }
      setFile(file);
      return false;
    },
    fileList: file ? [{ uid: '1', name: file.name, status: 'done' }] : [],
  };

  const testFeishuConnection = async () => {
    setFeishuConnectionStatus('testing');
    try {
      const response = await fetch(`${API_BASE}/feishu/test-connection`);
      const result = await response.json();
      if (result.success) {
        setFeishuConnectionStatus('connected');
      } else {
        setFeishuConnectionStatus('disconnected');
      }
    } catch (error) {
      setFeishuConnectionStatus('disconnected');
    }
  };

  const simulateProgress = (agentType, duration) => {
    let progress = 0;
    const interval = setInterval(() => {
      progress += Math.random() * 20;
      if (progress >= 100) {
        progress = 100;
        clearInterval(interval);
      }
      setAgentProgress(prev => ({ ...prev, [agentType]: Math.min(Math.round(progress), 100) }));
    }, duration / 5);
    return interval;
  };

  const startFullProcess = async () => {
    if (!file) {
      message.error('请先上传 PDF 文件');
      return;
    }

    setIsProcessing(true);
    setCurrentStep(0);
    setCustomers([]);
    setFeishuErrors([]);

    try {
      await runStep1Upload();
      await runStep2CompanyProfile();
      await runStep3CustomerStrategy();
      await runStep4CustomerSearch();
      await runStep5Grading();
      await runStep6ActionSuggestions();
      
      message.success('所有步骤完成！');
    } catch (error) {
      message.error(`处理失败: ${error.message}`);
    } finally {
      setIsProcessing(false);
    }
  };

  const runStep1Upload = async () => {
    setAgentStatuses(prev => ({ ...prev, company: 'running' }));
    setCurrentStep(0);
    const progressInterval = simulateProgress('company', 2000);

    try {
      const formData = new FormData();
      formData.append('file', file);
      
      const response = await fetch(`${API_BASE}/upload/pdf`, {
        method: 'POST',
        body: formData,
      });
      
      const result = await response.json();
      if (!result.success) {
        throw new Error(result.error || '上传失败');
      }
      
      setFileId(result.file_id);
      clearInterval(progressInterval);
      setAgentProgress(prev => ({ ...prev, company: 100 }));
      setAgentStatuses(prev => ({ ...prev, company: 'completed' }));
      setAgentData(prev => ({ ...prev, company: result }));
      
    } catch (error) {
      clearInterval(progressInterval);
      setAgentStatuses(prev => ({ ...prev, company: 'error' }));
      throw error;
    }
  };

  const runStep2CompanyProfile = async () => {
    setAgentStatuses(prev => ({ ...prev, company: 'running' }));
    setCurrentStep(1);
    const progressInterval = simulateProgress('company', 3000);

    try {
      const response = await fetch(`${API_BASE}/generate-profile/${fileId}`, {
        method: 'POST',
      });
      
      const result = await response.json();
      if (!result.success) {
        throw new Error(result.error || '生成公司画像失败');
      }
      
      setCompanyProfile(result.profile);
      clearInterval(progressInterval);
      setAgentProgress(prev => ({ ...prev, company: 100 }));
      setAgentStatuses(prev => ({ ...prev, company: 'completed' }));
      setAgentData(prev => ({ ...prev, company: result.profile }));
      
    } catch (error) {
      clearInterval(progressInterval);
      setAgentStatuses(prev => ({ ...prev, company: 'error' }));
      throw error;
    }
  };

  const runStep3CustomerStrategy = async () => {
    setAgentStatuses(prev => ({ ...prev, search: 'running' }));
    setCurrentStep(2);
    const progressInterval = simulateProgress('search', 2000);

    try {
      const response = await fetch(`${API_BASE}/generate-strategy`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(companyProfile),
      });
      
      const result = await response.json();
      if (!result.success) {
        throw new Error(result.error || '生成客户策略失败');
      }
      
      setCustomerStrategy(result.strategy);
      clearInterval(progressInterval);
      setAgentProgress(prev => ({ ...prev, search: 100 }));
      setAgentStatuses(prev => ({ ...prev, search: 'completed' }));
      setAgentData(prev => ({ ...prev, search: result.strategy }));
      
    } catch (error) {
      clearInterval(progressInterval);
      setAgentStatuses(prev => ({ ...prev, search: 'error' }));
      throw error;
    }
  };

  const runStep4CustomerSearch = async () => {
    setAgentStatuses(prev => ({ ...prev, search: 'running' }));
    setCurrentStep(3);
    const progressInterval = simulateProgress('search', 4000);

    try {
      const keywords = customerStrategy?.target_markets?.slice(0, 3) || ['import', 'export', 'trade'];
      
      const response = await fetch(`${API_BASE}/search-customers`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          keywords,
          location: customerStrategy?.priority_markets?.[0],
        }),
      });
      
      const result = await response.json();
      if (!result.success) {
        throw new Error(result.error || '搜索客户失败');
      }
      
      const customersWithId = result.results.map((c, idx) => ({
        ...c,
        id: idx + 1,
        feishu_synced: false,
      }));
      
      setCustomers(customersWithId);
      clearInterval(progressInterval);
      setAgentProgress(prev => ({ ...prev, search: 100 }));
      setAgentStatuses(prev => ({ ...prev, search: 'completed' }));
      setAgentData(prev => ({ ...prev, search: result.results }));
      
    } catch (error) {
      clearInterval(progressInterval);
      setAgentStatuses(prev => ({ ...prev, search: 'error' }));
      throw error;
    }
  };

  const runStep5Grading = async () => {
    setAgentStatuses(prev => ({ ...prev, grading: 'running' }));
    setCurrentStep(4);
    const progressInterval = simulateProgress('grading', 3000);

    try {
      const response = await fetch(`${API_BASE}/grade-customers`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          customers,
          company_profile: companyProfile,
          customer_strategy: customerStrategy,
        }),
      });
      
      const result = await response.json();
      if (!result.success) {
        throw new Error(result.error || '客户分级失败');
      }
      
      const gradedCustomers = customers.map((c, idx) => ({
        ...c,
        ...result.graded_customers[idx],
      }));
      
      setCustomers(gradedCustomers);
      clearInterval(progressInterval);
      setAgentProgress(prev => ({ ...prev, grading: 100 }));
      setAgentStatuses(prev => ({ ...prev, grading: 'completed' }));
      setAgentData(prev => ({ ...prev, grading: result.graded_customers }));
      
    } catch (error) {
      clearInterval(progressInterval);
      setAgentStatuses(prev => ({ ...prev, grading: 'error' }));
      throw error;
    }
  };

  const runStep6ActionSuggestions = async () => {
    setAgentStatuses(prev => ({ ...prev, action: 'running' }));
    setCurrentStep(5);
    const progressInterval = simulateProgress('action', 3000);

    try {
      const response = await fetch(`${API_BASE}/generate-action-suggestions`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          graded_customers: customers,
          company_profile: companyProfile,
          customer_strategy: customerStrategy,
        }),
      });
      
      const result = await response.json();
      if (!result.success) {
        throw new Error(result.error || '生成动作建议失败');
      }
      
      const customersWithSuggestions = customers.map((c, idx) => ({
        ...c,
        ...result.suggestions[idx],
      }));
      
      setCustomers(customersWithSuggestions);
      clearInterval(progressInterval);
      setAgentProgress(prev => ({ ...prev, action: 100 }));
      setAgentStatuses(prev => ({ ...prev, action: 'completed' }));
      setAgentData(prev => ({ ...prev, action: result.suggestions }));
      
    } catch (error) {
      clearInterval(progressInterval);
      setAgentStatuses(prev => ({ ...prev, action: 'error' }));
      throw error;
    }
  };

  const syncToFeishu = async (customer) => {
    setFeishuSyncing(true);
    setAgentStatuses(prev => ({ ...prev, feishu: 'running' }));

    try {
      const response = await fetch(`${API_BASE}/feishu/add-record`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(customer),
      });
      
      const result = await response.json();
      if (result.success) {
        setCustomers(prev => prev.map(c => 
          c.id === customer.id ? { ...c, feishu_synced: true } : c
        ));
        setAgentStatuses(prev => ({ ...prev, feishu: 'completed' }));
        setLastSyncTime(new Date().toLocaleString());
        message.success('同步到飞书成功！');
      } else {
        throw new Error(result.error || '同步失败');
      }
    } catch (error) {
      setFeishuErrors(prev => [...prev, { company_name: customer.company_name, error: error.message }]);
      setAgentStatuses(prev => ({ ...prev, feishu: 'error' }));
      message.error(`同步失败: ${error.message}`);
    } finally {
      setFeishuSyncing(false);
    }
  };

  const syncAllToFeishu = async () => {
    setFeishuSyncing(true);
    setAgentStatuses(prev => ({ ...prev, feishu: 'running' }));
    const progressInterval = simulateProgress('feishu', 5000);

    try {
      const unsynced = customers.filter(c => !c.feishu_synced);
      const response = await fetch(`${API_BASE}/feishu/add-records-batch`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(unsynced),
      });
      
      const result = await response.json();
      if (result.success) {
        setCustomers(prev => prev.map(c => ({ ...c, feishu_synced: true })));
        clearInterval(progressInterval);
        setAgentProgress(prev => ({ ...prev, feishu: 100 }));
        setAgentStatuses(prev => ({ ...prev, feishu: 'completed' }));
        setLastSyncTime(new Date().toLocaleString());
        message.success('全部同步成功！');
      } else {
        throw new Error(result.error || '批量同步失败');
      }
    } catch (error) {
      clearInterval(progressInterval);
      setAgentStatuses(prev => ({ ...prev, feishu: 'error' }));
      message.error(`批量同步失败: ${error.message}`);
    } finally {
      setFeishuSyncing(false);
    }
  };

  const viewCustomerDetail = (customer) => {
    setSelectedCustomer(customer);
    setDrawerVisible(true);
  };

  const resetProcess = () => {
    setFile(null);
    setFileId(null);
    setIsProcessing(false);
    setCurrentStep(0);
    setAgentStatuses({
      company: 'idle',
      search: 'idle',
      grading: 'idle',
      action: 'idle',
      feishu: 'idle',
    });
    setAgentProgress({
      company: 0,
      search: 0,
      grading: 0,
      action: 0,
      feishu: 0,
    });
    setAgentData({
      company: null,
      search: null,
      grading: null,
      action: null,
      feishu: null,
    });
    setCompanyProfile(null);
    setCustomerStrategy(null);
    setCustomers([]);
    setSelectedCustomer(null);
    setDrawerVisible(false);
    setFeishuErrors([]);
  };

  const syncedCount = customers.filter(c => c.feishu_synced).length;
  const failedCount = feishuErrors.length;

  return (
    <Layout className="app-layout">
      <Header className="app-header">
        <div className="header-content">
          <Title level={3} style={{ margin: 0, color: 'white' }}>
            外贸获客智能体 Demo
          </Title>
          <Space>
            <Button 
              icon={<ReloadOutlined />} 
              onClick={resetProcess}
              disabled={isProcessing}
            >
              重置
            </Button>
          </Space>
        </div>
      </Header>

      <Content className="app-content">
        <div className="content-wrapper">
          <Card className="main-card">
            <div className="form-section">
              <Title level={4}>外贸获客智能体</Title>
              <div style={{ display: 'flex', flexWrap: 'wrap', gap: '16px', alignItems: 'center', marginBottom: '24px' }}>
                <div style={{ flex: '1 1 300px' }}>
                  <Upload {...uploadProps} style={{ width: '100%' }}>
                    <Button icon={<InboxOutlined />}>选择 PDF 文件</Button>
                  </Upload>
                  {file && (
                    <div style={{ marginTop: '8px' }}>
                      <Text strong>已选择文件：</Text>
                      <Text style={{ marginLeft: '8px' }}>{file.name}</Text>
                    </div>
                  )}
                </div>
                <Button 
                  type="primary" 
                  icon={<PlayCircleOutlined />}
                  onClick={startFullProcess}
                  loading={isProcessing}
                  disabled={!file || isProcessing}
                >
                  {isProcessing ? '处理中...' : '开始执行'}
                </Button>
              </div>
            </div>

            <div className="steps-section">
              <Title level={5}>处理流程</Title>
              <Steps current={currentStep} size="small">
                <Step title="上传 PDF" description="文件上传与预处理" />
                <Step title="公司画像" description="提取公司信息" />
                <Step title="客户策略" description="生成目标客户方向" />
                <Step title="客户搜索" description="搜索候选客户" />
                <Step title="客户分级" description="S/A/B/C/D 分级" />
                <Step title="动作建议" description="生成跟进建议" />
              </Steps>
            </div>

            <Divider />

            <div className="agents-section">
              <Title level={5}>Agent 工作状态</Title>
              <Row gutter={[16, 16]}>
                <Col xs={24} sm={12} md={12} lg={8} xl={8}>
                  <AgentCard 
                    type="company"
                    status={agentStatuses.company}
                    progress={agentProgress.company}
                    data={agentData.company}
                  />
                </Col>
                <Col xs={24} sm={12} md={12} lg={8} xl={8}>
                  <AgentCard 
                    type="search"
                    status={agentStatuses.search}
                    progress={agentProgress.search}
                    data={agentData.search}
                  />
                </Col>
                <Col xs={24} sm={12} md={12} lg={8} xl={8}>
                  <AgentCard 
                    type="grading"
                    status={agentStatuses.grading}
                    progress={agentProgress.grading}
                    data={agentData.grading}
                  />
                </Col>
                <Col xs={24} sm={12} md={12} lg={8} xl={8}>
                  <AgentCard 
                    type="action"
                    status={agentStatuses.action}
                    progress={agentProgress.action}
                    data={agentData.action}
                  />
                </Col>
                <Col xs={24} sm={12} md={12} lg={8} xl={8}>
                  <AgentCard 
                    type="feishu"
                    status={agentStatuses.feishu}
                    progress={agentProgress.feishu}
                    data={agentData.feishu}
                  />
                </Col>
              </Row>
            </div>

            <Divider />

            <div className="feishu-section">
              <FeishuStatus 
                connectionStatus={feishuConnectionStatus}
                totalCount={customers.length}
                syncedCount={syncedCount}
                failedCount={failedCount}
                lastSyncTime={lastSyncTime}
                syncing={feishuSyncing}
                onTestConnection={testFeishuConnection}
                onSyncAll={syncAllToFeishu}
                errors={feishuErrors}
              />
            </div>

            {customers.length > 0 && (
              <>
                <Divider />
                <div className="table-section">
                  <Title level={5}>客户结果</Title>
                  <CustomerTable 
                    data={customers}
                    loading={isProcessing}
                    onViewDetail={viewCustomerDetail}
                  />
                </div>
              </>
            )}
          </Card>
        </div>
      </Content>

      <CustomerDetailDrawer 
        visible={drawerVisible}
        onClose={() => setDrawerVisible(false)}
        customer={selectedCustomer}
        onSyncToFeishu={() => syncToFeishu(selectedCustomer)}
        syncing={feishuSyncing}
      />
    </Layout>
  );
}

export default App;
