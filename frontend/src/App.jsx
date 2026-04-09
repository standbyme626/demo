import { useState } from 'react'
import './App.css'

function App() {
  const [file, setFile] = useState(null)
  const [isUploading, setIsUploading] = useState(false)
  const [uploadProgress, setUploadProgress] = useState(0)
  const [uploadResult, setUploadResult] = useState(null)
  const [error, setError] = useState(null)
  
  // 客户搜索相关状态
  const [searchKeywords, setSearchKeywords] = useState('')
  const [searchIndustry, setSearchIndustry] = useState('')
  const [searchLocation, setSearchLocation] = useState('')
  const [searchCompanySize, setSearchCompanySize] = useState('')
  const [isSearching, setIsSearching] = useState(false)
  const [searchResults, setSearchResults] = useState([])
  const [searchError, setSearchError] = useState(null)

  const handleFileChange = (e) => {
    const selectedFile = e.target.files[0]
    if (selectedFile && selectedFile.type === 'application/pdf') {
      setFile(selectedFile)
      setError(null)
    } else {
      setError('请选择 PDF 文件')
      setFile(null)
    }
  }

  const handleUpload = async () => {
    if (!file) {
      setError('请先选择文件')
      return
    }

    setIsUploading(true)
    setUploadProgress(0)
    setError(null)
    setUploadResult(null)

    try {
      const formData = new FormData()
      formData.append('file', file)

      const response = await fetch('http://localhost:8000/upload/pdf', {
        method: 'POST',
        body: formData,
      })

      if (!response.ok) {
        throw new Error('上传失败')
      }

      const result = await response.json()
      setUploadResult(result)
    } catch (err) {
      setError(err.message)
    } finally {
      setIsUploading(false)
      setUploadProgress(100)
    }
  }

  const handleSearch = async () => {
    if (!searchKeywords.trim()) {
      setSearchError('请输入搜索关键词')
      return
    }

    setIsSearching(true)
    setSearchError(null)
    setSearchResults([])

    try {
      const response = await fetch('http://localhost:8000/search-customers', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          keywords: searchKeywords.split(',').map(k => k.trim()),
          industry: searchIndustry,
          location: searchLocation,
          company_size: searchCompanySize
        }),
      })

      if (!response.ok) {
        throw new Error('搜索失败')
      }

      const result = await response.json()
      if (result.success) {
        setSearchResults(result.results)
      } else {
        setSearchError(result.error)
      }
    } catch (err) {
      setSearchError(err.message)
    } finally {
      setIsSearching(false)
    }
  }

  return (
    <div className="app">
      <h1>外贸获客智能体</h1>
      
      <div className="upload-container">
        <h2>上传 PDF 文件</h2>
        
        <div className="file-input-wrapper">
          <input 
            type="file" 
            accept=".pdf" 
            onChange={handleFileChange}
            disabled={isUploading}
          />
          {file && (
            <div className="file-info">
              <span>{file.name}</span>
              <span>{(file.size / 1024).toFixed(2)} KB</span>
            </div>
          )}
        </div>

        {error && <div className="error-message">{error}</div>}

        <button 
          className="upload-button" 
          onClick={handleUpload}
          disabled={isUploading || !file}
        >
          {isUploading ? '上传中...' : '上传并解析'}
        </button>

        {isUploading && (
          <div className="progress-container">
            <div className="progress-bar">
              <div 
                className="progress-fill" 
                style={{ width: `${uploadProgress}%` }}
              ></div>
            </div>
            <span>{uploadProgress}%</span>
          </div>
        )}
      </div>

      {uploadResult && (
        <div className="result-container">
          <h2>上传结果</h2>
          <div className="result-card">
            <p><strong>状态:</strong> {uploadResult.status}</p>
            <p><strong>文件 ID:</strong> {uploadResult.file_id}</p>
            <p><strong>文件名:</strong> {uploadResult.filename}</p>
            <p><strong>OpenAI 文件 ID:</strong> {uploadResult.openai_file_id}</p>
          </div>
        </div>
      )}

      <div className="search-container">
        <h2>候选客户搜索</h2>
        
        <div className="search-form">
          <div className="form-group">
            <label>搜索关键词（逗号分隔）</label>
            <input 
              type="text" 
              value={searchKeywords}
              onChange={(e) => setSearchKeywords(e.target.value)}
              placeholder="例如：trade, import, export"
              disabled={isSearching}
            />
          </div>
          
          <div className="form-group">
            <label>行业</label>
            <input 
              type="text" 
              value={searchIndustry}
              onChange={(e) => setSearchIndustry(e.target.value)}
              placeholder="例如：Technology, Trade"
              disabled={isSearching}
            />
          </div>
          
          <div className="form-group">
            <label>位置</label>
            <input 
              type="text" 
              value={searchLocation}
              onChange={(e) => setSearchLocation(e.target.value)}
              placeholder="例如：United States, China"
              disabled={isSearching}
            />
          </div>
          
          <div className="form-group">
            <label>公司规模</label>
            <input 
              type="text" 
              value={searchCompanySize}
              onChange={(e) => setSearchCompanySize(e.target.value)}
              placeholder="例如：Small, Medium, Large"
              disabled={isSearching}
            />
          </div>

          {searchError && <div className="error-message">{searchError}</div>}

          <button 
            className="search-button" 
            onClick={handleSearch}
            disabled={isSearching || !searchKeywords.trim()}
          >
            {isSearching ? '搜索中...' : '搜索客户'}
          </button>
        </div>

        {searchResults.length > 0 && (
          <div className="search-results">
            <h3>搜索结果 ({searchResults.length})</h3>
            <div className="results-grid">
              {searchResults.map((result, index) => (
                <div key={index} className="result-card">
                  <h4>{result.company_name}</h4>
                  <p><strong>行业:</strong> {result.industry}</p>
                  <p><strong>位置:</strong> {result.location}</p>
                  <p><strong>网站:</strong> <a href={result.website} target="_blank" rel="noopener noreferrer">{result.website}</a></p>
                  <p><strong>来源:</strong> {result.source}</p>
                  <p><strong>来源链接:</strong> <a href={result.source_url} target="_blank" rel="noopener noreferrer">查看</a></p>
                </div>
              ))}
            </div>
          </div>
        )}
      </div>

      <div className="info-section">
        <h2>功能说明</h2>
        <p>本系统提供以下功能：</p>
        <ul>
          <li>上传 PDF 文件并解析</li>
          <li>基于公司画像生成客户策略</li>
          <li>搜索候选客户</li>
        </ul>
      </div>
    </div>
  )
}

export default App
