from typing import Dict, Any, List, Optional
import requests
import random
from app.config.config import settings

# 客户搜索输入结构
class CustomerSearchInput:
    def __init__(self, keywords: List[str], industry: Optional[str] = None, location: Optional[str] = None, company_size: Optional[str] = None):
        self.keywords = keywords
        self.industry = industry
        self.location = location
        self.company_size = company_size

# 规范化客户结果结构
class CustomerResult:
    def __init__(self, company_name: str, industry: str, location: str, website: str, source: str, source_url: str):
        self.company_name = company_name
        self.industry = industry
        self.location = location
        self.website = website
        self.source = source
        self.source_url = source_url

    def to_dict(self) -> Dict[str, Any]:
        return {
            "company_name": self.company_name,
            "industry": self.industry,
            "location": self.location,
            "website": self.website,
            "source": self.source,
            "source_url": self.source_url
        }

class CustomerSearcher:
    def __init__(self):
        pass

    def search_customers(self, search_input: CustomerSearchInput) -> List[Dict[str, Any]]:
        """搜索候选客户"""
        try:
            # 实现多个搜索来源
            sources = [
                self._search_from_api1,
                self._search_from_api2,
                self._search_from_mock
            ]

            results = []
            for source_func in sources:
                try:
                    source_results = source_func(search_input)
                    results.extend(source_results)
                except Exception as e:
                    # 单个来源失败不影响其他来源
                    print(f"搜索来源失败: {str(e)}")

            # 去重
            unique_results = self._deduplicate_results(results)

            # 限制结果数量为5-10个
            final_results = unique_results[:10] if len(unique_results) > 10 else unique_results
            if len(final_results) < 5:
                # 如果结果不足5个，补充一些模拟数据
                final_results = self._supplement_results(final_results, search_input, 10)

            return [result.to_dict() for result in final_results]

        except Exception as e:
            raise Exception(f"搜索客户失败: {str(e)}")

    def _search_from_api1(self, search_input: CustomerSearchInput) -> List[CustomerResult]:
        """从第一个搜索来源获取客户"""
        # 模拟 API 调用，实际项目中可以使用真实的 API
        results = []
        base_url = "https://api.example.com/search"

        # 模拟搜索结果
        mock_companies = [
            {"name": "Tech Innovations Inc", "industry": "Technology", "location": "United States", "website": "https://techinnovations.com"},
            {"name": "Global Trade Co", "industry": "Import/Export", "location": "United Kingdom", "website": "https://globaltrade.co.uk"},
            {"name": "Business Solutions Ltd", "industry": "Consulting", "location": "Germany", "website": "https://businesssolutions.de"}
        ]

        for company in mock_companies:
            if any(keyword.lower() in company["name"].lower() or keyword.lower() in company["industry"].lower() for keyword in search_input.keywords):
                results.append(CustomerResult(
                    company_name=company["name"],
                    industry=company["industry"],
                    location=company["location"],
                    website=company["website"],
                    source="API1",
                    source_url=f"{base_url}?q={'+'.join(search_input.keywords)}"
                ))

        return results

    def _search_from_api2(self, search_input: CustomerSearchInput) -> List[CustomerResult]:
        """从第二个搜索来源获取客户"""
        # 模拟另一个 API 调用
        results = []
        base_url = "https://directory.example.com/find"

        # 模拟搜索结果
        mock_companies = [
            {"name": "International Trading Group", "industry": "Trade", "location": "Canada", "website": "https://itg.ca"},
            {"name": "Digital Commerce Inc", "industry": "E-commerce", "location": "Australia", "website": "https://digitalcommerce.com.au"},
            {"name": "Global Business Network", "industry": "Networking", "location": "Singapore", "website": "https://gbn.sg"}
        ]

        for company in mock_companies:
            if any(keyword.lower() in company["name"].lower() or keyword.lower() in company["industry"].lower() for keyword in search_input.keywords):
                results.append(CustomerResult(
                    company_name=company["name"],
                    industry=company["industry"],
                    location=company["location"],
                    website=company["website"],
                    source="API2",
                    source_url=f"{base_url}?industry={search_input.industry}&location={search_input.location}"
                ))

        return results

    def _search_from_mock(self, search_input: CustomerSearchInput) -> List[CustomerResult]:
        """从模拟数据获取客户"""
        results = []
        base_url = "https://mock-directory.com/search"

        # 模拟更多搜索结果
        mock_companies = [
            {"name": "Worldwide Exports", "industry": "Export", "location": "Netherlands", "website": "https://worldwideexports.nl"},
            {"name": "Global Imports Ltd", "industry": "Import", "location": "Japan", "website": "https://globalimports.jp"},
            {"name": "Trade Partners Inc", "industry": "Trading", "location": "China", "website": "https://tradepartners.cn"},
            {"name": "International Business Co", "industry": "Business", "location": "India", "website": "https://internationalbusiness.in"},
            {"name": "Global Trade Solutions", "industry": "Solutions", "location": "Brazil", "website": "https://globaltradesolutions.br"}
        ]

        for company in mock_companies:
            if any(keyword.lower() in company["name"].lower() or keyword.lower() in company["industry"].lower() for keyword in search_input.keywords):
                results.append(CustomerResult(
                    company_name=company["name"],
                    industry=company["industry"],
                    location=company["location"],
                    website=company["website"],
                    source="Mock Directory",
                    source_url=f"{base_url}?keywords={'+'.join(search_input.keywords)}"
                ))

        return results

    def _deduplicate_results(self, results: List[CustomerResult]) -> List[CustomerResult]:
        """去重客户结果"""
        seen = set()
        unique_results = []
        for result in results:
            if result.company_name not in seen:
                seen.add(result.company_name)
                unique_results.append(result)
        return unique_results

    def _supplement_results(self, results: List[CustomerResult], search_input: CustomerSearchInput, target_count: int) -> List[CustomerResult]:
        """补充结果以达到目标数量"""
        current_count = len(results)
        if current_count >= target_count:
            return results

        # 补充一些额外的模拟数据
        supplement_companies = [
            {"name": "Global Commerce Group", "industry": "Commerce", "location": "France", "website": "https://globalcommerce.fr"},
            {"name": "International Trade Services", "industry": "Services", "location": "Spain", "website": "https://internationaltrade.es"},
            {"name": "World Trade Network", "industry": "Network", "location": "Italy", "website": "https://worldtradenetwork.it"},
            {"name": "Global Business Solutions", "industry": "Solutions", "location": "South Korea", "website": "https://globalbusiness.kr"},
            {"name": "International Trading Partners", "industry": "Partners", "location": "Russia", "website": "https://internationalpartners.ru"}
        ]

        supplement_results = []
        for company in supplement_companies:
            if len(results) + len(supplement_results) >= target_count:
                break
            if any(keyword.lower() in company["name"].lower() or keyword.lower() in company["industry"].lower() for keyword in search_input.keywords):
                supplement_results.append(CustomerResult(
                    company_name=company["name"],
                    industry=company["industry"],
                    location=company["location"],
                    website=company["website"],
                    source="Supplement Data",
                    source_url="https://supplement-directory.com/search"
                ))

        return results + supplement_results

customer_searcher = CustomerSearcher()