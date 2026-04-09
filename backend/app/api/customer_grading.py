from typing import Dict, Any, List, Optional
import openai
from app.config.config import settings

openai.api_key = settings.OPENAI_API_KEY

class DimensionScore:
    def __init__(self, name: str, score: float, max_score: float, reason: str):
        self.name = name
        self.score = score
        self.max_score = max_score
        self.reason = reason
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "name": self.name,
            "score": self.score,
            "max_score": self.max_score,
            "percentage": round((self.score / self.max_score) * 100, 2),
            "reason": self.reason
        }

class GradedCustomer:
    def __init__(self, customer_data: Dict[str, Any]):
        self.customer_data = customer_data
        self.total_score = 0.0
        self.max_total_score = 100.0
        self.grade = ""
        self.dimension_scores: List[DimensionScore] = []
        self.grade_reason = ""
        self.key_evidences: List[str] = []
        self.to_verify: List[str] = []
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            **self.customer_data,
            "total_score": self.total_score,
            "max_total_score": self.max_total_score,
            "grade": self.grade,
            "dimension_scores": [ds.to_dict() for ds in self.dimension_scores],
            "grade_reason": self.grade_reason,
            "key_evidences": self.key_evidences,
            "to_verify": self.to_verify
        }

class CustomerGrader:
    def __init__(self):
        self.grade_intervals = {
            "A": (85, 100),
            "B": (70, 84),
            "C": (50, 69),
            "D": (0, 49)
        }
        
        self.dimensions = [
            {"name": "市场匹配度", "weight": 30, "max_score": 30},
            {"name": "行业相关性", "weight": 25, "max_score": 25},
            {"name": "公司规模与实力", "weight": 20, "max_score": 20},
            {"name": "采购潜力", "weight": 15, "max_score": 15},
            {"name": "联系可达性", "weight": 10, "max_score": 10}
        ]
    
    def grade_customer(self, customer: Dict[str, Any], company_profile: Dict[str, Any], customer_strategy: Dict[str, Any]) -> GradedCustomer:
        graded_customer = GradedCustomer(customer)
        
        self._apply_rule_based_scoring(graded_customer, company_profile, customer_strategy)
        
        self._apply_model_based_enhancement(graded_customer, company_profile, customer_strategy)
        
        self._determine_grade(graded_customer)
        
        self._generate_explanation(graded_customer, company_profile, customer_strategy)
        
        return graded_customer
    
    def grade_multiple_customers(self, customers: List[Dict[str, Any]], company_profile: Dict[str, Any], customer_strategy: Dict[str, Any]) -> List[Dict[str, Any]]:
        graded_customers = []
        for customer in customers:
            graded = self.grade_customer(customer, company_profile, customer_strategy)
            graded_customers.append(graded.to_dict())
        
        graded_customers.sort(key=lambda x: x["total_score"], reverse=True)
        return graded_customers
    
    def _apply_rule_based_scoring(self, graded_customer: GradedCustomer, company_profile: Dict[str, Any], customer_strategy: Dict[str, Any]):
        customer = graded_customer.customer_data
        
        market_score = self._score_market_match(customer, company_profile, customer_strategy)
        graded_customer.dimension_scores.append(market_score)
        
        industry_score = self._score_industry_relevance(customer, company_profile, customer_strategy)
        graded_customer.dimension_scores.append(industry_score)
        
        size_score = self._score_company_size(customer, company_profile, customer_strategy)
        graded_customer.dimension_scores.append(size_score)
        
        potential_score = self._score_purchase_potential(customer, company_profile, customer_strategy)
        graded_customer.dimension_scores.append(potential_score)
        
        contact_score = self._score_contact_accessibility(customer, company_profile, customer_strategy)
        graded_customer.dimension_scores.append(contact_score)
        
        graded_customer.total_score = sum(ds.score for ds in graded_customer.dimension_scores)
    
    def _score_market_match(self, customer: Dict[str, Any], company_profile: Dict[str, Any], customer_strategy: Dict[str, Any]) -> DimensionScore:
        score = 0.0
        reason = ""
        customer_location = customer.get("location", "").lower()
        
        recommended_markets = [m.lower() for m in customer_strategy.get("recommended_markets", [])]
        
        if customer_location in recommended_markets:
            score = 30.0
            reason = f"客户位于推荐市场 '{customer.get('location', '未知')}'"
        elif any(market in customer_location for market in recommended_markets):
            score = 20.0
            reason = f"客户位于相关市场区域 '{customer.get('location', '未知')}'"
        elif customer_location:
            score = 10.0
            reason = f"客户位于非推荐市场 '{customer.get('location', '未知')}'"
        else:
            score = 5.0
            reason = "客户位置信息缺失"
        
        return DimensionScore("市场匹配度", score, 30, reason)
    
    def _score_industry_relevance(self, customer: Dict[str, Any], company_profile: Dict[str, Any], customer_strategy: Dict[str, Any]) -> DimensionScore:
        score = 0.0
        reason = ""
        customer_industry = customer.get("industry", "").lower()
        company_products = [p.lower() for p in company_profile.get("products_services", [])]
        recommended_segments = [s.lower() for s in customer_strategy.get("recommended_segments", [])]
        
        if any(segment in customer_industry for segment in recommended_segments):
            score = 25.0
            reason = f"客户行业 '{customer.get('industry', '未知')}' 匹配推荐客群"
        elif any(product in customer_industry for product in company_products):
            score = 18.0
            reason = f"客户行业 '{customer.get('industry', '未知')}' 与公司产品相关"
        elif customer_industry:
            score = 10.0
            reason = f"客户行业 '{customer.get('industry', '未知')}' 相关性较低"
        else:
            score = 5.0
            reason = "客户行业信息缺失"
        
        return DimensionScore("行业相关性", score, 25, reason)
    
    def _score_company_size(self, customer: Dict[str, Any], company_profile: Dict[str, Any], customer_strategy: Dict[str, Any]) -> DimensionScore:
        score = 0.0
        reason = ""
        
        icp_lite = customer_strategy.get("icp_lite", {})
        target_size = icp_lite.get("company_size", "").lower()
        
        company_name = customer.get("company_name", "").lower()
        size_indicators = {
            "large": ["group", "inc", "corporation", "global", "international", "holding"],
            "medium": ["ltd", "limited", "co.", "company"],
            "small": ["studio", "workshop", "local"]
        }
        
        detected_size = "unknown"
        for size, indicators in size_indicators.items():
            if any(indicator in company_name for indicator in indicators):
                detected_size = size
                break
        
        if detected_size != "unknown" and target_size:
            if detected_size == "large" and "large" in target_size:
                score = 20.0
                reason = "客户规模符合大型企业目标"
            elif detected_size == "medium" and "medium" in target_size:
                score = 18.0
                reason = "客户规模符合中型企业目标"
            elif detected_size == "small" and "small" in target_size:
                score = 15.0
                reason = "客户规模符合小型企业目标"
            elif detected_size == "large":
                score = 16.0
                reason = "客户为大型企业，有较强实力"
            elif detected_size == "medium":
                score = 12.0
                reason = "客户为中型企业，有一定实力"
            else:
                score = 8.0
                reason = "客户为小型企业"
        elif detected_size == "large":
            score = 14.0
            reason = "从公司名称判断为大型企业"
        elif detected_size == "medium":
            score = 10.0
            reason = "从公司名称判断为中型企业"
        else:
            score = 6.0
            reason = "公司规模信息有限"
        
        return DimensionScore("公司规模与实力", score, 20, reason)
    
    def _score_purchase_potential(self, customer: Dict[str, Any], company_profile: Dict[str, Any], customer_strategy: Dict[str, Any]) -> DimensionScore:
        score = 0.0
        reason = ""
        
        website = customer.get("website", "")
        company_name = customer.get("company_name", "")
        
        if website and "global" in website.lower() or "international" in website.lower():
            score = 15.0
            reason = "客户有国际化网站，可能有跨境采购需求"
        elif website:
            score = 10.0
            reason = "客户有官方网站，经营较为规范"
        elif company_name:
            score = 5.0
            reason = "仅有公司名称，采购潜力有待核实"
        else:
            score = 2.0
            reason = "客户信息不足，难以评估采购潜力"
        
        return DimensionScore("采购潜力", score, 15, reason)
    
    def _score_contact_accessibility(self, customer: Dict[str, Any], company_profile: Dict[str, Any], customer_strategy: Dict[str, Any]) -> DimensionScore:
        score = 0.0
        reason = ""
        
        website = customer.get("website", "")
        source_url = customer.get("source_url", "")
        
        if website:
            score = 10.0
            reason = f"可通过官网 '{website}' 联系客户"
        elif source_url:
            score = 6.0
            reason = f"可通过来源链接 '{source_url}' 获取更多信息"
        else:
            score = 2.0
            reason = "缺乏直接联系方式"
        
        return DimensionScore("联系可达性", score, 10, reason)
    
    def _determine_grade(self, graded_customer: GradedCustomer):
        score = graded_customer.total_score
        for grade, (min_score, max_score) in self.grade_intervals.items():
            if min_score <= score <= max_score:
                graded_customer.grade = grade
                break
    
    def _apply_model_based_enhancement(self, graded_customer: GradedCustomer, company_profile: Dict[str, Any], customer_strategy: Dict[str, Any]):
        pass
    
    def _generate_explanation(self, graded_customer: GradedCustomer, company_profile: Dict[str, Any], customer_strategy: Dict[str, Any]):
        grade = graded_customer.grade
        score = graded_customer.total_score
        
        grade_descriptions = {
            "A": "极高价值客户，建议优先重点跟进",
            "B": "高价值客户，建议积极跟进",
            "C": "中等价值客户，可适度跟进",
            "D": "低价值客户，可暂不投入或作为备选"
        }
        
        graded_customer.grade_reason = f"客户综合得分为 {score:.1f} 分，评定为 {grade} 级。{grade_descriptions.get(grade, '')}"
        
        graded_customer.key_evidences = []
        for ds in graded_customer.dimension_scores:
            if ds.score >= ds.max_score * 0.8:
                graded_customer.key_evidences.append(f"{ds.name}: {ds.reason}")
        
        if not graded_customer.key_evidences:
            top_dimension = max(graded_customer.dimension_scores, key=lambda x: x.score)
            graded_customer.key_evidences.append(f"{top_dimension.name}: {top_dimension.reason}")
        
        graded_customer.to_verify = []
        customer = graded_customer.customer_data
        
        if not customer.get("location"):
            graded_customer.to_verify.append("核实客户具体地理位置")
        if not customer.get("industry"):
            graded_customer.to_verify.append("核实客户具体行业")
        if not customer.get("website"):
            graded_customer.to_verify.append("查找客户官方网站")
        graded_customer.to_verify.append("核实客户公司规模和年营收")
        graded_customer.to_verify.append("确认客户关键决策人联系方式")
        
        if not graded_customer.to_verify:
            graded_customer.to_verify.append("进一步了解客户具体采购需求")

customer_grader = CustomerGrader()
